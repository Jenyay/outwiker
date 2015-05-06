# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader

from test.guitests.basemainwnd import BaseMainWndTest
from outwiker.gui.tester import Tester


class ExecDialogTest (BaseMainWndTest):
    """
    Tests for ExecDialog and ExecDialogController
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        dirlist = [u"../plugins/externaltools"]

        self._loader = PluginsLoader(Application)
        self._loader.load (dirlist)

        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig (Application.config).clearAll()

        from externaltools.commandexec.execdialog import ExecDialog
        self._dlg = ExecDialog (Application.mainWindow)
        Tester.dialogTester.clear()
        Tester.dialogTester.appendOk()


    def tearDown(self):
        Application.wikiroot = None
        self._dlg.Destroy()
        self._loader.clear()

        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig (Application.config).clearAll()

        BaseMainWndTest.tearDown (self)


    def testDefault (self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController (
            self._dlg,
            Application
        )

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual (result, wx.ID_OK)
        self.assertEqual (begin, u'(:exec:)')
        self.assertEqual (end, u'(:execend:)')


    def testTitle (self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController (
            self._dlg,
            Application
        )

        self._dlg.title = u'Заголовок команды'

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual (result, wx.ID_OK)
        self.assertEqual (begin, u'(:exec title="Заголовок команды":)')
        self.assertEqual (end, u'(:execend:)')


    def testFormat (self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController (
            self._dlg,
            Application
        )

        self._dlg.format = 1

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual (result, wx.ID_OK)
        self.assertEqual (begin, u'(:exec format="button":)')
        self.assertEqual (end, u'(:execend:)')


    def testTitleFormat (self):
        from externaltools.commandexec.execdialogcontroller import ExecDialogController

        controller = ExecDialogController (
            self._dlg,
            Application
        )

        self._dlg.title = u'Заголовок команды'
        self._dlg.format = 1

        result = controller.showDialog()
        begin, end = controller.getResult()

        self.assertEqual (result, wx.ID_OK)
        self.assertEqual (begin, u'(:exec title="Заголовок команды" format="button":)')
        self.assertEqual (end, u'(:execend:)')
