"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""
import re


def is_http_domain(domain: str) -> bool:
    regex = re.compile('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
    return bool(re.match(regex, domain))

"""
write tests for is_http_domain function
"""
import pytest

def test_is_http_domain():
    assert is_http_domain('http://wikipedia.org')
    assert is_http_domain('https://ru.wikipedia.org/')
    assert not is_http_domain('griddynamics.com')