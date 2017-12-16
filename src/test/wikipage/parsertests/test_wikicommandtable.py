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
        self.testPage = self.wikiroot['Страница 1']

        factory = ParserFactory()
        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, 'Страница 1', [])


    def tearDown(self):
        removeDir (self.path)


    def testCommand_empty (self):
        cmd = TableCommand (self.parser)
        result = cmd.execute ('', '')

        valid = '''<table></table>'''
        self.assertEqual (result, valid)


    def testParser_empty (self):
        text = '(:table:)(:tableend:)'
        result = self.parser.toHtml (text)

        valid = '''<table></table>'''
        self.assertEqual (result, valid)


    def testTable_empty_params (self):
        cmd = TableCommand (self.parser)
        result = cmd.execute ('border=1', '')

        valid = '''<table border=1></table>'''
        self.assertEqual (result, valid)


    def testParser_empty_params (self):
        text = '(:table border=1:)(:tableend:)'
        result = self.parser.toHtml (text)

        valid = '''<table border=1></table>'''
        self.assertEqual (result, valid)


    def testTable_empty_params_2 (self):
        cmd = TableCommand (self.parser)
        result = cmd.execute ('border=1 width=100', '')

        valid = '''<table border=1 width=100></table>'''
        self.assertEqual (result, valid)


    def testParser_empty_params_2 (self):
        text = '(:table border=1 width=100:)(:tableend:)'
        result = self.parser.toHtml (text)

        valid = '''<table border=1 width=100></table>'''
        self.assertEqual (result, valid)


    def testParser_suffix (self):
        text = '(:table2:)(:table2end:)'
        result = self.parser.toHtml (text)

        valid = '''<table></table>'''
        self.assertEqual (result, valid)


    def testParser_suffix_invalid (self):
        text = '(:table20:)(:table20end:)'
        result = self.parser.toHtml (text)

        valid = '''(:table20:)(:table20end:)'''
        self.assertEqual (result, valid)


    def testCommand_single_row_01 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:cell:)ааа(:cell:)ббб'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_single_row_02 (self):
        cmd = TableCommand (self.parser)
        text = '''(:cell:)ааа(:cell:)ббб'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_01 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:cell:)ааа(:cell:)ббб(:row:)(:cell:)ввв(:cell:)ггг'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_02 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:cell:)ааа(:cell:)ббб(:row:)(:cell:)ввв(:cell:)ггг(:cell:)'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td><td></td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_03 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:cell:)ааа(:cell:)ббб(:row:)(:cell:)ввв(:cell:)ггг(:row:)'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr><tr></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_04_params (self):
        cmd = TableCommand (self.parser)
        text = '''(:row rowparam=один:)(:cell cellparam=два:)ааа(:cell cellparam2=три cellparam3=четыре:)ббб(:row:)(:cell:)ввв(:cell:)ггг(:cell:)'''

        result = cmd.execute ('', text)

        valid = '''<table><tr rowparam=один><td cellparam=два>ааа</td><td cellparam2=три cellparam3=четыре>ббб</td></tr><tr><td>ввв</td><td>ггг</td><td></td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_05 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)
(:cell:)ааа
(:cell:)ббб
(:row:)
(:cell:)ввв
(:cell:)ггг'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_01 (self):
        text = '''(:table:)(:row:)(:cell:)ааа(:cell:)ббб(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_02 (self):
        text = '''(:table:)(:cell:)ааа(:cell:)ббб(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_03 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_04 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_05 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа(:cellend:)
(:cell:)ббб(:cellend:)
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_06 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа(:cellend:)ййй
(:cell:)ббб(:cellend:)ццц
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>аааййй</td><td>бббццц</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_single_row_07 (self):
        text = '''(:table:)
(:row:)
(:cell:)''ааа''(:cellend:)
(:cell:)ббб(:cellend:)
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td><i>ааа</i></td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_many_row_08 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)
(:cell:)ааа
(:cell:)ббб
(:rowend:)(:row:)
(:cell:)ввв
(:cell:)ггг
(:rowend:)'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><td>ббб</td></tr><tr><td>ввв</td><td>ггг</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_nested_01 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа(:table2:)(:table2end:)
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа<table></table></td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_nested_02 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа(:table2:)(:row2:)(:cell2:)111(:cell2:)222(:table2end:)
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа<table><tr><td>111</td><td>222</td></tr></table></td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_nested_03 (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа(:table2:)(:row2:)(:cell2:)111(:cell2:)222(:row2:)(:cell2:)Абырвалг(:cell2:)Главрыба(:table2end:)
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа<table><tr><td>111</td><td>222</td></tr><tr><td>Абырвалг</td><td>Главрыба</td></tr></table></td><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_hcell_01 (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:hcell:)ааа(:hcell:)ббб'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><th>ааа</th><th>ббб</th></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_hcell_02 (self):
        cmd = TableCommand (self.parser)
        text = '''(:hcell:)ааа(:hcell:)ббб'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><th>ааа</th><th>ббб</th></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_cell_hcell (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:cell:)ааа(:hcell:)ббб'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><td>ааа</td><th>ббб</th></tr></table>'''
        self.assertEqual (result, valid, result)


    def testCommand_hcell_cell (self):
        cmd = TableCommand (self.parser)
        text = '''(:row:)(:hcell:)ааа(:cell:)ббб'''

        result = cmd.execute ('', text)

        valid = '''<table><tr><th>ааа</th><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_cell_hcell (self):
        text = '''(:table:)
(:row:)
(:cell:)ааа
(:hcell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><td>ааа</td><th>ббб</th></tr></table>'''
        self.assertEqual (result, valid, result)


    def testParser_hcell_cell (self):
        text = '''(:table:)
(:row:)
(:hcell:)ааа
(:cell:)ббб
(:tableend:)'''
        result = self.parser.toHtml (text)

        valid = '''<table><tr><th>ааа</th><td>ббб</td></tr></table>'''
        self.assertEqual (result, valid, result)
