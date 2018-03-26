# -*- coding: utf-8 -*-

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUITest


class ExecDialogTest(BaseOutWikerGUITest):
    """
    Tests for ExecDialog and ExecDialogController
    """

    def setUp(self):
        self.initApplication()

        dirlist = ["../plugins/externaltools"]

        self._loader = PluginsLoader(self.application)
        self._loader.load(dirlist)

        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig(self.application.config).clearAll()

        from externaltools.commandexec.execdialog import ExecDialog
        self._dlg = ExecDialog(self.application.mainWindow)
        Tester.dialogTester.clear()
        Tester.dialogTester.appendOk()

    def tearDown(self):
        self._dlg.Destroy()
        self._loader.clear()

        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig(self.application.config).clearAll()

        self.destroyApplication()

    def testDefault(self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController(
            self._dlg,
            self.application
        )

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual(result, wx.ID_OK)
        self.assertEqual(begin, '(:exec:)')
        self.assertEqual(end, '(:execend:)')

    def testTitle(self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController(
            self._dlg,
            self.application
        )

        self._dlg.title = 'Заголовок команды'

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual(result, wx.ID_OK)
        self.assertEqual(begin, '(:exec title="Заголовок команды":)')
        self.assertEqual(end, '(:execend:)')

    def testFormat(self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController(
            self._dlg,
            self.application
        )

        self._dlg.format = 1

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual(result, wx.ID_OK)
        self.assertEqual(begin, '(:exec format="button":)')
        self.assertEqual(end, '(:execend:)')

    def testTitleFormat(self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController(
            self._dlg,
            self.application
        )

        self._dlg.title = 'Заголовок команды'
        self._dlg.format = 1

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual(result, wx.ID_OK)
        self.assertEqual(
            begin, '(:exec title="Заголовок команды" format="button":)')
        self.assertEqual(end, '(:execend:)')
