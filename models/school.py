# Author: Desig9 by Deadline
# Date: April 27, 2022
# Flask API for GPA Calculator

from .student import Student
import json

class School:
    def __init__(self, name:str, *students:list):
        """initialize with name of school and list of students"""
        self.name=name

        self.students=list()
        with open('data/database.json') as fp:
            data = json.load(fp)
            for elem in data:
                self.students.append(Student(**elem))
    # ****can also do this -> **** self.students = [Student(**student) for student in data]


    def __len__(self):
        return len(self.students)

    def get_by_id(self, student_id: str):
        """get a student using student_id, return student or None"""
        for student in self.students:
            if student.student_id==student_id:
                return student

    def get_by_name(self, name:str):
        """get a student using student name, return list of students or empty list"""
        students=list()

        for student in self.students:
            if student.name==name:
                students.append(student)        
            
        return students

    def add(self, student:Student):
        """add a new Student, no return"""
        self.students.append(student)
    
    def delete(self, student_id:str):
        """delete student using student_id, return boolean"""
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                return True
        return False

    def save(self):
        """save student list to JSON file, no return"""
        students=list()
        with open('data/database', 'w') as fp:
            for student in self.students:
                students.append(student.to_dict())
            json.dump(students, fp)
