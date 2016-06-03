# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.core.appinfo import AppInfo


class XmlVersionParserTest (unittest.TestCase):
    def test_empty_01(self):
        text = u""
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result, AppInfo))
        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")

    def test_empty_02(self):
        text = u'<?xml version="1.1" encoding="UTF-8" ?>'
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result, AppInfo))
        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")

    def test_empty_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
<info></info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result, AppInfo))
        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")

    def test_empty_name(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
<info><name></name></info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result, AppInfo))
        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")

    def test_name_only(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
<info><name>Имя приложения</name></info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"Имя приложения")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
