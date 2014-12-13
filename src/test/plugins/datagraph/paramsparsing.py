# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class ParamsParsingTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.parseGraphParams = self.loader[u'DataGraph'].PlotCommand.parseGraphParams


    def tearDown (self):
        self.loader.clear()


    def testParamsParsing_01 (self):
        params_text = u"""Параметр1
        Параметр2 = 111
        Параметр3 = " бла бла бла"
        Параметр4
        Параметр5="111"
        Параметр6=' 222 '
        Параметр7 = " проверка 'бла бла бла' проверка"
        Параметр8 = ' проверка "bla-bla-bla" тест ' """

        params = self.parseGraphParams (params_text)

        self.assertEqual (len (params), 8)
        self.assertEqual (params[u"Параметр1"], u"")
        self.assertEqual (params[u"Параметр2"], u"111")
        self.assertEqual (params[u"Параметр3"], u" бла бла бла")
        self.assertEqual (params[u"Параметр4"], u"")
        self.assertEqual (params[u"Параметр5"], u"111")
        self.assertEqual (params[u"Параметр6"], u" 222 ")
        self.assertEqual (params[u"Параметр7"], u" проверка 'бла бла бла' проверка")
        self.assertEqual (params[u"Параметр8"], u' проверка "bla-bla-bla" тест ')


    def testParamsParsing_02 (self):
        params_text = u""
        params = self.parseGraphParams (params_text)

        self.assertEqual (len (params), 0)


    def testParamsParsing_03 (self):
        params_text = u"""Параметр=-1"""
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"-1")


    def testParamsParsing_04 (self):
        params_text = u'Параметр="-1"'
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"-1")


    def testParamsParsing_05 (self):
        params_text = u'Параметр= -1 '
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"-1")


    def testParamsParsing_06 (self):
        params_text = u'Параметр=Бла-бла-бла'
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла-бла-бла")


    def testParamsParsing_07 (self):
        params_text = u'Параметр= Бла-бла-бла'
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла-бла-бла")


    def testParamsParsing_08 (self):
        params_text = u'Параметр=Бла_бла_бла'
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла_бла_бла")


    def testParamsParsing_09 (self):
        params_text = u'Параметр= Бла_бла_бла'
        params = self.parseGraphParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла_бла_бла")


    def testParamsParsing_10 (self):
        params_text = u"""Параметр1.Подпараметр
        Пар_аме_тр2 = 111
        Параметр3.Еще.Подпар_аметр
        Пар.ам.етр4 = " проверка 'бла бла бла' проверка"
        Пар.аме.тр5 = ' проверка "bla-bla-bla" тест ' """

        params = self.parseGraphParams (params_text)

        self.assertEqual (len (params), 5)
        self.assertEqual (params[u"Параметр1.Подпараметр"], u"")
        self.assertEqual (params[u"Пар_аме_тр2"], u"111")
        self.assertEqual (params[u"Параметр3.Еще.Подпар_аметр"], u"")
        self.assertEqual (params[u"Пар.ам.етр4"], u" проверка 'бла бла бла' проверка")
        self.assertEqual (params[u"Пар.аме.тр5"], u' проверка "bla-bla-bla" тест ')
