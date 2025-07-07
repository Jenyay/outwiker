# -*- coding: utf-8 -*-

from tempfile import mkdtemp
from unittest import TestCase

from outwiker.api.core.tree import createNotesTree
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerMixin


class WikiCommandsTest (BaseOutWikerMixin, TestCase):
    def setUp(self):
        self.initApplication()

        self.filesPath = "testdata/samplefiles/"
        self.__createWiki()

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, self.application)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def testParamsParsing1(self):
        params_text = """Параметр1
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

        params = Command.parseParams(params_text)

        self.assertEqual(len(params), 11, params)
        self.assertEqual(params["Параметр1"], "")
        self.assertEqual(params["Параметр2"], "111")
        self.assertEqual(params["Параметр3"], " бла бла бла")
        self.assertEqual(params["Параметр4"], "")
        self.assertEqual(params["Параметр5"], "111")
        self.assertEqual(params["Параметр6"], " 222 ")
        self.assertEqual(
            params["Параметр7"],
            " проверка 'бла бла бла' проверка")
        self.assertEqual(params["Параметр8"], ' проверка "bla-bla-bla" тест ')
        self.assertEqual(params["Параметр9"], "-1")
        self.assertEqual(params["Параметр10"], "-10.5")
        self.assertEqual(params["Параметр11"], "12.5")

    def testParamsParsing2(self):
        params_text = ""
        params = Command.parseParams(params_text)

        self.assertEqual(len(params), 0)

    def testParamsParsing3(self):
        params_text = """Параметр=-1"""
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "-1")

    def testParamsParsing4(self):
        params_text = 'Параметр="-1"'
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "-1")

    def testParamsParsing5(self):
        params_text = 'Параметр= -1 '
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "-1")

    def testParamsParsing6(self):
        params_text = 'Параметр=Бла-бла-бла'
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "Бла-бла-бла")

    def testParamsParsing7(self):
        params_text = 'Параметр= Бла-бла-бла'
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "Бла-бла-бла")

    def testParamsParsing8(self):
        params_text = 'Параметр=Бла_бла_бла'
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "Бла_бла_бла")

    def testParamsParsing9(self):
        params_text = 'Параметр= Бла_бла_бла'
        params = Command.parseParams(params_text)
        self.assertEqual(params["Параметр"], "Бла_бла_бла")

    def testParamsParsing10(self):
        params_text = """Параметр1.Подпараметр
            Пар_аме_тр2 = 111
            Параметр3.Еще.Подпар_аметр
            Пар.ам.етр4 = " проверка 'бла бла бла' проверка"
            Пар.аме.тр5 = ' проверка "bla-bla-bla" тест ' """

        params = Command.parseParams(params_text)

        self.assertEqual(len(params), 5)
        self.assertEqual(params["Параметр1.Подпараметр"], "")
        self.assertEqual(params["Пар_аме_тр2"], "111")
        self.assertEqual(params["Параметр3.Еще.Подпар_аметр"], "")
        self.assertEqual(
            params["Пар.ам.етр4"],
            " проверка 'бла бла бла' проверка")
        self.assertEqual(
            params["Пар.аме.тр5"],
            ' проверка "bla-bla-bla" тест ')

    def testCommandTest1(self):
        self.parser.addCommand(ExampleCommand(self.parser))
        text = """(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды"""

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testCommandTest2(self):
        command = ExampleCommand(self.parser)
        params = "Параметр1 Параметр2=2 Параметр3=3"
        content = """Текст внутри
команды"""

        self.assertEqual(command.name, "test")

        result = command.execute(params, content)
        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды"""

        self.assertEqual(result_right, result, result)

    def testCommandTest3(self):
        self.parser.addCommand(ExampleCommand(self.parser))
        text = """(: test Параметр1 Параметр2=2 Параметр3=3 :)"""

        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: """

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testCommandTest4(self):
        self.parser.addCommand(ExampleCommand(self.parser))
        text = """(:test:)"""

        result_right = """Command name: test
params: 
content: """

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testCommandTest5(self):
        self.parser.addCommand(ExampleCommand(self.parser))
        text = """(: test Параметр1 Параметр2=2 Параметр3=3 :)"""

        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: """

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testCommandTest6(self):
        self.parser.addCommand(ExampleCommand(self.parser))
        text = """(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)

(: test Параметры :)
Контент
(:testend:)"""

        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды

Command name: test
params: Параметры
content: Контент"""

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testCommandTest7(self):
        factory = ParserFactory()

        parser = factory.make(self.testPage, self.application)
        parser.addCommand(ExampleCommand(parser))

        text = """(: test Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)

(: test Параметры :)
Контент
(:testend:)"""

        result_right = """Command name: test
params: Параметр1 Параметр2=2 Параметр3=3
content: Текст внутри
команды

Command name: test
params: Параметры
content: Контент"""

        result = parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testInvalidCommandTest(self):
        text = """(: testblabla Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result_right = """(: testblabla Параметр1 Параметр2=2 Параметр3=3 :)
Текст внутри
команды
(:testend:)"""

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result, result)

    def testExceptionCommand(self):
        factory = ParserFactory()

        parser = factory.make(self.testPage, self.application)
        parser.addCommand(ExceptionCommand(parser))

        text = """(:exception:)"""

        result = parser.toHtml(text)
        # Исключение не должно бросаться, а должно быть выведено в
        # результирующий текст
        self.assertTrue("Exception" in result, result)

    def testCommand_remove(self):
        command = ExampleCommand(self.parser)

        self.parser.addCommand(command)
        text = """(:test:)"""

        result_right = """Command name: test
params: 
content: """

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

        self.parser.removeCommand(command.name)

        result = self.parser.toHtml(text)
        self.assertEqual(text, result)

    def testCommand_remove_none(self):
        command = ExampleCommand(self.parser)

        self.parser.addCommand(command)
        text = """(:test:)"""

        result_right = """Command name: test
params: 
content: """

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

        self.parser.removeCommand(None)

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

    def testCommand_remove_invalid(self):
        command = ExampleCommand(self.parser)

        self.parser.addCommand(command)
        text = """(:test:)"""

        result_right = """Command name: test
params: 
content: """

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)

        self.parser.removeCommand('абырвалг')

        result = self.parser.toHtml(text)
        self.assertEqual(result_right, result)


class ExampleCommand (Command):
    """
    Тестовая команда. Обрабатывает команды вида
        (:test params... :) content (:testend:)
    В результате выводит текст:
        Command name: test
        params: params
        content: content
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"test"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды
        в вики-нотации
        """
        params_result = params if params is not None else u""
        content_result = content if content is not None else u""

        result = u"""Command name: test
params: {params}
content: {content}""".format(params=params_result.strip(),
                             content=content_result.strip())

        return result


class ExceptionCommand (Command):
    """
    Тестовая команда, которая бросает исключение Exception
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"exception"

    def execute(self, params, content):
        raise Exception
