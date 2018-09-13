# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.gui.tester import Tester
from outwiker.gui.pagedialog import createPageWithDialog, editPage
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.basetestcases import BaseOutWikerGUIMixin


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
        Tester.dialogTester.append(self._set_title_func, 'Новая страница')
        Tester.dialogTester.appendError()
        createPageWithDialog(self.application.mainWindow, self.wikiroot)

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot['Новая страница'])

    def test_normal_child(self):
        Tester.dialogTester.append(self._set_title_func, 'Новая страница')
        Tester.dialogTester.appendError()

        parent = WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        createPageWithDialog(self.application.mainWindow, parent)

        self.assertEqual(len(parent), 1)
        self.assertIsNotNone(parent['Новая страница'])

    def test_duplicate_01(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        Tester.dialogTester.append(self._set_title_func, 'Викистраница')
        Tester.dialogTester.appendError()
        createPageWithDialog(self.application.mainWindow, self.wikiroot)

        self.assertEqual(len(self.wikiroot), 2)
        self.assertIsNotNone(self.wikiroot['Викистраница'])

        self.assertIsNotNone(self.wikiroot['Викистраница (1)'])
        self.assertEqual(self.wikiroot['Викистраница (1)'].alias,
                         'Викистраница')

    def test_duplicate_02(self):
        WikiPageFactory().create(self.wikiroot, "Викистраница", [])

        Tester.dialogTester.append(self._set_title_func, 'Викистраница')
        Tester.dialogTester.append(self._set_title_func, 'Викистраница')
        Tester.dialogTester.appendError()
        createPageWithDialog(self.application.mainWindow, self.wikiroot)
        createPageWithDialog(self.application.mainWindow, self.wikiroot)

        self.assertEqual(len(self.wikiroot), 3)
        self.assertIsNotNone(self.wikiroot['Викистраница'])

        self.assertIsNotNone(self.wikiroot['Викистраница (1)'])
        self.assertEqual(self.wikiroot['Викистраница (1)'].alias,
                         'Викистраница')

        self.assertIsNotNone(self.wikiroot['Викистраница (2)'])
        self.assertEqual(self.wikiroot['Викистраница (2)'].alias,
                         'Викистраница')

    def test_space(self):
        Tester.dialogTester.append(self._set_title_func, '  Новая страница  ')
        Tester.dialogTester.appendError()
        createPageWithDialog(self.application.mainWindow, self.wikiroot)

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot['Новая страница'])
        self.assertIsNone(self.wikiroot['Новая страница'].alias)

    def test_invalid_chars_01(self):
        Tester.dialogTester.append(self._set_title_func, 'Страница1 / Страница2')
        Tester.dialogTester.appendError()
        createPageWithDialog(self.application.mainWindow, self.wikiroot)

        self.assertEqual(len(self.wikiroot), 1)
        self.assertIsNotNone(self.wikiroot['Страница1 _ Страница2'])
        self.assertEqual(self.wikiroot['Страница1 _ Страница2'].alias,
                         'Страница1 / Страница2')


class RenamePageWithDialogTest(BasePageDialogTest):
    def test_simple(self):
        page = WikiPageFactory().create(self.wikiroot, 'Викистраница', [])
        Tester.dialogTester.append(self._set_title_func, 'Новое имя')
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page)

        self.assertIsNotNone(self.wikiroot['Новое имя'])
        self.assertIsNone(self.wikiroot['Новое имя'].alias)

    def test_simple_spaces(self):
        page = WikiPageFactory().create(self.wikiroot, 'Викистраница', [])
        Tester.dialogTester.append(self._set_title_func, '    Новое имя    ')
        Tester.dialogTester.appendError()

        editPage(self.application.mainWindow, page)

        self.assertIsNotNone(self.wikiroot['Новое имя'])
        self.assertIsNone(self.wikiroot['Новое имя'].alias)
