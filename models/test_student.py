import pytest
from student import Student, NameValueError, EmailError, PasswordError

def test_student_attributes():
    luke = Student(name="Luke", email="Luke@Tester.com", password='string1')
    assert luke.name == "Luke"
    assert luke.email == "Luke@Tester.com"
    assert luke.password == 'string1'

def test_student_to_dict():
    luke = Student(name="Luke", email="Luke@Tester.com", password='string1')
    assert luke.to_dict() == {"name": "Luke", "email": "Luke@Tester.com", "password":'string1'}

def test_student_invalid():
    with pytest.raises(NameValueError):
        Student(name=12345, email="Luke@Tester.com", password="string1")
    with pytest.raises(EmailError):
        Student(name="Luke", email=123456, password="string1")
    with pytest.raises(EmailError):
        Student(name="Luke", email="Luke@Tester", password="string1")
    with pytest.raises(EmailError):
        Student(name="Luke", email="Luke.com", password="string1")
    with pytest.raises(EmailError):
        Student(name="Luke", email="Luke.com@Tester", password="string1")
    with pytest.raises(PasswordError):
        Student(name="Luke", email="Luke@Tester.com", password=None)

# def test_student_invalid():
#     with pytest.raises(ValueError):
#         Student(name=12345, email="Luke@Tester.com", password="string1")
#     with pytest.raises(ValueError):
#         Student(name="Luke", email=123456, password="string1")
#     with pytest.raises(ValueError):
#         Student(name="Luke", email="Luke@Tester", password="string1")
#     with pytest.raises(ValueError):
#         Student(name="Luke", email="Luke.com", password="string1")
#     with pytest.raises(ValueError):
#         Student(name="Luke", email="Luke.com@Tester", password="string1")
#     with pytest.raises(ValueError):
#         Student(name="Luke", email="Luke@Tester.com", password=None)