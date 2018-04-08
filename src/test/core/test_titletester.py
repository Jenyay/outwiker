# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester, PageTitleError, PageTitleWarning


class PageTitleTesterTest (unittest.TestCase):
    def testValidWin (self):
        title = "Обычный нормальный заголовок %gg"

        tester = WindowsPageTitleTester()
        tester.test (title)


    def testValidLinux (self):
        title = "Обычный нормальный заголовок %gg"

        tester = LinuxPageTitleTester()
        tester.test (title)


    def testDotWin (self):
        title = " . "

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testDotLinux (self):
        title = " . "

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testEmptyTitleWin (self):
        title = ""

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testEmptyTitleLinux (self):
        title = ""

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testSpaceTitleWin (self):
        title = "  "

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testSpaceTitleLinux (self):
        title = "  "

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testInvalidSymbolsWindows (self):
        invalidCharacters = '><|?*/\\:"\0'

        template = "Бла-бла-бла {0} И еще текст"
        tester = WindowsPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertRaises (PageTitleError, tester.test, title)


    def testInvalidSymbolsLinux (self):
        invalidCharacters = '\0\\/'

        template = "Бла-бла-бла {0} И еще текст"
        tester = LinuxPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertRaises (PageTitleError, tester.test, title)


    def testWarningSymbolsLinux (self):
        invalidCharacters = '><|?*:"'

        template = "Бла-бла-бла {0} И еще текст"
        tester = LinuxPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertRaises (PageTitleWarning, tester.test, title)


    def testWarningPercentWindows (self):
        titleList = ["Заголовок %10 бла-бла-бла",
                     "Заголовок %aa бла-бла-бла",
                     "Заголовок %AA бла-бла-бла",
                     "Заголовок %1f бла-бла-бла",
                     "Заголовок %1F бла-бла-бла"
                     ]

        tester = WindowsPageTitleTester()
        for title in titleList:
            self.assertRaises (PageTitleWarning, tester.test, title)


    def testWarningPercentLinux (self):
        titleList = ["Заголовок %10 бла-бла-бла",
                     "Заголовок %aa бла-бла-бла",
                     "Заголовок %AA бла-бла-бла",
                     "Заголовок %1f бла-бла-бла",
                     "Заголовок %1F бла-бла-бла"
                     ]

        tester = LinuxPageTitleTester()
        for title in titleList:
            self.assertRaises (PageTitleWarning, tester.test, title)


    def testUnderlineLinux (self):
        title = "__Заголовок с подчеркиванием"

        tester = LinuxPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)



    def testUnderlineWindows (self):
        title = "__Заголовок с подчеркиванием"

        tester = WindowsPageTitleTester()
        self.assertRaises (PageTitleError, tester.test, title)


    def testReplace_01 (self):
        title = 'А>б<ы|р?в\\а:л"г*А/бырвалг'
        tester = WindowsPageTitleTester()

        result = tester.replaceDangerousSymbols (title, '_')
        self.assertEqual (result, 'А_б_ы_р_в_а_л_г_А_бырвалг')


    def testReplace_02 (self):
        title = 'Абырвалг%aa%12%1a%a1Абырвалг'
        tester = WindowsPageTitleTester()

        result = tester.replaceDangerousSymbols (title, '_')
        self.assertEqual (result, 'Абырвалг____Абырвалг')
