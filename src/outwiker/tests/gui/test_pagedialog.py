# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.app.gui.pagedialog import createPageWithDialog, editPage
from outwiker.gui.tester import Tester
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class BasePageDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.application.wikiroot = self.wikiroot
        Tester.dialogTester.clear()

    def tearDown(self):
        Tester.dialogTester.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _set_title_func(self, dialog, title):
        dialog.getPanel(0).pageTitle = title
        return wx.ID_OK


class CreatePageWithDialogTest(BasePageDialogTest):
    def test_normal_root(self):
        Tester.dialogTester.append(self._set_title_func, "Новая страница")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["Новая страница"])

    def test_normal_child(self):
        Tester.dialogTester.append(self._set_title_func, "Новая страница")
        Tester.dialogTester.appendError()

        parent = WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        createPageWithDialog(self.application.mainWindow, parent, self.application)

        self.assertEqual(len(parent), 1)
        self.assertIsNotNone(parent["Новая страница"])

    def test_duplicate_01(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        Tester.dialogTester.append(self._set_title_func, "Викистраница")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 2)
        self.assertIsNotNone(self.wikiroot["Викистраница"])

        self.assertIsNotNone(self.wikiroot["Викистраница (1)"])
        self.assertEqual(self.wikiroot["Викистраница (1)"].alias, "Викистраница")

    def test_duplicate_02(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        Tester.dialogTester.append(self._set_title_func, "Викистраница")
        Tester.dialogTester.append(self._set_title_func, "Викистраница")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 3)
        self.assertIsNotNone(self.wikiroot["Викистраница"])

        self.assertIsNotNone(self.wikiroot["Викистраница (1)"])
        self.assertEqual(self.wikiroot["Викистраница (1)"].alias, "Викистраница")

        self.assertIsNotNone(self.wikiroot["Викистраница (2)"])
        self.assertEqual(self.wikiroot["Викистраница (2)"].alias, "Викистраница")

    def test_duplicate_03(self):
        WikiPageFactory().create(self.wikiroot, "(1)", [])

        Tester.dialogTester.append(self._set_title_func, ".")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 2)
        self.assertIsNotNone(self.wikiroot["(2)"])

        self.assertEqual(self.wikiroot["(2)"].alias, ".")

    def test_space(self):
        Tester.dialogTester.append(self._set_title_func, "  Новая страница  ")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["Новая страница"])
        self.assertIsNone(self.wikiroot["Новая страница"].alias)

    def test_invalid_chars_01(self):
        Tester.dialogTester.append(self._set_title_func, "Страница1 / Страница2")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["Страница1 _ Страница2"])
        self.assertEqual(
            self.wikiroot["Страница1 _ Страница2"].alias, "Страница1 / Страница2"
        )

    def test_double_dots(self):
        Tester.dialogTester.append(self._set_title_func, "..")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["(1)"])
        self.assertEqual(self.wikiroot["(1)"].alias, "..")

    def test_dot(self):
        Tester.dialogTester.append(self._set_title_func, ".")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["(1)"])
        self.assertEqual(self.wikiroot["(1)"].alias, ".")

    def test_dots_01(self):
        Tester.dialogTester.append(self._set_title_func, "...")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["(1)"])
        self.assertEqual(self.wikiroot["(1)"].alias, "...")

    def test_dots_02(self):
        Tester.dialogTester.append(self._set_title_func, "../.")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["..__"])
        self.assertEqual(self.wikiroot["..__"].alias, "../.")

    def test_double_underline(self):
        Tester.dialogTester.append(self._set_title_func, "__attach")
        Tester.dialogTester.appendError()
        createPageWithDialog(
            self.application.mainWindow, self.wikiroot, self.application
        )

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot["--attach"])
        self.assertEqual(self.wikiroot["--attach"].alias, "__attach")


class RenamePageWithDialogTest(BasePageDialogTest):
    def test_simple(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "Новое имя")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertEqual(page.title, "Новое имя")
        self.assertEqual(page.display_title, "Новое имя")
        self.assertIsNotNone(self.wikiroot["Новое имя"])
        self.assertIsNone(self.wikiroot["Новое имя"].alias)

    def test_simple_spaces(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "    Новое имя    ")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertEqual(page.title, "Новое имя")
        self.assertEqual(page.display_title, "Новое имя")
        self.assertIsNotNone(self.wikiroot["Новое имя"])
        self.assertIsNone(self.wikiroot["Новое имя"].alias)

    def test_some_name(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "Викистраница")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertEqual(page.title, "Викистраница")
        self.assertEqual(page.display_title, "Викистраница")
        self.assertIsNotNone(self.wikiroot["Викистраница"])
        self.assertIsNone(self.wikiroot["Викистраница"].alias)

    def test_some_name_spaces(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "   Викистраница   ")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertEqual(page.title, "Викистраница")
        self.assertEqual(page.display_title, "Викистраница")
        self.assertIsNotNone(self.wikiroot["Викистраница"])
        self.assertIsNone(self.wikiroot["Викистраница"].alias)

    def test_special_chars(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, 'Тест ><|?*:"\\/#% проверка')
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertEqual(page.title, "Тест ___________ проверка")
        self.assertEqual(page.display_title, 'Тест ><|?*:"\\/#% проверка')
        self.assertEqual(page.alias, 'Тест ><|?*:"\\/#% проверка')
        self.assertIsNotNone(self.wikiroot["Тест ___________ проверка"])

    def test_rename_duplicate_01(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        page2 = WikiPageFactory().create(self.wikiroot, "Викистраница - 2", [])
        Tester.dialogTester.append(self._set_title_func, "Викистраница")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page2, self.application)

        self.assertEqual(page2.title, "Викистраница (1)")
        self.assertEqual(page2.alias, "Викистраница")
        self.assertEqual(page2.display_title, "Викистраница")
        self.assertIsNotNone(self.wikiroot["Викистраница (1)"])

    def test_rename_duplicate_02(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        WikiPageFactory().create(self.wikiroot, "Викистраница (1)", [])

        page3 = WikiPageFactory().create(self.wikiroot, "Викистраница - 3", [])
        Tester.dialogTester.append(self._set_title_func, "Викистраница")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page3, self.application)

        self.assertEqual(page3.title, "Викистраница (2)")
        self.assertEqual(page3.alias, "Викистраница")
        self.assertEqual(page3.display_title, "Викистраница")
        self.assertIsNotNone(self.wikiroot["Викистраница (2)"])

    def test_begin_underlines(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "__Викистраница")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertIsNone(self.wikiroot["Викистраница"])
        self.assertEqual(page.title, "--Викистраница")
        self.assertEqual(page.display_title, "__Викистраница")
        self.assertIsNotNone(self.wikiroot["--Викистраница"])
        self.assertEqual(self.wikiroot["--Викистраница"].alias, "__Викистраница")

    def test_begin_special_chars_underlines(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "##Викистраница")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertIsNone(self.wikiroot["Викистраница"])
        self.assertEqual(page.title, "--Викистраница")
        self.assertEqual(page.display_title, "##Викистраница")
        self.assertIsNotNone(self.wikiroot["--Викистраница"])
        self.assertEqual(self.wikiroot["--Викистраница"].alias, "##Викистраница")

    def test_dots(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, "..")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertIsNone(self.wikiroot["Викистраница"])
        self.assertEqual(page.title, "(1)")
        self.assertEqual(page.display_title, "..")
        self.assertIsNotNone(self.wikiroot["(1)"])
        self.assertEqual(self.wikiroot["(1)"].alias, "..")

    def test_dot(self):
        page = WikiPageFactory().create(self.wikiroot, "Викистраница", [])
        Tester.dialogTester.append(self._set_title_func, ".")
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page, self.application)

        self.assertIsNone(self.wikiroot["Викистраница"])
        self.assertEqual(page.title, "(1)")
        self.assertEqual(page.display_title, ".")
        self.assertIsNotNone(self.wikiroot["(1)"])
        self.assertEqual(self.wikiroot["(1)"].alias, ".")
