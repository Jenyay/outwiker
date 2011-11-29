#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pagetitletester import WindowsPageTitleTester, LinuxPageTitleTester


class PageTitleTesterTest (unittest.TestCase):
    def setUp (self):
        pass

    def tearDown (self):
        pass


    def testValidWin (self):
        title = u"Обычный нормальный заголовок %gg"

        tester = WindowsPageTitleTester()
        self.assertEqual (tester.testForError (title), None)
        self.assertEqual (tester.testForWarning (title), None)


    def testValidLinux (self):
        title = u"Обычный нормальный заголовок %gg"

        tester = LinuxPageTitleTester()
        self.assertEqual (tester.testForError (title), None)
        self.assertEqual (tester.testForWarning (title), None)


    def testDotWin (self):
        title = u" . "
        validResult = u"Invalid Title"

        tester = WindowsPageTitleTester()
        self.assertEqual (tester.testForError (title), validResult)


    def testDotLinux (self):
        title = u" . "
        validResult = u"Invalid Title"

        tester = LinuxPageTitleTester()
        self.assertEqual (tester.testForError (title), validResult)


    def testEmptyTitleWin (self):
        title = u""
        validResult = u"Invalid Title"

        tester = WindowsPageTitleTester()
        self.assertEqual (tester.testForError (title), validResult)


    def testEmptyTitleLinux (self):
        title = u""
        validResult = u"Invalid Title"

        tester = LinuxPageTitleTester()
        self.assertEqual (tester.testForError (title), validResult)


    def testSpaceTitleWin (self):
        title = u"  "
        validResult = u"Invalid Title"

        tester = WindowsPageTitleTester()
        self.assertEqual (tester.testForError (title), validResult)


    def testSpaceTitleLinux (self):
        title = u"  "
        validResult = u"Invalid Title"

        tester = LinuxPageTitleTester()
        self.assertEqual (tester.testForError (title), validResult)


    def testInvalidSymbolsWindows (self):
        invalidCharacters = u'><|?*/\\:"\0'
        validResult = u"The title contains illegal characters"

        template = u"Бла-бла-бла {0} И еще текст"
        tester = WindowsPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertEqual (tester.testForError (title), validResult)


    def testInvalidSymbolsLinux (self):
        invalidCharacters = u'\0\\/'
        validResult = u"The title contains illegal characters"

        template = u"Бла-бла-бла {0} И еще текст"
        tester = LinuxPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertEqual (tester.testForError (title), validResult)


    def testWarningSymbolsLinux (self):
        invalidCharacters = u'><|?*:"'
        validResult = u"The title contains illegal characters for Windows"

        template = u"Бла-бла-бла {0} И еще текст"
        tester = LinuxPageTitleTester()

        for char in invalidCharacters:
            title = template.format (char)
            self.assertEqual (tester.testForWarning (title), validResult)


    def testWarningPercentWindows (self):
        titleList = [u"Заголовок %10 бла-бла-бла",
                u"Заголовок %aa бла-бла-бла",
                u"Заголовок %AA бла-бла-бла",
                u"Заголовок %1f бла-бла-бла",
                u"Заголовок %1F бла-бла-бла"
                ]
        validResult = u"Link to a page with this title is incorrect"

        tester = WindowsPageTitleTester()
        for title in titleList:
            self.assertEqual (tester.testForWarning (title), validResult)


    def testWarningPercentLinux (self):
        titleList = [u"Заголовок %10 бла-бла-бла",
                u"Заголовок %aa бла-бла-бла",
                u"Заголовок %AA бла-бла-бла",
                u"Заголовок %1f бла-бла-бла",
                u"Заголовок %1F бла-бла-бла"
                ]
        validResult = u"Link to a page with this title is incorrect"

        tester = LinuxPageTitleTester()
        for title in titleList:
            self.assertEqual (tester.testForWarning (title), validResult)
