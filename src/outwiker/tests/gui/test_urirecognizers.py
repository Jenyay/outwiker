# -*- coding: utf-8 -*-

from pathlib import Path
import unittest

import outwiker.gui.urirecognizers as ur
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.basetestcases import BaseOutWikerMixin


def test_recognize_url_http():
    href = 'http://jenyay.net'
    recognizer = ur.URLRecognizer('')

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_https():
    href = 'https://jenyay.net'
    basepath = ''
    recognizer = ur.URLRecognizer('')

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_mailto():
    href = 'mailto:example@example.com'
    recognizer = ur.URLRecognizer('')

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_ftp():
    href = 'ftp://jenyay.net'
    recognizer = ur.URLRecognizer('')

    result = recognizer.recognize(href)
    assert result == href


def test_recognize_url_invalid():
    href = 'page://jenyay.net'
    recognizer = ur.URLRecognizer('')

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_url_none():
    href = None
    recognizer = ur.URLRecognizer('')

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_ie_none():
    href = None
    basepath = 'c:/tmp/__content.html'
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
    basepath = 'c:/tmp/__content.html'
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
    href = 'c:/tmp/__content.html'
    basepath = 'c:/tmp/__content.html'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_webkit_not():
    href = '/tmp/'
    basepath = '/tmp'
    recognizer = ur.AnchorRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result is None


def test_recognize_anchor_ie_anchor_01():
    href = 'c:/tmp/__content.html#anchor'
    basepath = 'c:/tmp/__content.html'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_ie_anchor_02():
    href = 'c:/tmp/__content.html#anchor'
    basepath = 'c:\\tmp\\__content.html'
    recognizer = ur.AnchorRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == '#anchor'


def test_recognize_anchor_ie_anchor_03():
    href = 'c:/tmp/__content.html#anchor'
    basepath = 'c:\\tmp\\__content.html#oldanchor'
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
    basepath = 'c:/tmp/__content.html'
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
    href = 'testdata/images/16x16.png'
    basepath = 'c:/tmp/__content.html'
    recognizer = ur.FileRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(href).resolve())


def test_recognize_file_webkit_absolute_path_01():
    href = 'testdata/images/16x16.png'
    basepath = '/tmp'
    recognizer = ur.FileRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(href).resolve())


def test_recognize_file_webkit_absolute_path_02():
    href = 'file://testdata/images/16x16.png'
    basepath = '/tmp'
    recognizer = ur.FileRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path('testdata/images/16x16.png').resolve())


def test_recognize_file_ie_relative_path_01():
    href = '16x16.png'
    basepath = 'testdata/images'
    recognizer = ur.FileRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(basepath, href).resolve())


def test_recognize_file_ie_relative_path_02():
    href = '16x16.png'
    basepath = 'testdata/images/__init__.py'
    recognizer = ur.FileRecognizerIE(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path('testdata/images/16x16.png').resolve())


def test_recognize_file_webkit_relative_path():
    href = '16x16.png'
    basepath = 'testdata/images'
    recognizer = ur.FileRecognizerWebKit(basepath)

    result = recognizer.recognize(href)
    assert result == str(Path(basepath, href).resolve())


class PageRecognizerTest(unittest.TestCase, BaseOutWikerMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.page_1 = TextPageFactory().create(self.wikiroot, "Страница 1", [])
        self.page_2 = TextPageFactory().create(self.wikiroot, "Страница 2", [])
        self.page_1_1 = TextPageFactory().create(self.page_1, "Подстраница 1", [])

        self.page_1_uid = self.application.pageUidDepot.createUid(self.page_1)
        self.page_2_uid = self.application.pageUidDepot.createUid(self.page_2)

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.page_1

    def _getBasePathIE(self, page) -> str:
        return str(Path(page.path, '__content.html')).replace('\\', '/')

    def _getBasePathWebKit(self, page) -> str:
        return page.path

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_page_protocol_webkit_none(self):
        href = 'page://invalid'
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result is None

    def test_page_protocol_ie_none(self):
        href = 'page://invalid'
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result is None

    def test_page_protocol_webkit_01(self):
        href = 'page://' + self.page_2_uid
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_protocol_ie_01(self):
        href = 'page://' + self.page_2_uid
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_protocol_webkit_02(self):
        href = 'page://' + self.page_2.title
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_protocol_ie_02(self):
        basepath = self._getBasePathIE(self.application.selectedPage)
        href = 'page://' + self.page_2.title
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_protocol_webkit_03(self):
        href = 'page://' + self.page_1_1.title
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_protocol_ie_03(self):
        href = 'page://' + self.page_1_1.title
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_protocol_webkit_04(self):
        href = 'page://{}/{}'.format(self.page_1.title, self.page_1_1.title)
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_protocol_ie_04(self):
        href = 'page://{}/{}'.format(self.page_1.title, self.page_1_1.title)
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_path_webkit_none(self):
        href = 'invalid page'
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result is None

    def test_page_path_ie_none(self):
        href = 'invalid page'
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result is None

    def test_page_path_webkit_01(self):
        href = self.page_2.subpath
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_path_ie_01(self):
        href = self.page_2.subpath
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_path_webkit_02(self):
        href = '/' + self.page_2.subpath
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_path_ie_02(self):
        href = '/' + self.page_2.subpath
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_2

    def test_page_path_webkit_03(self):
        href = self.page_1_1.subpath
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_path_ie_03(self):
        href = self.page_1_1.subpath
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_path_webkit_04(self):
        href = '/' + self.page_1_1.subpath
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_path_ie_04(self):
        href = '/' + self.page_1_1.subpath
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_path_webkit_05(self):
        href = self.page_1_1.title
        basepath = self._getBasePathWebKit(self.application.selectedPage)
        recognizer = ur.PageRecognizerWebKit(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1

    def test_page_path_ie_05(self):
        href = self.page_1_1.title
        basepath = self._getBasePathIE(self.application.selectedPage)
        recognizer = ur.PageRecognizerIE(basepath, self.application)

        result = recognizer.recognize(href)
        assert result == self.page_1_1
