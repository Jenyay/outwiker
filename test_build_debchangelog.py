# -*- coding: UTF-8 -*-

import unittest

from buildtools.contentgenerators import DebChangelogGenerator
from outwiker.core.appinfo import AppInfo, VersionInfo
from outwiker.core.version import Version


class DebChangelogGeneratorTest (unittest.TestCase):
    def setUp(self):
        self._appname = u'OutWiker'
        self._distrib = u'distribname'

    def test_changelog_empty(self):
        maintainer = u'Ivan Petrov'
        maintainer_email = u'petrov@example.com'
        changelog = []
        date_str = u'13.06.2016'

        appinfo = AppInfo(self._appname, None, changelog)
        generator = DebChangelogGenerator(appinfo,
                                          maintainer,
                                          maintainer_email)

        self.assertRaises(ValueError, generator.make, self._distrib, date_str)

    def test_changelog_01(self):
        changes_1 = []
        version_1 = VersionInfo(Version(1, 2, 3, 100),
                                changes=changes_1)

        maintainer = u'Ivan Petrov'
        maintainer_email = u'petrov@example.com'
        changelog = [version_1]
        date_str = u'13.06.2016'

        appinfo = AppInfo(self._appname, None, changelog)
        generator = DebChangelogGenerator(appinfo,
                                          maintainer,
                                          maintainer_email)

        result = generator.make(self._distrib, date_str)

        result_right = u'''outwiker (1.2.3+100~distribname) distribname; urgency=medium

  * 

 -- Ivan Petrov <petrov@example.com>  13.06.2016'''

        self.assertEqual(result, result_right)

    def test_changelog_02(self):
        changes_1 = [u'Изменение 1']
        version_1 = VersionInfo(Version(1, 2, 3, 100),
                                changes=changes_1)

        maintainer = u'Ivan Petrov'
        maintainer_email = u'petrov@example.com'
        changelog = [version_1]
        date_str = u'13.06.2016'

        appinfo = AppInfo(self._appname, None, changelog)
        generator = DebChangelogGenerator(appinfo,
                                          maintainer,
                                          maintainer_email)

        result = generator.make(self._distrib, date_str)

        result_right = u'''outwiker (1.2.3+100~distribname) distribname; urgency=medium

  * Изменение 1

 -- Ivan Petrov <petrov@example.com>  13.06.2016'''

        self.assertEqual(result, result_right)

    def test_changelog_03(self):
        changes_1 = [u'Изменение 1', u'Изменение 2']
        version_1 = VersionInfo(Version(1, 2, 3, 100),
                                changes=changes_1)

        maintainer = u'Ivan Petrov'
        maintainer_email = u'petrov@example.com'
        changelog = [version_1]
        date_str = u'13.06.2016'

        appinfo = AppInfo(self._appname, None, changelog)
        generator = DebChangelogGenerator(appinfo,
                                          maintainer,
                                          maintainer_email)

        result = generator.make(self._distrib, date_str)

        result_right = u'''outwiker (1.2.3+100~distribname) distribname; urgency=medium

  * Изменение 1
  * Изменение 2

 -- Ivan Petrov <petrov@example.com>  13.06.2016'''

        self.assertEqual(result, result_right)


if __name__ == '__main__':
    unittest.main()
