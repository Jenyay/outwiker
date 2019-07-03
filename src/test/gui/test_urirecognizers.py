# -*- coding: utf-8 -*-

import outwiker.gui.urirecognizers as ur


def test_recognize_url_http():
    href = 'http://jenyay.net'
    recognizer = ur.URLRecognizer()

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_https():
    href = 'https://jenyay.net'
    recognizer = ur.URLRecognizer()

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_mailto():
    href = 'mailto:example@example.com'
    recognizer = ur.URLRecognizer()

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_ftp():
    href = 'ftp://jenyay.net'
    recognizer = ur.URLRecognizer()

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_invalid():
    href = 'page://jenyay.net'
    recognizer = ur.URLRecognizer()

    result = recognizer.recognize(href)
    assert result is None
