# imports from pip
# run `pip install bson flask flask_sqlalchemy flask_pymongo flask_wtf wtforms wtforms.validators datetime bcrypt pytest`
from bson import ObjectId
from flask import (
    Flask,
    render_template,
    redirect,
    flash,
    request,
    session,
    jsonify,
    url_for
)
from flask_pymongo import PyMongo, pymongo
from datetime import datetime
import bcrypt
import certifi

# Custom imports
from calculator import class_gpa_claculator, overall_gpa_calculator
from forms import GradesForm, UserForm


# Set up flask
app = Flask(__name__, template_folder='./templates', static_folder='./CSS')

# Session setup, required by flask_mongo and wtform
app.config['SECRET_KEY'] = "fuckit"

# Mongo setup
app.config['MONGO_URI'] = 'mongodb+srv://acit2911:acit2911@cluster0.nrjoq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)

ca = certifi.where()
mongo = pymongo.MongoClient(
    f'mongodb+srv://acit2911:acit2911@cluster0.nrjoq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority', tlsCAFile=ca)

db = mongo.db

# Database variables
records = db.register
transcripts = db.transcripts


@app.route("/", methods=['post', 'get'])
def index():
    # Registration page backend
    message = ''
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})
        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message)
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message)
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message)
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
            user_input = {'name': user, 'email': email, 'password': hashed}
            records.insert_one(user_input)

            user_data = records.find_one({"email": email})
            new_email = user_data['email']

            return render_template('logged_in.html', email=new_email)
    return render_template('index.html')


@app.route('/logged_in')
def logged_in():
    # homepage backend, ugly as sin and needs a lot of work
    if "email" in session:
        email = session["email"]
        # .find searches the database for all records that match the argument.
        # returns records as a cursor object, cursor object can be broken down into dictionaries.
        cursor = transcripts.find({"email": email})
        terms = []
        for document in cursor:
            print(type(document))
            terms.append(document)
        print(type(terms))
        return render_template("logged_in.html", email=email, session=session, parent_list=terms)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    # login page backend.
    message = 'Please login to your account'
    # is user alread logged in? redirect them to homepage
    if "email" in session:
        return redirect(url_for("logged_in"))
    # checks that user exists in database, logs them in.
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        email_found = records.find_one({"email": email})
        if email_found:
            email_val = email_found['email']
            passwordcheck = email_found['password']

            if bcrypt.checkpw(password.encode('utf-8'), passwordcheck):
                session["email"] = email_val
                return redirect(url_for('logged_in'))
            else:
                if "email" in session:
                    return redirect(url_for("logged_in"))
                message = 'Wrong password'
                return render_template('login.html', message=message)
        else:
            message = 'Email not found'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    # logout backend. very simple.
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    # gpa calculator backend
    # imports the gradeform object from form to autogenerate object from inputs
    form = GradesForm()
    # check if user is logged in, provides a save function.
    if "email" in session:
        email = session["email"]
        if form.validate_on_submit():
            print(request.form['submit_button'])
            # calculates gpa without writing to database.
            if request.form["submit_button"] == "Read":
                grades = form.grades.data
                courses = form.courses.data
                course_gpas = list()
                for grade in grades:
                    gpa = class_gpa_claculator(grade)
                    course_gpas.append(gpa)
                    # course_credits= cred * grade
                final_gpa = overall_gpa_calculator(course_gpas)
                return render_template('gpa_calc.html', courses=courses, gpa=final_gpa, grades=course_gpas, form=form, email=email)
            # writes grades to database.
            if request.form["submit_button"] == "Write":
                term = form.term.data
                grades = form.grades.data
                courses = form.courses.data
                res = {courses[i]: grades[i] for i in range(len(courses))}
                user_input = {'email': email, 'term': term, 'grades': res}
                transcripts.insert_one(user_input)
                return redirect(url_for('logged_in'))
        # standard render
        return render_template('gpa_calc.html', form=form, email=email)
    else:
        # if no user is logged in, provides calculator without function to write to database.
        if form.validate_on_submit():
            grades = form.grades.data
            courses = form.courses.data
            course_gpas = list()
            for grade in grades:
                gpa = class_gpa_claculator(grade)
                course_gpas.append(gpa)
                # course_credits= cred * grade
            final_gpa = overall_gpa_calculator(course_gpas)
            return render_template('gpa_calc.html', courses=courses, gpa=final_gpa, grades=course_gpas, form=form)
        return render_template('gpa_calc.html', form=form)


@app.route("/remove/<id>", methods=["GET", "POST"])
def delete_grade(id):
    # deletes grades/term record
    try:
        grade = transcripts.find_one({"_id": ObjectId(id)})
        if session["email"] == grade["email"]:
            transcripts.delete_one({"_id": ObjectId(id)})
            return redirect("/logged_in")
        else:
            return "404: invalid permissions", 404
    except:
        return "404: transcript not found", 404

# @app.route("/edit/<id>", methods=["GET", "POST"])
# def grade_update(id):
#     email = session["email"]
#     grade = transcripts.find_one({"_id": ObjectId(id)})
#     term = grade['term']
#     grades = grade['grades']
#     form = GradesForm()
#     if "email" in session:

#         return render_template('gpa_calc.html', form=form)
#     else:
#         return render_template('gpa_calc.html', form=form, email=email)


if __name__ == "__main__":
    app.run(debug=True)
