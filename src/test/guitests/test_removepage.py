# -*- coding: utf-8 -*-

import wx

from outwiker.actions.removepage import RemovePageAction
from outwiker.core.commands import removePage
from outwiker.gui.tester import Tester
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUITest


class RemovePageGuiTest(BaseOutWikerGUITest):
    """
    Тесты удаления страниц через интерфейс
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testCommandRemove_01(self):
        Tester.dialogTester.appendNo()

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        removePage(self.wikiroot["Страница 1"])

        self.assertNotEqual(self.wikiroot["Страница 1"], None)

    def testCommandRemove_02(self):
        Tester.dialogTester.appendYes()

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        removePage(self.wikiroot["Страница 1"])

        self.assertEqual(self.wikiroot["Страница 1"], None)

    def testCommandRemove_03(self):
        Tester.dialogTester.appendYes()

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        removePage(self.wikiroot["Страница 1"])

        self.assertEqual(self.wikiroot["Страница 1"], None)

    def testCommandRemove_04(self):
        Tester.dialogTester.appendYes()

        removePage(self.wikiroot["Страница 1"])

        self.assertEqual(self.wikiroot["Страница 1"], None)

    def testCommandRemove_05_ReadOnly(self):
        Tester.dialogTester.appendOk()
        self.wikiroot["Страница 1"].readonly = True

        removePage(self.wikiroot["Страница 1"])

        self.assertNotEqual(self.wikiroot["Страница 1"], None)

    def testCommandRemove_06(self):
        Tester.dialogTester.appendYes()

        removePage(self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(self.wikiroot["Страница 2/Страница 3"], None)
        self.assertNotEqual(self.wikiroot["Страница 2"], None)

    def testCommandRemove_08_root(self):
        Tester.dialogTester.appendYes()
        removePage(self.wikiroot)
        self.assertEqual(Tester.dialogTester.count, 0)

    def testCommandRemove_07_IOError(self):
        def removeBeforeRemove(dialog):
            self.wikiroot["Страница 2/Страница 3"].remove()
            # Для сообщения об ошибке удаления
            Tester.dialogTester.appendOk()
            return wx.YES

        Tester.dialogTester.append(removeBeforeRemove)

        removePage(self.wikiroot["Страница 2/Страница 3"])

        # Убедимся, что были показаны все сообщения
        self.assertEqual(Tester.dialogTester.count, 0)

    def testActionRemovePage_01(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = None

        self.application.actionController.getAction(RemovePageAction.stringId).run(None)

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertNotEqual(self.wikiroot["Страница 2"], None)

    def testActionRemovePage_02(self):
        Tester.dialogTester.appendYes()

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.actionController.getAction(RemovePageAction.stringId).run(None)

        self.assertEqual(self.wikiroot["Страница 1"], None)
        self.assertNotEqual(self.wikiroot["Страница 2"], None)

    def testActionRemovePage_03(self):
        Tester.dialogTester.appendYes()

        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 2/Страница 3"]

        self.application.actionController.getAction(RemovePageAction.stringId).run(None)

        self.assertEqual(self.wikiroot["Страница 2/Страница 3"], None)
        self.assertNotEqual(self.wikiroot["Страница 2"], None)
