
def class_gpa_claculator(grade=int):
    if type(grade)!=int:
        raise TypeError

    elif grade > 100 or grade < 0:
        raise ValueError

    elif grade >= 93:
        return 4.0

    elif grade >= 90:
        return 3.7

    elif grade >= 87:
        return  3.3

    elif grade >= 83:
        return  3.0

    elif grade >= 80:
        return  2.7

    elif grade >= 77:
        return  2.3

    elif grade >= 73:
        return  2.0

    elif grade >= 70:
        return  1.7

    elif grade >= 67:
        return  1.3

    elif grade >= 63:
        return  1.0

    elif grade >= 60:
        return  0.7

    elif grade >= 0 and grade < 60:
        return  0

def overall_gpa_calculator(course_gpas:list):
    try:
        final_gpa = round(sum(course_gpas)/len(course_gpas),2)
        return final_gpa
    except:
        raise TypeError

def list_of_course_gpas(grades):
    course_gpas = list()
    for grade in grades:
        gpa = class_gpa_claculator(grade)
        course_gpas.append(gpa)
    return course_gpas

def final_gpa_calculator(grades):
    """takes list of grades and calculates overall gpa by feeding into overall_gpa_calculator function and returns final GPA"""
    return overall_gpa_calculator(list_of_course_gpas(grades))