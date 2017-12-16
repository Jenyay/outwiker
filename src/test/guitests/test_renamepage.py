# -*- coding: UTF-8 -*-

from os.path import basename

from .basemainwnd import BaseMainWndTest
from outwiker.core.commands import renamePage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester


class RenamePageGuiTest (BaseMainWndTest):
    """
    Тесты переименования страниц
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        factory = TextPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot["Страница 2"], "Страница 3", [])


    def testCommand_01 (self):
        renamePage (self.wikiroot["Страница 1"], "Абырвалг")

        self.assertIsNone (self.wikiroot["Страница 1"])
        self.assertIsNotNone (self.wikiroot["Абырвалг"])


    def testCommand_02 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "Страница 2")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNotNone (self.wikiroot["Страница 2"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_03 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "safsd/Абырвалг")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_04 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_05 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "    \t\n")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_06 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "__asdasdf")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNone (self.wikiroot["__asdasdf"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_07_readonly (self):
        self.wikiroot["Страница 1"].readonly = True

        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "Абырвалг")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNone (self.wikiroot["Абырвалг"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_08 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "..")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNone (self.wikiroot[".."])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_09 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "..\\")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNone (self.wikiroot["..\\"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_10 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "../sadfasdf")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNone (self.wikiroot["../sadfasdf"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_11 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 1"], "..\\Абырвалг")

        self.assertIsNotNone (self.wikiroot["Страница 1"])
        self.assertIsNone (self.wikiroot["..\\Абырвалг"])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_12 (self):
        renamePage (self.wikiroot["Страница 2/Страница 3"], "Абырвалг")

        self.assertIsNone (self.wikiroot["Страница 2/Страница 3"])
        self.assertIsNotNone (self.wikiroot["Страница 2"])
        self.assertIsNotNone (self.wikiroot["Страница 2/Абырвалг"])


    def testCommand_13 (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot["Страница 2/Страница 3"], "..")

        self.assertIsNotNone (self.wikiroot["Страница 2/Страница 3"])
        self.assertIsNone (self.wikiroot[".."])
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommand_14_root (self):
        Tester.dialogTester.appendOk()
        renamePage (self.wikiroot, "Абырвалг")

        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertEqual (self.wikiroot.title, basename (self.path))
