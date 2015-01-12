# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.parser.commandtest import TestCommand, ExceptionCommand
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class WikiCommandsTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])
        self.testPage = self.wikiroot[u"Страница 2"]


    def tearDown(self):
        removeDir (self.path)


    def testParamsParsing1 (self):
        params_text = u"""Параметр1
Параметр2 = 111
Параметр3 = " бла бла бла"
Параметр4
Параметр5="111"
Параметр6=' 222 '
Параметр7 = " проверка 'бла бла бла' проверка"
Параметр8 = ' проверка "bla-bla-bla" тест '
Параметр9 = -1
Параметр10 = -10.5
Параметр11 = 12.5
"""

        params = Command.parseParams (params_text)

        self.assertEqual (len (params), 11, params)
        self.assertEqual (params[u"Параметр1"], u"")
        self.assertEqual (params[u"Параметр2"], u"111")
        self.assertEqual (params[u"Параметр3"], u" бла бла бла")
        self.assertEqual (params[u"Параметр4"], u"")
        self.assertEqual (params[u"Параметр5"], u"111")
        self.assertEqual (params[u"Параметр6"], u" 222 ")
        self.assertEqual (params[u"Параметр7"], u" проверка 'бла бла бла' проверка")
        self.assertEqual (params[u"Параметр8"], u' проверка "bla-bla-bla" тест ')
        self.assertEqual (params[u"Параметр9"], u"-1")
        self.assertEqual (params[u"Параметр10"], u"-10.5")
        self.assertEqual (params[u"Параметр11"], u"12.5")


    def testParamsParsing2 (self):
        params_text = u""
        params = Command.parseParams (params_text)

        self.assertEqual (len (params), 0)


    def testParamsParsing3 (self):
        params_text = u"""Параметр=-1"""
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"-1")


    def testParamsParsing4 (self):
        params_text = u'Параметр="-1"'
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"-1")


    def testParamsParsing5 (self):
        params_text = u'Параметр= -1 '
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"-1")


    def testParamsParsing6 (self):
        params_text = u'Параметр=Бла-бла-бла'
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла-бла-бла")


    def testParamsParsing7 (self):
        params_text = u'Параметр= Бла-бла-бла'
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла-бла-бла")


    def testParamsParsing8 (self):
        params_text = u'Параметр=Бла_бла_бла'
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла_бла_бла")


    def testParamsParsing9 (self):
        params_text = u'Параметр= Бла_бла_бла'
        params = Command.parseParams (params_text)
        self.assertEqual (params[u"Параметр"], u"Бла_бла_бла")


    def testParamsParsing10 (self):
        params_text = u"""Параметр1.Подпараметр
            Пар_аме_тр2 = 111
            Параметр3.Еще.Подпар_аметр
            Пар.ам.етр4 = " проверка 'бла бла бла' проверка"
            Пар.аме.тр5 = ' проверка "bla-bla-bla" тест ' """

        params = Command.parseParams (params_text)

        self.assertEqual (len (params), 5)
        self.assertEqual (params[u"Параметр1.Подпараметр"], u"")
        self.assertEqual (params[u"Пар_аме_тр2"], u"111")
        self.assertEqual (params[u"Параметр3.Еще.Подпар_аметр"], u"")
        self.assertEqual (params[u"Пар.ам.етр4"], u" проверка 'бла бла бла' проверка")
        self.assertEqual (params[u"Пар.аме.тр5"], u' проверка "bla-bla-bla" тест ')


    def testCommandTest1 (self):
        self.parser.addCommand (TestCommand (self.parser))
        text = u"""(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды"""

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)


    def testCommandTest2 (self):
        command = TestCommand (self.parser)
        params = u"Параметр1 Параметр2=2 Параметр3=3"
        content = u"""Текст внутри
команды"""

        self.assertEqual (command.name, u"test")

        result = command.execute (params, content)
        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды"""

        self.assertEqual (result_right, result, result)


    def testCommandTest3 (self):
        self.parser.addCommand (TestCommand (self.parser))
        text = u"""(: test Параметр1 Параметр2=2 Параметр3=3 :)"""

        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: """

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)


    def testCommandTest4 (self):
        self.parser.addCommand (TestCommand (self.parser))
        text = u"""(:test:)"""

        result_right = u"""Command name: test
params: 
content: """

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)


    def testCommandTest5 (self):
        self.parser.addCommand (TestCommand (self.parser))
        text = u"""(: test Параметр1 Параметр2=2 Параметр3=3 :)"""

        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: """

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)


    def testCommandTest6 (self):
        self.parser.addCommand (TestCommand (self.parser))
        text = u"""(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)

(: test Параметры :)
Контент
(:testend:)"""

        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды

Command name: test
params: Параметры
content: Контент"""

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)


    def testCommandTest7 (self):
        factory = ParserFactory ()
        factory.appendCommand (TestCommand)

        parser = factory.make (self.testPage, Application.config)


        text = u"""(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)

(: test Параметры :)
Контент
(:testend:)"""

        result_right = u"""Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды

Command name: test
params: Параметры
content: Контент"""

        result = parser.toHtml (text)
        self.assertEqual (result_right, result, result)



    def testInvalidCommandTest (self):
        text = u"""(: testblabla Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result_right = u"""(: testblabla Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result = self.parser.toHtml (text)
        self.assertEqual (result_right, result, result)


    def testExceptionCommand (self):
        factory = ParserFactory ()
        factory.appendCommand (ExceptionCommand)

        parser = factory.make (self.testPage, Application.config)

        text = u"""(:exception:)"""

        result = parser.toHtml(text)
        # Исключение не должно бросаться, а должно быть выведено в результирующий текст
        self.assertTrue ("Exception" in result, result)
