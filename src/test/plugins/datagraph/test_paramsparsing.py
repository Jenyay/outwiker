# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class ParamsParsingTest(unittest.TestCase):
    def setUp(self):
        dirlist = ["../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()

    def testParamsParsing_01(self):
        from datagraph.commands import PlotCommand
        params_text = """Параметр1
        Параметр2 = 111
        Параметр3 = " бла бла бла"
        Параметр4
        Параметр5="111"
        Параметр6=' 222 '
        Параметр7 = " проверка 'бла бла бла' проверка"
        Параметр8 = ' проверка "bla-bla-bla" тест ' """

        params = PlotCommand.parseGraphParams(params_text)

        self.assertEqual(len(params), 8)
        self.assertEqual(params["Параметр1"], "")
        self.assertEqual(params["Параметр2"], "111")
        self.assertEqual(params["Параметр3"], " бла бла бла")
        self.assertEqual(params["Параметр4"], "")
        self.assertEqual(params["Параметр5"], "111")
        self.assertEqual(params["Параметр6"], " 222 ")
        self.assertEqual(params["Параметр7"], " проверка 'бла бла бла' проверка")
        self.assertEqual(params["Параметр8"], ' проверка "bla-bla-bla" тест ')

    def testParamsParsing_02(self):
        from datagraph.commands import PlotCommand
        params_text = ""
        params = PlotCommand.parseGraphParams(params_text)

        self.assertEqual(len(params), 0)

    def testParamsParsing_03(self):
        from datagraph.commands import PlotCommand
        params_text = """Параметр=-1"""
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "-1")

    def testParamsParsing_04(self):
        from datagraph.commands import PlotCommand
        params_text = 'Параметр="-1"'
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "-1")

    def testParamsParsing_05(self):
        from datagraph.commands import PlotCommand
        params_text = 'Параметр= -1 '
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "-1")

    def testParamsParsing_06(self):
        from datagraph.commands import PlotCommand
        params_text = 'Параметр=Бла-бла-бла'
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "Бла-бла-бла")

    def testParamsParsing_07(self):
        from datagraph.commands import PlotCommand
        params_text = 'Параметр= Бла-бла-бла'
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "Бла-бла-бла")

    def testParamsParsing_08(self):
        from datagraph.commands import PlotCommand
        params_text = 'Параметр=Бла_бла_бла'
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "Бла_бла_бла")

    def testParamsParsing_09(self):
        from datagraph.commands import PlotCommand
        params_text = 'Параметр= Бла_бла_бла'
        params = PlotCommand.parseGraphParams(params_text)
        self.assertEqual(params["Параметр"], "Бла_бла_бла")

    def testParamsParsing_10(self):
        from datagraph.commands import PlotCommand
        params_text = """Параметр1.Подпараметр
        Пар_аме_тр2 = 111
        Параметр3.Еще.Подпар_аметр
        Пар.ам.етр4 = " проверка 'бла бла бла' проверка"
        Пар.аме.тр5 = ' проверка "bla-bla-bla" тест ' """

        params = PlotCommand.parseGraphParams(params_text)

        self.assertEqual(len(params), 5)
        self.assertEqual(params["Параметр1.Подпараметр"], "")
        self.assertEqual(params["Пар_аме_тр2"], "111")
        self.assertEqual(params["Параметр3.Еще.Подпар_аметр"], "")
        self.assertEqual(params["Пар.ам.етр4"], " проверка 'бла бла бла' проверка")
        self.assertEqual(params["Пар.аме.тр5"], ' проверка "bla-bla-bla" тест ')
