# -*- coding: utf-8 -*-

from pathlib import Path

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


def test_recognize_url_none():
    href = None
    recognizer = ur.URLRecognizer()

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_ie_none():
    href = None
    basepath = 'c:/tmp'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_webkit_none():
    href = None
    basepath = '/tmp'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_ie_empty():
    href = ''
    basepath = 'c:/tmp'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_webkit_empty():
    href = ''
    basepath = '/tmp'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_ie_not():
    href = 'c:/tmp/'
    basepath = 'c:/tmp'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_webkit_not():
    href = '/tmp/'
    basepath = '/tmp'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_ie_anchor():
    href = 'c:/tmp#anchor'
    basepath = 'c:/tmp'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_webkit_anchor_1():
    href = '/tmp/#anchor'
    basepath = '/tmp'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_webkit_anchor_2():
    href = '/tmp/#anchor'
    basepath = '/tmp/'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_webkit_anchor_3():
    href = 'file:///tmp/#anchor'
    basepath = '/tmp/'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_ie_page_protocol():
    href = 'page://qqqqq/#anchor'
    basepath = 'c:/tmp'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_webkit_page_protocol():
    href = 'page://qqqqq/#anchor'
    basepath = '/tmp'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_file_ie_absolute_path():
    href = '../test/images/16x16.png'
    basepath = 'c:/tmp'
    recognizer = ur.FileRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(href).resolve())


def test_recognize_file_webkit_absolute_path_01():
    href = '../test/images/16x16.png'
    basepath = '/tmp'
    recognizer = ur.FileRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(href).resolve())


def test_recognize_file_webkit_absolute_path_02():
    href = 'file://../test/images/16x16.png'
    basepath = '/tmp'
    recognizer = ur.FileRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path('../test/images/16x16.png').resolve())


def test_recognize_file_ie_relative_path():
    href = '16x16.png'
    basepath = '../test/images'
    recognizer = ur.FileRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(basepath, href).resolve())


def test_recognize_file_webkit_relative_path():
    href = '16x16.png'
    basepath = '../test/images'
    recognizer = ur.FileRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(basepath, href).resolve())
