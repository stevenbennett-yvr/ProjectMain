# Author: Desig9 by Deadline
# Date: April 27, 2022
# Flask API for GPA Calculator
from __future__ import print_function
from flask import Flask, render_template, request, jsonify
import json
from calculator import calculation
import sys


app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html"), 200

@app.route('/demo', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        grades = list()
        course1 = int(request.form['course1'])
        course2 = int(request.form['course2'])
        course3 = int(request.form['course3'])
        course4 = int(request.form['course4'])
        course5 = int(request.form['course5'])
        course6 = int(request.form['course6'])
        course7 = int(request.form['course7'])
        course8 = int(request.form['course8'])

        # print(f'{int(course1)}', file=sys.stderr)
        # print(course2, file=sys.stderr)
        grade1 = calculation(course1)
        grades.append(grade1)
        
        grade2 = calculation(course2)
        grades.append(grade2)

       
        grade3 = calculation(course3)
        grades.append(grade3)

        
        grade4 = calculation(course4)
        grades.append(grade4)

        
        grade5 = calculation(course5)
        grades.append(grade5)

        
        grade6 = calculation(course6)
        grades.append(grade6)

        
        grade7 = calculation(course7)
        grades.append(grade7)

        
        grade8 = calculation(course8)
        grades.append(grade8)

        final_grade = sum(grades)/len(grades)
        final_gpa = round(final_grade, 2)

        return render_template('demo.html', title='Demo', final_gpa = final_gpa, course1=grade1,course=grade2)
    else:
        return render_template('demo.html', title='Demo')


@app.route('/student/<student_id>', methods=["GET", "PUT", "DELETE"])
def getbyID(student_id):
    if request.method=="GET":
        pass

if __name__=="__main__":
    app.run(debug=True)