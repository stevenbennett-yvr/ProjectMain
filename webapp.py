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
from flask_pymongo import PyMongo
from calculator import class_gpa_claculator, overall_gpa_calculator
from forms import GradesForm, UserForm
from datetime import datetime
import bcrypt

app = Flask(__name__, template_folder='./templates', static_folder='./CSS')

# do we currently need these lines?
app.config['SECRET_KEY'] = "fuckit"
app.config['MONGO_URI'] = 'mongodb+srv://acit2911:acit2911@cluster0.nrjoq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)
db = mongo.db
records = db.register
transcripts = db.transcripts


@app.route("/", methods=['post', 'get'])
def index():
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
    if "email" in session:
        email = session["email"]
        cursor = transcripts.find({"email": email})
        terms = []
        for document in cursor:
            print(document)
            terms.append(document)
        return render_template("logged_in.html", email=email, session=session, terms=terms)
    else:
        return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    message = 'Please login to your account'
    if "email" in session:
        return redirect(url_for("logged_in"))

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
    if "email" in session:
        session.pop("email", None)
        return render_template("signout.html")
    else:
        return render_template('index.html')
# How does this use POST?


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    form = GradesForm()
    if "email" in session:
        email = session["email"]
        if form.validate_on_submit():
            print(request.form['submit_button'])
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
            if request.form["submit_button"] == "Write":
                term = form.term.data
                grades = form.grades.data
                courses = form.courses.data
                res = {courses[i]: grades[i] for i in range(len(courses))}
                user_input = {'email': email, 'term': term, 'grades': res}
                transcripts.insert_one(user_input)
                return redirect(url_for('logged_in'))
        return render_template('gpa_calc.html', form=form, email=email)
    else:
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


if __name__ == "__main__":
    app.run(debug=True)
