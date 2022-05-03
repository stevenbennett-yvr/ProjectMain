# Author: Desig9 by Deadline
# Date: April 27, 2022
# Flask API for GPA Calculator

from flask import Flask, render_template, request, jsonify
import json
from calculator import calculation

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html"), 200

@app.route('/demo', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        grades = list()
        course1 = request.form['course1']
        course2 = request.form['course2']
        course3 = request.form['course3']
        course4 = request.form['course4']
        course5 = request.form['course5']
        course6 = request.form['course6']
        course7 = request.form['course7']
        course8 = request.form['course8']

        calculation(course1)
        grade1 = calculation.grade
        grades.append(grade1)

        calculation(course2)
        grade2 = calculation.grade
        grades.append(grade2)

        calculation(course3)
        grade3 = calculation.grade
        grades.append(grade3)

        calculation(course4)
        grade4 = calculation.grade
        grades.append(grade4)

        calculation(course5)
        grade5 = calculation.grade
        grades.append(grade5)

        calculation(course6)
        grade6 = calculation.grade
        grades.append(grade6)

        calculation(course7)
        grade7 = calculation.grade
        grades.append(grade7)

        calculation(course8)
        grade8 = calculation.grade
        grades.append(grade8)

        final_grade = sum(grades)/len(grades)
        final_gpa = round(final_grade, 2)

        return render_template('demo.html', title='Demo', final_gpa = final_gpa)
    else:
        return render_template('demo.html', title='Demo')


@app.route('/student/<student_id>', methods=["GET", "PUT", "DELETE"])
def getbyID(student_id):
    if request.method=="GET":
        pass

if __name__=="__main__":
    app.run(debug=True)