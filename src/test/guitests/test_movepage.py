# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.core.commands import movePage
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.gui.tester import Tester


class MovePageGuiTest (BaseMainWndTest):
    """
    Тесты перемещения страниц
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        factory = TextPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot, "Страница 3", [])
        factory.create (self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create (self.wikiroot["Страница 2"], "Страница 4", [])


    def testCommandMove_01 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        Tester.dialogTester.appendOk()

        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 1"])

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_02 (self):
        Tester.dialogTester.appendOk()

        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 1"])

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_03 (self):
        movePage (self.wikiroot["Страница 1"], self.wikiroot)
        self.assertNotEqual (self.wikiroot["Страница 1"], None)


    def testCommandMove_04 (self):
        Application.wikiroot = self.wikiroot
        Application.selectedPage = self.wikiroot["Страница 1"]

        movePage (self.wikiroot["Страница 1"], self.wikiroot)
        self.assertNotEqual (self.wikiroot["Страница 1"], None)


    def testCommandMove_05 (self):
        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 2"])

        self.assertEqual (self.wikiroot["Страница 1"], None)
        self.assertNotEqual (self.wikiroot["Страница 2/Страница 1"], None)


    def testCommandMove_06 (self):
        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual (self.wikiroot["Страница 1"], None)
        self.assertNotEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)


    def testCommandMove_07 (self):
        Tester.dialogTester.appendOk()

        movePage (self.wikiroot["Страница 3"], self.wikiroot["Страница 2"])

        self.assertNotEqual (self.wikiroot["Страница 3"], None)
        self.assertNotEqual (self.wikiroot["Страница 2/Страница 3"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_08 (self):
        Tester.dialogTester.appendOk()

        movePage (self.wikiroot["Страница 2/Страница 3"], self.wikiroot)

        self.assertNotEqual (self.wikiroot["Страница 3"], None)
        self.assertNotEqual (self.wikiroot["Страница 2/Страница 3"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_09 (self):
        self.assertRaises (AssertionError, movePage, self.wikiroot["Страница 1"], None)
        self.assertRaises (AssertionError, movePage, None, self.wikiroot)


    def testCommandMove_10_readonly (self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot["Страница 2/Страница 3"].readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 2/Страница 3"])

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_11_readonly (self):
        self.wikiroot["Страница 1"].readonly = False
        self.wikiroot["Страница 2/Страница 3"].readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)
        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_12_readonly (self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot["Страница 2/Страница 3"].readonly = False

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot["Страница 1"], self.wikiroot["Страница 2/Страница 3"])

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_13_readonly (self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot.readonly = False

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot["Страница 1"], self.wikiroot)

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_14_readonly (self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot.readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot["Страница 1"], self.wikiroot)

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)


    def testCommandMove_15_readonly (self):
        self.wikiroot["Страница 1"].readonly = False
        self.wikiroot.readonly = True

        Tester.dialogTester.appendOk()
        movePage (self.wikiroot["Страница 1"], self.wikiroot)

        self.assertNotEqual (self.wikiroot["Страница 1"], None)
        self.assertEqual (self.wikiroot["Страница 2/Страница 3/Страница 1"], None)
        self.assertEqual (Tester.dialogTester.count, 0)
