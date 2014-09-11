# -*- coding: UTF-8 -*-

import wx

from basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.commands import removePage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeWiki
from outwiker.actions.removepage import RemovePageAction


class RemovePageGuiTest (BaseMainWndTest):
    """
    Тесты окна со списком прикрепленных файлов
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])
        factory.create (self.wikiroot[u"Страница 2"], u"Страница 3", [])

        Tester.dialogTester.clear()


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.selectedPage = None
        Application.wikiroot = None
        removeWiki (self.path)


    def testCommandRemove_01 (self):
        Tester.dialogTester.appendNo()

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        removePage (self.wikiroot[u"Страница 1"])

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandRemove_02 (self):
        Tester.dialogTester.appendYes()

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        removePage (self.wikiroot[u"Страница 1"])

        self.assertEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandRemove_03 (self):
        Tester.dialogTester.appendYes()

        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        removePage (self.wikiroot[u"Страница 1"])

        self.assertEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandRemove_04 (self):
        Tester.dialogTester.appendYes()

        removePage (self.wikiroot[u"Страница 1"])

        self.assertEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandRemove_05_ReadOnly (self):
        Tester.dialogTester.appendOk()
        self.wikiroot[u"Страница 1"].readonly = True

        removePage (self.wikiroot[u"Страница 1"])

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)


    def testCommandRemove_06 (self):
        Tester.dialogTester.appendYes()

        removePage (self.wikiroot[u"Страница 2/Страница 3"])

        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2"], None)


    def testCommandRemove_07_IOError (self):
        def removeBeforeRemove (dialog):
            self.wikiroot[u"Страница 2/Страница 3"].remove()
            # Для сообщения об ошибке удаления
            Tester.dialogTester.appendOk()
            return wx.YES

        Tester.dialogTester.append (removeBeforeRemove)

        removePage (self.wikiroot[u"Страница 2/Страница 3"])

        # Убедимся, что были показаны все сообщения
        self.assertEqual (Tester.dialogTester.count, 0)


    def testActionRemovePage_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = None

        Application.actionController.getAction (RemovePageAction.stringId).run (None)

        self.assertNotEqual (self.wikiroot[u"Страница 1"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2"], None)


    def testActionRemovePage_02 (self):
        Tester.dialogTester.appendYes()

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 1"]

        Application.actionController.getAction (RemovePageAction.stringId).run (None)

        self.assertEqual (self.wikiroot[u"Страница 1"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2"], None)


    def testActionRemovePage_03 (self):
        Tester.dialogTester.appendYes()

        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot[u"Страница 2/Страница 3"]

        Application.actionController.getAction (RemovePageAction.stringId).run (None)

        self.assertEqual (self.wikiroot[u"Страница 2/Страница 3"], None)
        self.assertNotEqual (self.wikiroot[u"Страница 2"], None)
