# Author: Desig9 by Deadline
# Date: April 27, 2022
# Flask API for GPA Calculator

class Student():
    def __init__(self, firstname:str, lastname:str, courses: list, studentnumber:str):
        """initializes student with name, student_id, and term (default of 1)"""

        self.firstname=firstname
        self.lastname=lastname
        self.courses=courses
        self.studentnumber=studentnumber

    def to_dict(self):
        """passes student to dictionary"""
        student_dict={"studentnumber":self.studentnumber, "firstName":self.firstname, "lastName":self.lastname, "courses":self.courses}
        return student_dict