import pytest

from outwiker.utilites.urls import is_url


@pytest.mark.parametrize('line,expected', [
    ('blablabla', False),
    ('http:/adfadf', False),
    ('http://adfadf', True),
    ('page://adfadf/', True),
    ('https://adfadf/#sdfafd', True),
    ('xxx_yyy_111://adfadf/#sdfafd', True),
    ])
def test_is_url(line: str, expected: bool):
    assert is_url(line) == expected
