# Author: Desig9 by Deadline
# Date: April 27, 2022
# Flask API for GPA Calculator

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def homepage():
    return render_template("index.html"), 200

@app.route('/student/<student_id>', methods=["GET", "PUT", "DELETE"])
def getbyID(student_id):
    if request.method=="GET":
        pass

if __name__=="__main__":
    app.run(debug=True)