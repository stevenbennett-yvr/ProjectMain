from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, IntegerField
from wtforms.validators import DataRequired
from calculator import calculation


class FavouriteGradesForm(FlaskForm):
    username = StringField("Your name", validators=[DataRequired()])
    grades = FieldList(IntegerField('Grades Name'),
                       min_entries=1, max_entries=10)


app = Flask(__name__, template_folder='./templates')
app.config['SECRET_KEY'] = "fuckit"


@app.route('/', methods=['GET', 'POST'])
def index():
    form = FavouriteGradesForm()
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
