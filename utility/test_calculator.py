from calculator import class_gpa_claculator, overall_gpa_calculator, list_of_course_gpas, final_gpa_calculator
import pytest

def test_calculation():
    assert class_gpa_claculator(93) == 4.0
    assert class_gpa_claculator(91) == 3.7
    assert class_gpa_claculator(89) == 3.3
    assert class_gpa_claculator(83) == 3.0
    assert class_gpa_claculator(82) == 2.7
    assert class_gpa_claculator(79) == 2.3
    assert class_gpa_claculator(74) == 2.0
    assert class_gpa_claculator(72) == 1.7
    assert class_gpa_claculator(69) == 1.3
    assert class_gpa_claculator(64) == 1.0
    assert class_gpa_claculator(61) == 0.7
    assert class_gpa_claculator(55) == 0

def test_calculation_TypeError():
    with pytest.raises(TypeError):
        class_gpa_claculator('string')

def test_calculation_ValueError():
    with pytest.raises(ValueError):
        class_gpa_claculator(-10)

def test_overall_gpa_calculator():
    course_gpas = (1.0, 2.0, 3.0, 4.0)
    assert overall_gpa_calculator(course_gpas) == 2.5

def test_overall_gpa_calculator_TypeError():
    course_gpas = ('string1', 'string2', 'string3', 'string4')
    with pytest.raises(TypeError):
        overall_gpa_calculator(course_gpas)

def test_list_of_course_gpas():
    grades=(100,99,86,38)
    assert list_of_course_gpas(grades) == [4.0, 4.0, 3.0, 0]

def test_final_gpa_calculator():
    grades=(100,99,86,38)
    assert final_gpa_calculator(grades) == 2.75
