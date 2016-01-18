# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester, PageTitleError, PageTitleWarning


class PageTitleTesterTest (unittest.TestCase):
    def testValidWin (self):
        title = u"Обычный нормальный заголовок %gg"

        tester = WindowsPageTitleTester()
        tester.test (title)


    def testValidLinux (self):
        title = u"Обычный нормальный заголовок %gg"

        tester = LinuxPageTitleTester()
        tester.test (title)


    def testDotWin (self):
        title = u" . "

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testDotLinux (self):
        title = u" . "

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testEmptyTitleWin (self):
        title = u""

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testEmptyTitleLinux (self):
        title = u""

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testSpaceTitleWin (self):
        title = u"  "

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testSpaceTitleLinux (self):
        title = u"  "

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testInvalidSymbolsWindows (self):
        invalidCharacters = u'><|?*/\\:"\0'

        template = u"Бла-бла-бла {0} И еще текст"
        tester = WindowsPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertRaises (PageTitleError, tester.test, title)


    def testInvalidSymbolsLinux (self):
        invalidCharacters = u'\0\\/'

        template = u"Бла-бла-бла {0} И еще текст"
        tester = LinuxPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertRaises (PageTitleError, tester.test, title)


    def testWarningSymbolsLinux (self):
        invalidCharacters = u'><|?*:"'

        template = u"Бла-бла-бла {0} И еще текст"
        tester = LinuxPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertRaises (PageTitleWarning, tester.test, title)


    def testWarningPercentWindows (self):
        titleList = [u"Заголовок %10 бла-бла-бла",
                     u"Заголовок %aa бла-бла-бла",
                     u"Заголовок %AA бла-бла-бла",
                     u"Заголовок %1f бла-бла-бла",
                     u"Заголовок %1F бла-бла-бла"
                     ]

        tester = WindowsPageTitleTester()
        for title in titleList:
            self.assertRaises (PageTitleWarning, tester.test, title)


    def testWarningPercentLinux (self):
        titleList = [u"Заголовок %10 бла-бла-бла",
                     u"Заголовок %aa бла-бла-бла",
                     u"Заголовок %AA бла-бла-бла",
                     u"Заголовок %1f бла-бла-бла",
                     u"Заголовок %1F бла-бла-бла"
                     ]

        tester = LinuxPageTitleTester()
        for title in titleList:
            self.assertRaises (PageTitleWarning, tester.test, title)


    def testUnderlineLinux (self):
        title = u"__Заголовок с подчеркиванием"

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)



    def testUnderlineWindows (self):
        title = u"__Заголовок с подчеркиванием"

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testReplace_01 (self):
        title = u'А>б<ы|р?в\\а:л"г*Абырвалг'
        tester = WindowsPageTitleTester()

        result = tester.replaceDangerousSymbols (title, u'_')
        self.assertEqual (result, u'А_б_ы_р_в_а_л_г_Абырвалг')


    def testReplace_02 (self):
        title = u'Абырвалг%aa%12%1a%a1Абырвалг'
        tester = WindowsPageTitleTester()

        result = tester.replaceDangerousSymbols (title, u'_')
        self.assertEqual (result, u'Абырвалг____Абырвалг')
