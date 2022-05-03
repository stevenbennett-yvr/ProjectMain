
def calculation(grade):
    grade = int(grade)
    
    if grade >= 93:
        calculation.grade = 4.0

    elif grade >= 90:
        calculation.grade = 3.7

    elif grade >= 87:
        calculation.grade = 3.3

    elif grade >= 83:
        calculation.grade = 3.0

    elif grade >= 80:
        calculation.grade = 2.7

    elif grade >= 77:
        calculation.grade = 2.3

    elif grade >= 73:
        calculation.grade = 2.0

    elif grade >= 70:
        calculation.grade = 1.7

    elif grade >= 67:
        calculation.grade = 1.3

    elif grade >= 63:
        calculation.grade = 1.0

    elif grade >= 60:
        calculation.grade = 0.7

    else:
        calculation.grade = 0
