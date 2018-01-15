# -*- coding: utf-8 -*-

import unittest

from buildtools.contentgenerators import SiteChangelogGenerator
from outwiker.core.appinfo import AppInfo, VersionInfo
from outwiker.core.version import Version


class ChangelogContentTest (unittest.TestCase):
    def setUp(self):
        self._appname = u'Test'
        self._author = None

    def test_changelog_None(self):
        appinfo = None
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()
        self.assertEqual(changelog, u'')

    def test_changelog_empty(self):
        changelog = []
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()
        self.assertEqual(changelog, u'')

    def test_changelog_single_01(self):
        version_1 = VersionInfo(Version(1))
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1'''

        self.assertEqual(changelog, right_result)

    def test_changelog_single_02(self):
        version_1 = VersionInfo(Version(1, 0))
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_03(self):
        version_1 = VersionInfo(Version.parse(u'1.2.3 beta'))
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.2.3 beta'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_date(self):
        version_1 = VersionInfo(Version.parse(u'1.2.3 beta'),
                                date_str=u'13.06.2016')
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.2.3 beta (13.06.2016)'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_changes_01(self):
        changes = [u'Первая версия.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes)
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0

* Первая версия.'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_changes_02(self):
        changes = [u'Исправление ошибок.',
                   u'Добавлена новая возможность.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes)
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0

* Исправление ошибок.
* Добавлена новая возможность.'''
        self.assertEqual(changelog, right_result)

    def test_changelog_single_changes_date(self):
        changes = [u'Исправление ошибок.',
                   u'Добавлена новая возможность.']
        version_1 = VersionInfo(Version(1, 0),
                                date_str=u'1 мая 2016',
                                changes=changes)
        changelog = [version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.0 (1 мая 2016)

* Исправление ошибок.
* Добавлена новая возможность.'''
        self.assertEqual(changelog, right_result)

    def test_changelog_versions_01(self):
        changes_1 = [u'Первая версия.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes_1)

        changes_2 = [u'Исправление ошибок.',
                     u'Добавлена новая возможность.']
        version_2 = VersionInfo(Version(1, 1),
                                changes=changes_2)
        changelog = [version_1, version_2]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.1

* Исправление ошибок.
* Добавлена новая возможность.


!!!! 1.0

* Первая версия.'''
        self.assertEqual(changelog, right_result, changelog)

    def test_changelog_versions_02(self):
        changes_1 = [u'Первая версия.']
        version_1 = VersionInfo(Version(1, 0),
                                changes=changes_1)

        changes_2 = [u'Исправление ошибок.',
                     u'Добавлена новая возможность.']
        version_2 = VersionInfo(Version(1, 1),
                                changes=changes_2)
        changelog = [version_2, version_1]
        appinfo = AppInfo(self._appname, self._author, changelog)
        generator = SiteChangelogGenerator(appinfo)
        changelog = generator.make()

        right_result = u'''!!!! 1.1

* Исправление ошибок.
* Добавлена новая возможность.


!!!! 1.0

* Первая версия.'''
        self.assertEqual(changelog, right_result, changelog)


if __name__ == '__main__':
    unittest.main()
