# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from test.guitests.basemainwnd import BaseMainWndTest


class VarDialogTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)
        mainWnd = Application.mainWindow
        plugins_dir = [u"../plugins/snippets"]

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
        self._dialog.addStringVariable(u'test')
        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {u'test': u''})

    def test_single(self):
        self._dialog.addStringVariable(u'test')
        self._dialog.setStringVariable(u'test', u'Проверка')

        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {u'test': u'Проверка'})

    def test_two_items(self):
        self._dialog.addStringVariable(u'test_1')
        self._dialog.addStringVariable(u'test_2')

        self._dialog.setStringVariable(u'test_1', u'Проверка_1')
        self._dialog.setStringVariable(u'test_2', u'Проверка_2')

        variables = self._dialog.getVarDict()
        self.assertEqual(variables, {u'test_1': u'Проверка_1',
                                     u'test_2': u'Проверка_2'})

    def test_no_item(self):
        self.assertRaises(KeyError,
                          self._dialog.setStringVariable,
                          u'test',
                          u'test')
