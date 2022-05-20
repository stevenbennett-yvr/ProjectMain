# pip install -r requirements.txt

from bson import ObjectId
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    session,
    url_for
)
from flask_pymongo import PyMongo, pymongo
import bcrypt
import certifi
from sqlalchemy import null
from models.student import Student

# Custom imports
from calculator import class_gpa_claculator, overall_gpa_calculator
from forms import GradesForm


# Set up flask
app = Flask(__name__, template_folder='./templates', static_folder='./static')

# Session setup, required by flask_mongo and wtform
app.config['SECRET_KEY'] = "123123"

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

"""
this seems to be a "registration" page and not a "home page", perhaps we should rename it? 
or better yet, make "/" route to "/registration" if not logged in
"""


@app.route("/register", methods=['post', 'get'])
def index():
    if "email" in session:
        return redirect(url_for("logged_in"))
    if request.method == "POST":
        user = request.form.get("fullname")
        email = request.form.get("email")
        email.lower()

        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user_found = records.find_one({"name": user})
        email_found = records.find_one({"email": email})

        if user_found:
            message = 'There already is a user by that name'
            return render_template('index.html', message=message), 200
        if email_found:
            message = 'This email already exists in database'
            return render_template('index.html', message=message), 200
        if password1 != password2:
            message = 'Passwords should match!'
            return render_template('index.html', message=message), 200
        else:
            hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())

            try:
                new_user = Student(user, email, hashed)
            except:
                message = 'Please make sure that: Your name is not all numbers, your email is in a correct format (example@website.com), and that you have entered a password'
                return render_template('index.html', message=message), 200
            records.insert_one(new_user.to_dict())

            user_data = records.find_one({"email": email})
            new_email = user_data['email']
            session["email"] = email
            return redirect(url_for("logged_in"))
    return render_template('index.html'), 200


@app.route('/logged_in/')
def logged_in():
    # homepage backend, ugly as sin and needs a lot of work
    if "email" in session:
        email = session["email"]
        email.lower()
        record = records.find_one({"email": email})
        name = record["name"]
        id = record["_id"]
        # .find searches the database for all records that match the argument.
        # returns records as a cursor object, cursor object can be broken down into dictionaries.
        cursor = transcripts.find({"userid": id})
        terms = []
        for document in cursor:
            terms.append(document)
        return render_template("logged_in.html", email=email, session=session, parent_list=terms, user_id=id, name=name), 201
    else:
        return redirect(url_for("/"))


@app.route("/", methods=["POST", "GET"])
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
                return render_template('login.html', message=message), 200
        else:
            message = 'Email not found'
            return render_template('login.html', message=message), 200
    return render_template('login.html', message=message), 200


@app.route("/logout", methods=["POST", "GET"])
def logout():
    # logout backend. very simple.
    if "email" in session:
        session.pop("email", None)
        message="You are signed out!"
        return render_template("signout.html", message=message), 200
    else:
        return render_template('index.html'), 200


@app.route('/gpa_calc', methods=['GET', 'POST'])
def gpa_calc():
    # gpa calculator backend
    # imports the gradeform object from form to autogenerate object from inputs
    form = GradesForm()
    # check if user is logged in, provides a save function.
    if "email" in session:
        email = session["email"]
        record = records.find_one({"email": email})
        id = record["_id"]
        if form.validate_on_submit():
            # calculates gpa without writing to database.
            if request.form["submit_button"] == "Read":
                print(form.data)
                grades = form.grades.data
                courses = form.courses.data
                course_gpas = list()
                for grade in grades:
                    gpa = class_gpa_claculator(grade)
                    course_gpas.append(gpa)
                    # course_credits= cred * grade
                final_gpa = overall_gpa_calculator(course_gpas)
                return render_template('gpa_calc.html', courses=courses, gpa=final_gpa, grades=course_gpas, form=form, email=email), 200
            # writes grades to database.
            if request.form["submit_button"] == "Write":
                term = form.term.data
                grades = form.grades.data
                courses = form.courses.data
                course_gpas = list()
                for grade in grades:
                    gpa = class_gpa_claculator(grade)
                    course_gpas.append(gpa)
                    # course_credits= cred * grade
                final_gpa = overall_gpa_calculator(course_gpas)
                res = {courses[i]: grades[i] for i in range(len(courses))}
                user_input = {'userid': id, 
                            'term': term,
                            'gpa': final_gpa, 
                            'grades': res}
                transcripts.insert_one(user_input)
                return redirect(url_for('logged_in'))
        # standard render
        return render_template('gpa_calc.html', form=form, email=email), 201
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
            return render_template('gpa_calc.html', courses=courses, gpa=final_gpa, grades=course_gpas, form=form), 201
        return render_template('gpa_calc.html', form=form), 200


@app.route("/remove/<id>", methods=["GET", "POST"])
def delete_grade(id):
    # deletes grades/term record
    try:
        grade = transcripts.find_one({"_id": ObjectId(id)})
        email = session["email"]
        record = records.find_one({"email": email})
        sessionid = record["_id"]
        if sessionid == grade["userid"]:
            transcripts.delete_one({"_id": ObjectId(id)})
            return redirect("/logged_in")
        else:
            return "404: invalid permissions", 404
    except:
        return "404: transcript not found", 404


@app.route("/user_edit/<id>", methods=["GET", "POST"])
def update_user(id):

    email = session["email"]
    record = records.find_one({"email": email})
    user_id = record["_id"]
    currentuser = record["name"]
    currentemail = record["email"]
    if "email" in session:
        if request.method == "POST":
            # does the current password match the records password
            currentpassword = request.form.get("currentpassword")
            record = records.find_one({"_id": user_id})
            passwordcheck = record['password']
            if bcrypt.checkpw(currentpassword.encode('utf-8'), passwordcheck):
                # logic for repalcement
                user_data={}
                newname = request.form.get("fullname")
                if newname is not None:
                    if newname != currentuser:
                        user_found = records.find_one({"name": newname})
                        if user_found:
                            message = 'There already is a user by that name'
                            return render_template('edit_user.html', message=message), 200
                        else:
                            user_data["name"]=newname
                    pass
                newemail = request.form.get("email")
                newemail.lower()
                if newemail is not None:
                    if newemail != currentemail:
                        email_found = records.find_one({"email": newemail})
                        if email_found:
                            message = 'This email already exists in database'
                            return render_template('edit_user.html', message=message), 200
                        else:
                            user_data["email"] = newemail
                    else:
                        pass
                password1 = request.form.get("password1")
                password2 = request.form.get("password2")
                if password2 != None and password1 != None:
                    if password1 != password2:
                        message = 'Passwords should match!'
                        return render_template('edit_user.html', message=message), 200
                    else:
                        hashed = bcrypt.hashpw(
                            password2.encode('utf-8'), bcrypt.gensalt())
                        user_data['password']=hashed
                else:
                    pass
                records.update_one(
                    {'_id': ObjectId(id)},
                    {'$set': user_data}
                )
                if "email" in session:
                    session.pop("email", None)
                    message="You have successfully changed your account information, please log in again!"
                    return render_template("signout.html", message=message), 200
            else:
                message = "Password Incorrect"
                return render_template('edit_user.html', message=message), 200
    return render_template('edit_user.html', user=currentuser, email=currentemail), 200


@app.route("/term_edit/<id>", methods=["GET", "POST"])
def update_term(id):
    term = transcripts.find_one({"_id": ObjectId(id)})
    currentterm = term["term"]
    currentgrades = term["grades"]
    courses = currentgrades.keys()
    grades = currentgrades.values()
    courses = list(courses)
    grades = list(grades)
    form = GradesForm()
    if form.validate_on_submit():
        if request.form["submit_button"] == "Read":
            term = form.term.data
            grades = form.grades.data
            courses = form.courses.data
            course_gpas = list()
            for grade in grades:
                gpa = class_gpa_claculator(grade)
                course_gpas.append(gpa)
            final_gpa = overall_gpa_calculator(course_gpas)
            return render_template('edit_term.html', form=form, currentterm=term, courses=courses, grades=grades, gpa=final_gpa), 200
        if request.form["submit_button"] == "Write":
            term = form.term.data
            grades = form.grades.data
            courses = form.courses.data
            course_gpas = list()
            for grade in grades:
                gpa = class_gpa_claculator(grade)
                course_gpas.append(gpa)
                # course_credits= cred * grade
            final_gpa = overall_gpa_calculator(course_gpas)
            res = {courses[i]: grades[i] for i in range(len(courses))}
            user_input = {'term': term,
                          'gpa': final_gpa, 
                          'grades': res}
            transcripts.update_one({'_id': ObjectId(id)},
                                   {'$set': user_input})
            return redirect(url_for('logged_in'))
    return render_template('edit_term.html', form=form, currentterm=currentterm, courses=courses, grades=grades), 200


if __name__ == "__main__":
    app.run(debug=True)
