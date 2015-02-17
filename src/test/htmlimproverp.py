# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.htmlimprover import ParagraphHtmlImprover


class ParagraphHtmlImproverTest (unittest.TestCase):
    def setUp (self):
        self.maxDiff = None


    def test_empty (self):
        src = u''
        expectedResult = u''

        result = ParagraphHtmlImprover().run (src)
        self.assertEqual (expectedResult, result)


    def test_text_single_line (self):
        src = u'Абырвалг'
        expectedResult = u'<p>Абырвалг</p>'

        result = ParagraphHtmlImprover().run (src)
        self.assertEqual (expectedResult, result)


    def test_text_br (self):
        src = u'''Абырвалг
Foo
Bar'''
        expectedResult = u'''<p>Абырвалг<br/>
Foo<br/>
Bar</p>'''

        result = ParagraphHtmlImprover().run (src)

        self.assertEqual (expectedResult, result)


    def test_text_p (self):
        src = u'''Абырвалг

Второй параграф'''

        expectedResult = u'''<p>Абырвалг</p>
<p>Второй параграф</p>'''

        result = ParagraphHtmlImprover().run (src)

        self.assertEqual (expectedResult, result)


    def test_improve_01 (self):
        src = ur"""<h2>Attach links</h2>Attach:file.odt<br/><a href="__attach/file.odt">file.odt</a><br/><a href="__attach/file.odt">alternative text</a><br/><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><h2>Images</h2>"""

        expectedResult = ur"""<h2>Attach links</h2>
<p>Attach:file.odt<br/>
<a href="__attach/file.odt">file.odt</a><br/>
<a href="__attach/file.odt">alternative text</a><br/>
<a href="__attach/file with spaces.pdf">file with spaces.pdf</a></p>
<h2>Images</h2>"""

        result = ParagraphHtmlImprover().run (src)

        self.assertEqual (expectedResult, result)
