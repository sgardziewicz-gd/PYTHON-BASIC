"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""
import math


class OperationNotFoundException(Exception):
    """Raised when provided operation which does not exist"""


def math_calculate(function: str, *args):
    args = args[:2]
    try:
        function = getattr(math, function)
    except AttributeError:
        raise OperationNotFoundException("Given operation does not exist")
    else:
        if len(args) == 1:
            return function(args[0])
        elif len(args) == 2:
            return function(args[0], args[1])

print(math_calculate('log', 1024, 2))
"""
Write tests for math_calculate function
"""
import pytest


def test_math_calculate_correct_function():
    assert math_calculate('log', 1024, 2) == 10.0
    assert math_calculate('log', 1024, 2, 4) == 10.0
    assert math_calculate('ceil', 10.7) == 11


def test_math_calculate_wrong_function():
    with pytest.raises(OperationNotFoundException) as excinfo:
        math_calculate('fsdfds', 2, 2)
    assert 'Given operation does not exist' in str(excinfo.value)
