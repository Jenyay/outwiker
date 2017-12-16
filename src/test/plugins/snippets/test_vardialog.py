# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from test.guitests.basemainwnd import BaseMainWndTest


class SnippetsVarDialogTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)
        mainWnd = Application.mainWindow
        plugins_dir = ["../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(plugins_dir)

        from snippets.gui.variablesdialog import VariablesDialog
        self._dialog = VariablesDialog(mainWnd)

    def tearDown(self):
        self._dialog.Destroy()
        self.loader.clear()
        BaseMainWndTest.tearDown(self)

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
