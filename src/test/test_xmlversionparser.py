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
        self.assertEqual(result.updatesUrl, u"")

    def test_empty_02(self):
        text = u'<?xml version="1.1" encoding="UTF-8" ?>'
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result, AppInfo))
        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

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
        self.assertEqual(result.updatesUrl, u"")

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
        self.assertEqual(result.updatesUrl, u"")

    def test_name_only(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
<info><name>Имя приложения</name></info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"Имя приложения")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_updates_url_only(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info><updates>http://example.com/updates.xml</updates></info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"http://example.com/updates.xml")

    def test_empty_updates_url_only(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info><updates></updates></info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_description_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en"><description>My plugin</description></data>
            </info>'''
        result = XmlVersionParser([u'ru_RU', u'en']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"My plugin")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_description_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en"><description>My plugin</description></data>
                <data lang="ru_RU"><description>Описание плагина</description></data>
            </info>'''
        result = XmlVersionParser([u'ru_RU', u'en']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"Описание плагина")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_description_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru_RU"><description>Описание плагина</description></data>
            </info>'''
        result = XmlVersionParser([u'en']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_description_04(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en"><description>My plugin</description></data>
                <data lang="ru_RU"><description>Описание плагина</description></data>
            </info>'''
        result = XmlVersionParser([u'en', u'ru_RU']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"My plugin")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_website_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en"><website>http://example.com/en/</website></data>
            </info>'''
        result = XmlVersionParser([u'ru_RU', u'en']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"http://example.com/en/")
        self.assertEqual(result.updatesUrl, u"")

    def test_website_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en"><website>http://example.com/en/</website></data>
                <data lang="ru_RU"><website>http://example.com/ru/</website></data>
            </info>'''
        result = XmlVersionParser([u'ru_RU', u'en']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"http://example.com/ru/")
        self.assertEqual(result.updatesUrl, u"")

    def test_website_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru_RU"><website>http://example.com/ru/</website></data>
            </info>'''
        result = XmlVersionParser([u'en']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"")
        self.assertEqual(result.updatesUrl, u"")

    def test_website_04(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en"><website>http://example.com/en/</website></data>
                <data lang="ru_RU"><website>http://example.com/ru/</website></data>
            </info>'''
        result = XmlVersionParser([u'en', u'ru_RU']).parse(text)

        self.assertEqual(result.author, None)
        self.assertEqual(result.appname, u"")
        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.description, u"")
        self.assertEqual(result.appwebsite, u"http://example.com/en/")
        self.assertEqual(result.updatesUrl, u"")
