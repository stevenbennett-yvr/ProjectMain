import sqlite3
from flask import Flask, render_template
# from flask_wtf import FlaskForm
# from wtforms import StringField, FieldList, IntegerField, SubmitField
# from wtforms.validators import DataRequired
from calculator import calculation
from forms import GradesForm, UserForm
from databaseclasses import Users

app = Flask(__name__, template_folder='./templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
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
        total = list()
        for grade in grades:
            gpa = calculation(grade)
            total.append(gpa)
        final_grade = sum(total)/len(total)
        final_gpa = round(final_grade, 2)
        return render_template('submit.html', username=form.username.data, gpa=final_gpa, grades=total, form=form)
    return render_template('test.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)
