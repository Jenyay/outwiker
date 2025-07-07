# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class SnippetsVarDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        mainWnd = self.application.mainWindow
        plugins_dir = ["plugins/snippets"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(plugins_dir)

        from snippets.gui.variablesdialog import VariablesDialog
        self._dialog = VariablesDialog(mainWnd, self.application)

    def tearDown(self):
        self._dialog.Destroy()
        self.loader.clear()
        self.destroyApplication()

    def test_empty(self):
        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {})

    def test_single_empty(self):
        self._dialog.addStringVariable('test')
        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {'test': ''})

    def test_single(self):
        self._dialog.addStringVariable('test')
        self._dialog.setStringVariable('test', 'Проверка')

        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {'test': 'Проверка'})

    def test_two_items(self):
        self._dialog.addStringVariable('test_1')
        self._dialog.addStringVariable('test_2')

        self._dialog.setStringVariable('test_1', 'Проверка_1')
        self._dialog.setStringVariable('test_2', 'Проверка_2')

        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {'test_1': 'Проверка_1',
                                     'test_2': 'Проверка_2'})

    def test_no_item(self):
        self.assertRaises(KeyError,
                          self._dialog.setStringVariable,
                          'test',
                          'test')
