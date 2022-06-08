"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""
from cgitb import reset
from datetime import datetime


class WrongFormatException(Exception):
    """Raised when provided date string is in wrong format"""
    pass


def calculate_days(from_date: str) -> int:
    try:
        formated_from_date = datetime.fromisoformat(from_date)
    except ValueError:
        raise WrongFormatException("WrongFormatException")
    else:
        difference = datetime.today() - formated_from_date
        return difference.days

#print(calculate_days("10-12-2021"))


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""
import pytest


parameters = [("2022-06-05", 1), ("2022-06-06", 0), ("2022-06-07", -1), ("2022-05-31", 6)]


@pytest.mark.freeze_time('2022-06-06')
@pytest.mark.parametrize("test_input, expected", parameters)
def test_calculate_days_correct_format(test_input, expected):
    assert calculate_days(test_input) == expected


def test_calculate_days_wrong_format(capfd):
    with pytest.raises(WrongFormatException) as excinfo:
        calculate_days("04-04-2022")
    assert 'WrongFormatException' in str(excinfo.value)
