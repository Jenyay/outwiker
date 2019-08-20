# -*- coding: utf-8 -*-

from outwiker.utilites.text import positionInside


def test_positionInside_empty():
    text = ''
    position = 0
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result


def test_positionInside_01():
    text = 'бла-бла-бла'
    position = 5
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result


def test_positionInside_02():
    text = '[=бла-бла-бла=]'
    position = 5
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert result


def test_positionInside_03():
    text = '[==]'
    position = 2
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert result


def test_positionInside_04():
    text = '[==]'
    position = 3
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result


def test_positionInside_05():
    text = '[==][==]'
    position = 2
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert result


def test_positionInside_06():
    text = '[==][==]'
    position = 4
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result


def test_positionInside_07():
    text = '[=[==][==]'
    position = 6
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result


def test_positionInside_08():
    text = '[=[==][==]=]'
    position = 6
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert result


def test_positionInside_09():
    text = '[=[==][==]=]'
    position = 8
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert result


def test_positionInside_10():
    text = '[==][==]=]'
    position = 4
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result


def test_positionInside_11():
    text = 'блабла[=...=]блабла'
    position = 6
    left = '[='
    right = '=]'

    result = positionInside(text, position, left, right)
    assert not result
