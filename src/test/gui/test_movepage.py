# -*- coding: utf-8 -*-

import unittest

from outwiker.core.commands import movePage
from outwiker.pages.text.textpage import TextPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class MovePageGuiTest(unittest.TestCase, BaseOutWikerGUIMixin):
    """
    Тесты перемещения страниц
    """
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot, "Страница 3", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 4", [])

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_error_move_to_self_current(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        self.application.mainWindow.toaster.counter.clear()

        movePage(self.wikiroot["Страница 1"], self.wikiroot["Страница 1"])

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def test_error_move_to_self(self):
        self.application.mainWindow.toaster.counter.clear()

        movePage(self.wikiroot["Страница 1"], self.wikiroot["Страница 1"])

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_03(self):
        movePage(self.wikiroot["Страница 1"], self.wikiroot)
        self.assertNotEqual(self.wikiroot["Страница 1"], None)

    def testCommandMove_04(self):
        self.application.wikiroot = self.wikiroot
        self.application.selectedPage = self.wikiroot["Страница 1"]

        movePage(self.wikiroot["Страница 1"], self.wikiroot)
        self.assertNotEqual(self.wikiroot["Страница 1"], None)

    def testCommandMove_05(self):
        movePage(self.wikiroot["Страница 1"], self.wikiroot["Страница 2"])

        self.assertEqual(self.wikiroot["Страница 1"], None)
        self.assertNotEqual(self.wikiroot["Страница 2/Страница 1"], None)

    def testCommandMove_06(self):
        movePage(self.wikiroot["Страница 1"],
                 self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(self.wikiroot["Страница 1"], None)
        self.assertNotEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                            None)

    def test_error_move_to_child(self):
        self.application.mainWindow.toaster.counter.clear()

        movePage(self.wikiroot["Страница 3"], self.wikiroot["Страница 2"])

        self.assertNotEqual(self.wikiroot["Страница 3"], None)
        self.assertNotEqual(self.wikiroot["Страница 2/Страница 3"], None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def test_error_duplicate_title(self):
        self.application.mainWindow.toaster.counter.clear()

        movePage(self.wikiroot["Страница 2/Страница 3"], self.wikiroot)

        self.assertNotEqual(self.wikiroot["Страница 3"], None)
        self.assertNotEqual(self.wikiroot["Страница 2/Страница 3"], None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_09(self):
        self.assertRaises(AssertionError,
                          movePage, self.wikiroot["Страница 1"], None)
        self.assertRaises(AssertionError, movePage, None, self.wikiroot)

    def testCommandMove_10_readonly(self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot["Страница 2/Страница 3"].readonly = True

        self.application.mainWindow.toaster.counter.clear()
        movePage(self.wikiroot["Страница 1"],
                 self.wikiroot["Страница 2/Страница 3"])

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                         None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_11_readonly(self):
        self.wikiroot["Страница 1"].readonly = False
        self.wikiroot["Страница 2/Страница 3"].readonly = True

        self.application.mainWindow.toaster.counter.clear()
        movePage(self.wikiroot["Страница 1"],
                 self.wikiroot["Страница 2/Страница 3"])

        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                         None)
        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_12_readonly(self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot["Страница 2/Страница 3"].readonly = False

        self.application.mainWindow.toaster.counter.clear()
        movePage(self.wikiroot["Страница 1"],
                 self.wikiroot["Страница 2/Страница 3"])

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                         None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_13_readonly(self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot.readonly = False

        self.application.mainWindow.toaster.counter.clear()
        movePage(self.wikiroot["Страница 1"], self.wikiroot)

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                         None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_14_readonly(self):
        self.wikiroot["Страница 1"].readonly = True
        self.wikiroot.readonly = True

        self.application.mainWindow.toaster.counter.clear()
        movePage(self.wikiroot["Страница 1"], self.wikiroot)

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                         None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)

    def testCommandMove_15_readonly(self):
        self.wikiroot["Страница 1"].readonly = False
        self.wikiroot.readonly = True

        self.application.mainWindow.toaster.counter.clear()
        movePage(self.wikiroot["Страница 1"], self.wikiroot)

        self.assertNotEqual(self.wikiroot["Страница 1"], None)
        self.assertEqual(self.wikiroot["Страница 2/Страница 3/Страница 1"],
                         None)
        self.assertEqual(
            self.application.mainWindow.toaster.counter.showErrorCount,
            1)
