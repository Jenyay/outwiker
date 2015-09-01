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


    def testCommand_single_row_01 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)(:cell:)ааа(:cell:)ббб'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_single_row_02 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:cell:)ааа(:cell:)ббб'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_01 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)(:cell:)ааа(:cell:)ббб(:row:)(:cell:)ввв(:cell:)ггг'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_02 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)(:cell:)ааа(:cell:)ббб(:row:)(:cell:)ввв(:cell:)ггг(:cell:)'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td><td></td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_03 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)(:cell:)ааа(:cell:)ббб(:row:)(:cell:)ввв(:cell:)ггг(:row:)'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr><tr></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_04_params (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row rowparam=один:)(:cell cellparam=два:)ааа(:cell cellparam2=три cellparam3=четыре:)ббб(:row:)(:cell:)ввв(:cell:)ггг(:cell:)'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr rowparam=один><td cellparam=два>ааа</td><td cellparam2=три cellparam3=четыре>ббб</td></tr><tr><td>ввв</td><td>ггг</td><td></td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_05 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)
(:cell:)ааа
(:cell:)ббб
(:row:)
(:cell:)ввв
(:cell:)ггг'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_01 (self):
        text = u'''(:table:)(:row:)(:cell:)ааа(:cell:)ббб(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_02 (self):
        text = u'''(:table:)(:cell:)ааа(:cell:)ббб(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_03 (self):
        text = u'''(:table:)
(:row:)
(:cell:)ааа
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_04 (self):
        text = u'''(:table:)
(:row:)
(:cell:)ааа
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_05 (self):
        text = u'''(:table:)
(:row:)
(:cell:)ааа(:cellend:)
(:cell:)ббб(:cellend:)
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_06 (self):
        text = u'''(:table:)
(:row:)
(:cell:)ааа(:cellend:)ййй
(:cell:)ббб(:cellend:)ццц
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td>аааййй</td><td>бббццц</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_07 (self):
        text = u'''(:table:)
(:row:)
(:cell:)''ааа''(:cellend:)
(:cell:)ббб(:cellend:)
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = u'''<table><tr><td><i>ааа</i></td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_08 (self):
        cmd = TableCommand (self.parser)
        text = u'''(:row:)
(:cell:)ааа
(:cell:)ббб
(:rowend:)(:row:)
(:cell:)ввв
(:cell:)ггг
(:rowend:)'''

        result = cmd.execute (u'', text)

        valid = u'''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr></table>'''
        self.assertEqual (result, valid, result)
