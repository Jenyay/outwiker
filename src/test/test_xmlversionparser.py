# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.xmlversionparser import XmlVersionParser
from outwiker.core.appinfo import AppInfo, AuthorInfo, RequirementsInfo
from outwiker.core.version import Version, StatusSet


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
        self.assertEqual(result.requirements, None)

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

    def test_author_empty(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <author></author>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance (result.author, AuthorInfo))
        self.assertEqual(result.author.name, u'')
        self.assertEqual(result.author.email, u'')
        self.assertEqual(result.author.website, u'')

    def test_author_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <author>
                        <name>Eugeniy Ilin</name>
                        <email>en@example.com</email>
                        <website>http://example.com/en/</website>
                    </author>
                </data>
            </info>'''
        result = XmlVersionParser([u'en']).parse(text)

        self.assertTrue(isinstance (result.author, AuthorInfo))
        self.assertEqual(result.author.name, u'Eugeniy Ilin')
        self.assertEqual(result.author.email, u'en@example.com')
        self.assertEqual(result.author.website, u'http://example.com/en/')

    def test_author_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <author>
                        <name>Eugeniy Ilin</name>
                        <email>en@example.com</email>
                        <website>http://example.com/en/</website>
                    </author>
                </data>

                <data lang="ru">
                    <author>
                        <name>Евгений Ильин</name>
                        <email>ru@example.com</email>
                        <website>http://example.com/ru/</website>
                    </author>
                </data>
            </info>'''
        result = XmlVersionParser([u'en']).parse(text)

        self.assertTrue(isinstance (result.author, AuthorInfo))
        self.assertEqual(result.author.name, u'Eugeniy Ilin')
        self.assertEqual(result.author.email, u'en@example.com')
        self.assertEqual(result.author.website, u'http://example.com/en/')

    def test_author_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <author>
                        <name>Eugeniy Ilin</name>
                        <email>en@example.com</email>
                        <website>http://example.com/en/</website>
                    </author>
                </data>

                <data lang="ru_RU">
                    <author>
                        <name>Евгений Ильин</name>
                        <email>ru@example.com</email>
                        <website>http://example.com/ru/</website>
                    </author>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru_RU']).parse(text)

        self.assertTrue(isinstance (result.author, AuthorInfo))
        self.assertEqual(result.author.name, u'Евгений Ильин')
        self.assertEqual(result.author.email, u'ru@example.com')
        self.assertEqual(result.author.website, u'http://example.com/ru/')

    def test_author_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <author>
                        <name>Eugeniy Ilin</name>
                        <email>en@example.com</email>
                        <website>http://example.com/en/</website>
                    </author>
                </data>

                <data lang="ru_RU">
                    <author>
                        <name>Евгений Ильин</name>
                        <email>ru@example.com</email>
                        <website>http://example.com/ru/</website>
                    </author>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru_RU', u'en']).parse(text)

        self.assertTrue(isinstance (result.author, AuthorInfo))
        self.assertEqual(result.author.name, u'Евгений Ильин')
        self.assertEqual(result.author.email, u'ru@example.com')
        self.assertEqual(result.author.website, u'http://example.com/ru/')

    def test_versions_list_empty(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <changelog></changelog>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(result.versionsList, [])
        self.assertEqual(result.currentVersion, None)

    def test_versions_invalid(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <changelog>
			<version>
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(len (result.versionsList), 0)
        self.assertEqual(result.currentVersion, None)

    def test_versions_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <changelog>
			<version number="1.0">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 0))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 0))

    def test_versions_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <changelog>
			<version number="1.0" status="beta">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 0, status=StatusSet.BETA))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 0, status=StatusSet.BETA))

    def test_versions_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <changelog>
			<version number="1.2.3.4" status="dev">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2, 3, 4, status=StatusSet.DEV))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 2, 3, 4, status=StatusSet.DEV))

    def test_versions_04(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="en">
                    <changelog>
			<version number="1.2"></version>
			<version number="1.1"></version>
			<version number="1.3"></version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertEqual(len (result.versionsList), 3)
        self.assertEqual(result.versionsList[0].version, Version(1, 3))
        self.assertEqual(result.versionsList[1].version, Version(1, 2))
        self.assertEqual(result.versionsList[2].version, Version(1, 1))
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(len (result.versionsList[1].changes), 0)
        self.assertEqual(len (result.versionsList[2].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 3))

    def test_date(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2" date="15 июня 2016">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2))
        self.assertEqual(result.versionsList[0].date_str, u'15 июня 2016')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 2))

    def test_hidden_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2" hidden="true">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, True)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 2))

    def test_hidden_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2" hidden="1">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, True)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 2))

    def test_hidden_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2" hidden="True">
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, True)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.currentVersion, Version(1, 2))

    def test_changes_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2">
                            <change>Изменение 1</change>
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 1)
        self.assertEqual(result.versionsList[0].changes[0], u'Изменение 1')

    def test_changes_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2">
                            <change>Изменение 1</change>
                            <change>Изменение 2</change>
                            <change>Изменение 3</change>
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 2))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 3)
        self.assertEqual(result.versionsList[0].changes[0], u'Изменение 1')
        self.assertEqual(result.versionsList[0].changes[1], u'Изменение 2')
        self.assertEqual(result.versionsList[0].changes[2], u'Изменение 3')

    def test_changes_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.2">
                            <change>Изменение 1</change>
                            <change>Изменение 2</change>
                            <change>Изменение 3</change>
			</version>

			<version number="1.3">
                            <change>Изменение 4</change>
                            <change>Изменение 5</change>
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 2)

        self.assertEqual(result.versionsList[0].version, Version(1, 3))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 2)
        self.assertEqual(result.versionsList[0].changes[0], u'Изменение 4')
        self.assertEqual(result.versionsList[0].changes[1], u'Изменение 5')

        self.assertEqual(result.versionsList[1].version, Version(1, 2))
        self.assertEqual(result.versionsList[1].date_str, u'')
        self.assertEqual(result.versionsList[1].hidden, False)
        self.assertEqual(len (result.versionsList[1].changes), 3)
        self.assertEqual(result.versionsList[1].changes[0], u'Изменение 1')
        self.assertEqual(result.versionsList[1].changes[1], u'Изменение 2')
        self.assertEqual(result.versionsList[1].changes[2], u'Изменение 3')

    def test_downloads_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.0">
                            <download>http://example.com/1.0/</download>
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 0))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.versionsList[0].downloads,
                         {u'all': u'http://example.com/1.0/'})

    def test_downloads_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <data lang="ru">
                    <changelog>
			<version number="1.0">
                            <download os="windows">http://example.com/1.0/windows/</download>
                            <download os="unix">http://example.com/1.0/unix/</download>
			</version>
                    </changelog>
                </data>
            </info>'''
        result = XmlVersionParser([u'ru']).parse(text)

        self.assertEqual(len (result.versionsList), 1)
        self.assertEqual(result.versionsList[0].version, Version(1, 0))
        self.assertEqual(result.versionsList[0].date_str, u'')
        self.assertEqual(result.versionsList[0].hidden, False)
        self.assertEqual(len (result.versionsList[0].changes), 0)
        self.assertEqual(result.versionsList[0].downloads,
                         {u'windows': u'http://example.com/1.0/windows/',
                          u'unix': u'http://example.com/1.0/unix/'
                          })

    def test_requirements_empty(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <requirements>
                </requirements>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result.requirements, RequirementsInfo))
        self.assertEqual(result.requirements.os, [])
        self.assertEqual(result.requirements.outwiker_version, None)

    def test_requirements_version_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <requirements>
                    <outwiker>2.0</outwiker>
                </requirements>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result.requirements, RequirementsInfo))
        self.assertEqual(result.requirements.os, [])
        self.assertEqual(result.requirements.outwiker_version, Version(2, 0))

    def test_requirements_version_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <requirements>
                    <outwiker>2.0 dev</outwiker>
                </requirements>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result.requirements, RequirementsInfo))
        self.assertEqual(result.requirements.os, [])
        self.assertEqual(result.requirements.outwiker_version, Version(2, 0, status=StatusSet.DEV))

    def test_requirements_os_01(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <requirements>
                    <os>Linux</os>
                </requirements>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result.requirements, RequirementsInfo))
        self.assertEqual(result.requirements.os, [u'Linux'])
        self.assertEqual(result.requirements.outwiker_version, None)

    def test_requirements_os_02(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <requirements>
                    <os>Linux, Windows</os>
                </requirements>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result.requirements, RequirementsInfo))
        self.assertEqual(result.requirements.os, [u'Linux', 'Windows'])
        self.assertEqual(result.requirements.outwiker_version, None)

    def test_requirements_os_03(self):
        text = u'''<?xml version="1.1" encoding="UTF-8" ?>
            <info>
                <requirements>
                    <os></os>
                </requirements>
            </info>'''
        result = XmlVersionParser().parse(text)

        self.assertTrue(isinstance(result.requirements, RequirementsInfo))
        self.assertEqual(result.requirements.os, [])
        self.assertEqual(result.requirements.outwiker_version, None)
