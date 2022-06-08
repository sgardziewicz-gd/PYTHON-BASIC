"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import pytest

from python_part_2.task_classes import Teacher, Student, Homework
import datetime

@pytest.fixture()
def teacher():
    return Teacher('Alan', 'Turing')


@pytest.fixture()
def student():
    return Student('Stan', 'Smith')


@pytest.fixture()
def homework_active():
    return Homework('CS presentation', 2)


@pytest.fixture()
def homework_inactive():
    return Homework('Biology excercise', -1)


def test_teacher_create_homework(teacher):
    test_homework = teacher.create_homework('test homework', 3)
    assert test_homework.text == 'test homework' and test_homework.days_to_complete == 3


def test_student_do_active_homework(student, homework_active):
    assert student.do_homework(homework_active).text == 'CS presentation'


def test_student_do_inactive_homework(student, homework_inactive, capfd):
    result = student.do_homework(homework_inactive)
    out, err = capfd.readouterr()
    assert result is None
    assert out == 'You are late\n'


def test_homework_deadline(homework_active):
    assert homework_active.deadline == homework_active.created + datetime.timedelta(2)


def test_homework_is_active(homework_active, homework_inactive):
    result_active = homework_active.is_active()
    result_inactive = homework_inactive.is_active()
    assert result_active == True
    assert result_inactive == False



    

