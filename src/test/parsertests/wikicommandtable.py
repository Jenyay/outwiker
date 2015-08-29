# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parser.commands.table import TableCommand

from test.utils import removeDir


class WikiCommandTableTest (unittest.TestCase):
    def setUp(self):
        self.__createWiki()
        self.testPage = self.wikiroot[u'Страница 1']

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, u'Страница 1', [])


    def tearDown(self):
        removeDir (self.path)


    def testCommand_empty (self):
        cmd = TableCommand (self.parser)
        result = cmd.execute (u'', u'')

        valid = u'''<table></table>'''
        self.assertEqual (result, valid)


    def testParser_empty (self):
        text = u'(:table:)(:tableend:)'
        result = self.parser.toHtml (text)

        valid = u'''<table></table>'''
        self.assertEqual (result, valid)


    def testTable_empty_params (self):
        cmd = TableCommand (self.parser)
        result = cmd.execute (u'border=1', u'')

        valid = u'''<table border=1></table>'''
        self.assertEqual (result, valid)


    def testParser_empty_params (self):
        text = u'(:table border=1:)(:tableend:)'
        result = self.parser.toHtml (text)

        valid = u'''<table border=1></table>'''
        self.assertEqual (result, valid)


    def testTable_empty_params_2 (self):
        cmd = TableCommand (self.parser)
        result = cmd.execute (u'border=1 width=100', u'')

        valid = u'''<table border=1 width=100></table>'''
        self.assertEqual (result, valid)


    def testParser_empty_params_2 (self):
        text = u'(:table border=1 width=100:)(:tableend:)'
        result = self.parser.toHtml (text)

        valid = u'''<table border=1 width=100></table>'''
        self.assertEqual (result, valid)


    def testParser_suffix (self):
        text = u'(:table2:)(:table2end:)'
        result = self.parser.toHtml (text)

        valid = u'''<table></table>'''
        self.assertEqual (result, valid)


    def testParser_suffix_invalid (self):
        text = u'(:table20:)(:table20end:)'
        result = self.parser.toHtml (text)

        valid = u'''(:table20:)(:table20end:)'''
        self.assertEqual (result, valid)


    def testCommand_single_row (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)
(:cell:)ааа
(:cell:)ббб'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid)
