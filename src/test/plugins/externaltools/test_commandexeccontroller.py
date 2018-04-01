# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.events import LinkClickParams
from outwiker.gui.tester import Tester
from test.basetestcases import BaseOutWikerGUIMixin


class CommandExecControllerTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        dirlist = ['../plugins/externaltools']

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        from externaltools.commandexec.commandcontroller import CommandController
        self._controller = CommandController(Application)
        self._controller.initialize()

        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig(Application.config).clearAll()

        Tester.dialogTester.clear()

    def tearDown(self):
        from externaltools.config import ExternalToolsConfig
        ExternalToolsConfig(Application.config).clearAll()

        self._controller.destroy()
        self.loader.clear()
        Tester.dialogTester.clear()
        self.destroyApplication()

    def testStatus_01(self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo('gvim', [])]
        title = self._controller.getStatusTitle(commands)
        rightTitle = '>>> gvim'

        self.assertEqual(title, rightTitle)

    def testStatus_02(self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [
            ExecInfo('gvim', []),
            ExecInfo('krusader', []),
        ]

        title = self._controller.getStatusTitle(commands)
        rightTitle = '>>> gvim ...'

        self.assertEqual(title, rightTitle)

    def testStatus_03(self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo('gvim', ['abyrvalg'])]
        title = self._controller.getStatusTitle(commands)
        rightTitle = '>>> gvim abyrvalg'

        self.assertEqual(title, rightTitle)

    def testStatus_04(self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo('gvim', ['abyrvalg', 'glavryba'])]
        title = self._controller.getStatusTitle(commands)
        rightTitle = '>>> gvim abyrvalg glavryba'

        self.assertEqual(title, rightTitle)

    def testStatus_05(self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [ExecInfo('gvim', ['abyrvalg glavryba'])]
        title = self._controller.getStatusTitle(commands)
        rightTitle = '>>> gvim "abyrvalg glavryba"'

        self.assertEqual(title, rightTitle)

    def testStatus_06(self):
        from externaltools.commandexec.execinfo import ExecInfo

        commands = [
            ExecInfo('gvim', ['abyrvalg glavryba']),
            ExecInfo('gvim', ['abyrvalg glavryba']),
        ]
        title = self._controller.getStatusTitle(commands)
        rightTitle = '>>> gvim "abyrvalg glavryba" ...'

        self.assertEqual(title, rightTitle)

    def testCommandsList_01(self):
        urlparams = {}
        commands = self._controller.getCommandsList(urlparams)

        self.assertEqual(len(commands), 0)

    def testCommandsList_02(self):
        urlparams = {'com1': ['gvim']}
        commands = self._controller.getCommandsList(urlparams)

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].command, 'gvim')
        self.assertEqual(commands[0].params, [])

    def testCommandsList_03(self):
        urlparams = {'com1': ['gvim', 'abyrvalg']}
        commands = self._controller.getCommandsList(urlparams)

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].command, 'gvim')
        self.assertEqual(commands[0].params, ['abyrvalg'])

    def testCommandsList_04(self):
        urlparams = {
            'com1': ['gvim', 'abyrvalg'],
            'com3': ['gvim', 'abyrvalg'],
        }
        commands = self._controller.getCommandsList(urlparams)

        self.assertEqual(len(commands), 1)
        self.assertEqual(commands[0].command, 'gvim')
        self.assertEqual(commands[0].params, ['abyrvalg'])

    def testCommandsList_05(self):
        urlparams = {
            'com1': ['gvim', 'abyrvalg'],
            'com2': ['krusader', 'glavryba'],
        }
        commands = self._controller.getCommandsList(urlparams)

        self.assertEqual(len(commands), 2)
        self.assertEqual(commands[0].command, 'gvim')
        self.assertEqual(commands[0].params, ['abyrvalg'])

        self.assertEqual(commands[1].command, 'krusader')
        self.assertEqual(commands[1].params, ['glavryba'])

    def testOnLinkClick_01(self):
        params = LinkClickParams('exec://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertTrue(params.process)

    def testOnLinkClick_02(self):
        params = LinkClickParams('other://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 1)
        self.assertFalse(params.process)

    def testOnLinkClick_03(self):
        params = LinkClickParams('exec://other/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 1)
        self.assertFalse(params.process)

    def testOnLinkClick_04(self):
        params = LinkClickParams('exec://exec/')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 1)
        self.assertFalse(params.process)

    def testOnLinkClick_05(self):
        params = LinkClickParams('exec://exec/?title=qqq')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertTrue(params.process)

    def testWarning_01(self):
        from externaltools.config import ExternalToolsConfig
        config = ExternalToolsConfig(Application.config)
        config.execWarning = True

        params = LinkClickParams('exec://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertTrue(params.process)

    def testWarning_02(self):
        from externaltools.config import ExternalToolsConfig
        config = ExternalToolsConfig(Application.config)
        config.execWarning = False

        params = LinkClickParams('exec://exec/?com1=sometools')

        Tester.dialogTester.appendOk()
        self.assertEqual(Tester.dialogTester.count, 1)

        self._controller.onLinkClick(None, params)
        self.assertEqual(Tester.dialogTester.count, 1)
        self.assertTrue(params.process)
