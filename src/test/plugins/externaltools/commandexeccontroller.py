# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.events import LinkClickParams
from outwiker.gui.tester import Tester


class CommandExecControllerTest (unittest.TestCase):
    def setUp (self):
        dirlist = [u'../plugins/externaltools']

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        from externaltools.commandexec.commandcontroller import CommandController
        self._controller = CommandController (Application)
        self._controller.initialize()

        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig (Application.config).clearAll()

        Tester.dialogTester.clear()


    def tearDown (self):
        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig (Application.config).clearAll()

        self._controller.destroy()
        self.loader.clear()
        Tester.dialogTester.clear()


    def testStatus_01 (self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo (u'gvim', [])]
        title = self._controller.getStatusTitle (commands)
        rightTitle = u'>>> gvim'

        self.assertEqual (title, rightTitle)


    def testStatus_02 (self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [
            ExecInfo (u'gvim', []),
            ExecInfo (u'krusader', []),
        ]

        title = self._controller.getStatusTitle (commands)
        rightTitle = u'>>> gvim ...'

        self.assertEqual (title, rightTitle)


    def testStatus_03 (self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo (u'gvim', [u'абырвалг'])]
        title = self._controller.getStatusTitle (commands)
        rightTitle = u'>>> gvim абырвалг'

        self.assertEqual (title, rightTitle)


    def testStatus_04 (self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo (u'gvim', [u'абырвалг', u'главрыба'])]
        title = self._controller.getStatusTitle (commands)
        rightTitle = u'>>> gvim абырвалг главрыба'

        self.assertEqual (title, rightTitle)


    def testStatus_05 (self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo (u'gvim', [u'абырвалг главрыба'])]
        title = self._controller.getStatusTitle (commands)
        rightTitle = u'>>> gvim "абырвалг главрыба"'

        self.assertEqual (title, rightTitle)


    def testStatus_06 (self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [
            ExecInfo (u'gvim', [u'абырвалг главрыба']),
            ExecInfo (u'gvim', [u'абырвалг главрыба']),
        ]
        title = self._controller.getStatusTitle (commands)
        rightTitle = u'>>> gvim "абырвалг главрыба" ...'

        self.assertEqual (title, rightTitle)


    def testCommandsList_01 (self):
        urlparams = {}
        commands = self._controller.getCommandsList (urlparams)

        self.assertEqual (len (commands), 0)


    def testCommandsList_02 (self):
        urlparams = {u'com1': ['gvim']}
        commands = self._controller.getCommandsList (urlparams)

        self.assertEqual (len (commands), 1)
        self.assertEqual (commands[0].command, u'gvim')
        self.assertEqual (commands[0].params, [])


    def testCommandsList_03 (self):
        urlparams = {u'com1': ['gvim', 'abyrvalg']}
        commands = self._controller.getCommandsList (urlparams)

        self.assertEqual (len (commands), 1)
        self.assertEqual (commands[0].command, u'gvim')
        self.assertEqual (commands[0].params, [u'abyrvalg'])


    def testCommandsList_04 (self):
        urlparams = {
            u'com1': ['gvim', 'abyrvalg'],
            u'com3': ['gvim', 'abyrvalg'],
        }
        commands = self._controller.getCommandsList (urlparams)

        self.assertEqual (len (commands), 1)
        self.assertEqual (commands[0].command, u'gvim')
        self.assertEqual (commands[0].params, [u'abyrvalg'])


    def testCommandsList_05 (self):
        urlparams = {
            u'com1': ['gvim', 'abyrvalg'],
            u'com2': ['krusader', 'glavryba'],
        }
        commands = self._controller.getCommandsList (urlparams)

        self.assertEqual (len (commands), 2)
        self.assertEqual (commands[0].command, u'gvim')
        self.assertEqual (commands[0].params, [u'abyrvalg'])

        self.assertEqual (commands[1].command, u'krusader')
        self.assertEqual (commands[1].params, [u'glavryba'])


    def testOnLinkClick_01 (self):
        params = LinkClickParams (u'exec://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertTrue (params.process)


    def testOnLinkClick_02 (self):
        params = LinkClickParams (u'other://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 1)
        self.assertFalse (params.process)


    def testOnLinkClick_03 (self):
        params = LinkClickParams (u'exec://other/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 1)
        self.assertFalse (params.process)


    def testOnLinkClick_04 (self):
        params = LinkClickParams (u'exec://exec/')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 1)
        self.assertFalse (params.process)


    def testOnLinkClick_05 (self):
        params = LinkClickParams (u'exec://exec/?title=qqq')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertTrue (params.process)


    def testWarning_01 (self):
        from externaltools.config import ExternalToolsConfig
        config = ExternalToolsConfig (Application.config)
        config.execWarning = True

        params = LinkClickParams (u'exec://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 0)
        self.assertTrue (params.process)


    def testWarning_02 (self):
        from externaltools.config import ExternalToolsConfig
        config = ExternalToolsConfig (Application.config)
        config.execWarning = False

        params = LinkClickParams (u'exec://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual (Tester.dialogTester.count, 1)

        self._controller.onLinkClick (None, params)
        self.assertEqual (Tester.dialogTester.count, 1)
        self.assertTrue (params.process)
