from flask import (
    Flask,
    render_template, 
    redirect, 
    flash, 
    request
)
from flask_pymongo import PyMongo
from calculator import class_gpa_claculator, overall_gpa_calculator
from forms import GradesForm, UserForm
from datetime import datetime


app = Flask(__name__, template_folder='./templates', static_folder='./CSS')

# do we currently need these lines?
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "fuckit"
app.config['MONGO_URI'] = 'mongodb+srv://acit2911:acit2911@cluster0.nrjoq.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def homepage():
    return render_template("homepage.html", title = "Layout Page")

@app.route('/user/add', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        form = UserForm(request.form)
        user_name = form.name.data
        user_email = form.email.data

        db.agile.users.insert_one({
            "name": user_name,
            "email": user_email,
            "date_added": datetime.utcnow()
        })
        flash("User successfully added", "success")
        return redirect('/')
    else:
        form = UserForm()
    return render_template('add_user.html', form=form)

# How does this use POST?
@app.route('/demo', methods=['GET', 'POST'])
def index():
    form = GradesForm()
    if form.validate_on_submit():
        grades = form.grades.data
        courses = form.courses.data
        course_gpas = list()
        for grade in grades:
            gpa = class_gpa_claculator(grade)
            course_gpas.append(gpa)
            # course_credits= cred * grade
        final_gpa = overall_gpa_calculator(course_gpas)
        return render_template('gpa_calc.html', username=form.username.data, courses=courses, gpa=final_gpa, grades=course_gpas, form=form)
    return render_template('gpa_calc.html', form=form)



if __name__ == "__main__":
    app.run(debug=True)
