"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from unittest import result
import urllib.request

def make_request(url: str) -> Tuple[int, str]:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        code = response.status
    return (code, html)


"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""
import unittest.mock as mock


def test_make_request():
    m = mock.MagicMock()
    m.return_value.__enter__.return_value.status = 200
    m.return_value.__enter__.return_value.read.return_value = b'test response'
    with mock.patch('urllib.request.urlopen', m, create=True):
        result = make_request('https://test.com')
    assert result == (200,  'test response')

