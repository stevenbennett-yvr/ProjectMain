from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import StringField, FieldList, IntegerField, SubmitField
# from wtforms.validators import DataRequired
from calculator import class_gpa_claculator, overall_gpa_calculator
from forms import GradesForm, UserForm
from databaseclasses import Users

app = Flask(__name__, template_folder='./templates')

# do we currently need these lines?
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "fuckit"


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    return render_template('add_user.html', form=form)


# How does this use POST?
@app.route('/', methods=['GET', 'POST'])
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
        return render_template('test.html', username=form.username.data, courses=courses, gpa=final_gpa, grades=course_gpas, form=form)
    return render_template('test.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
