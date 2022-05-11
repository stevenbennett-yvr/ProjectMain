from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField, SubmitField
from wtforms.validators import DataRequired


class GradesForm(FlaskForm):
    courses = FieldList(StringField('Course'), min_entries=1, max_entries=10)
    grades = FieldList(IntegerField('Grade'), min_entries=1, max_entries=10)


class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Add User")
