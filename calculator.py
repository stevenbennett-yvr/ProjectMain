
def calculation(grade=int):
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
