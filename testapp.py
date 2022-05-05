import sqlite3
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField, SubmitField
from wtforms.validators import DataRequired
from calculator import calculation
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='./templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = "fuckit"

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Name> {self.name}"


class GradesForm(FlaskForm):
    username = StringField("Your name", validators=[DataRequired()])
    grades = FieldList(IntegerField('Grades Name'),
                       min_entries=1, max_entries=10)


class UserForm(FlaskForm):
    name = StringField("Name", validator=[DataRequired()])
    email = StringField("Email", validator=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    return render_template('add_user.html', form=form)


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
