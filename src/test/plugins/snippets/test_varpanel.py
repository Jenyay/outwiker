# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from test.guitests.basemainwnd import BaseMainWndTest


class SnippetsVarPanelTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)
        mainWnd = Application.mainWindow
        plugins_dir = ["../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(plugins_dir)

        from snippets.gui.variablesdialog import VaraiblesPanel
        self._panel = VaraiblesPanel(mainWnd)

    def tearDown(self):
        self.loader.clear()
        BaseMainWndTest.tearDown(self)

    def test_empty(self):
        variables = self._panel.getVarDict()
        self.assertEqual(variables, {})

    def test_single_empty(self):
        self._panel.addStringVariable('test')
        variables = self._panel.getVarDict()
        self.assertEqual(variables, {'test': ''})

    def test_single(self):
        self._panel.addStringVariable('test')
        self._panel.setVarString('test', 'Проверка')

        variables = self._panel.getVarDict()
        self.assertEqual(variables, {'test': 'Проверка'})

    def test_two_items(self):
        self._panel.addStringVariable('test_1')
        self._panel.addStringVariable('test_2')

        self._panel.setVarString('test_1', 'Проверка_1')
        self._panel.setVarString('test_2', 'Проверка_2')

        variables = self._panel.getVarDict()
        self.assertEqual(variables, {'test_1': 'Проверка_1',
                                     'test_2': 'Проверка_2'})

    def test_no_item(self):
        self.assertRaises(KeyError, self._panel.setVarString, 'test', 'test')
