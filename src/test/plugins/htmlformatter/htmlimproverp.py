# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.htmlimproverfactory import HtmlImproverFactory


class ParagraphHtmlImproverTest (unittest.TestCase):
    def setUp (self):
        dirlist = [u"../plugins/htmlformatter"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        factory = HtmlImproverFactory (Application)
        self.improver = factory['pimprover']


    def tearDown (self):
        self.loader.clear()


    def test_empty (self):
        src = u''
        expectedResult = u''

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result)


    def test_text_single_line (self):
        src = u'Абырвалг'
        expectedResult = u'<p>Абырвалг</p>'

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result)


    def test_text_br (self):
        src = u'''Абырвалг
Foo
Bar'''
        expectedResult = u'''<p>Абырвалг<br/>
Foo<br/>
Bar</p>'''

        result = self.improver.run (src)

        self.assertEqual (expectedResult, result)


    def test_text_p_01 (self):
        src = u'''Абырвалг

Второй параграф'''

        expectedResult = u'''<p>Абырвалг</p>
<p>Второй параграф</p>'''

        result = self.improver.run (src)

        self.assertEqual (expectedResult, result)


    def test_text_p_02 (self):
        src = u'''Абырвалг

Второй параграф




'''

        expectedResult = u'''<p>Абырвалг</p>
<p>Второй параграф</p>'''

        result = self.improver.run (src)

        self.assertEqual (expectedResult, result)


    def test_improve_01 (self):
        src = ur"""<h2>Attach links</h2>Attach:file.odt<br/><a href="__attach/file.odt">file.odt</a><br/><a href="__attach/file.odt">alternative text</a><br/><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><h2>Images</h2>"""

        expectedResult = ur"""<h2>Attach links</h2>
<p>Attach:file.odt<br/>
<a href="__attach/file.odt">file.odt</a><br/>
<a href="__attach/file.odt">alternative text</a><br/>
<a href="__attach/file with spaces.pdf">file with spaces.pdf</a></p>
<h2>Images</h2>"""

        result = self.improver.run (src)

        self.assertEqual (expectedResult, result)


    def test_pre_01 (self):
        src = ur"""qweqweqw qweqwe
qwewqeqwe wqe

qweqweqw qwe qweqwe<pre>
аап ываыв ываываыываы ыва ыва
ываыва выа выа

ываыв фывфв фывфывыф ыфв
вапвапввап вапвапвап

вапвапвап вапваапва</pre>

sdfsdf sdfsdf
sdfsdf
sdf sdfsdf sdf"""

        expectedResult = ur"""<p>qweqweqw qweqwe<br/>
qwewqeqwe wqe</p>
<p>qweqweqw qwe qweqwe</p>

<pre>
аап ываыв ываываыываы ыва ыва
ываыва выа выа

ываыв фывфв фывфывыф ыфв
вапвапввап вапвапвап

вапвапвап вапваапва</pre>

<p>sdfsdf sdfsdf<br/>
sdfsdf<br/>
sdf sdfsdf sdf</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_02 (self):
        src = ur"""Абырвалг<pre><br/><h1>111</h1></pre>Абырвалг<pre><br/><h1>111</h1></pre>"""

        expectedResult = ur"""<p>Абырвалг</p>

<pre><br/><h1>111</h1></pre>

<p>Абырвалг</p>

<pre><br/><h1>111</h1></pre>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_03 (self):
        src = ur"""Абырвалг
<pre>111</pre>
Абырвалг
<pre>222</pre>"""

        expectedResult = ur"""<p>Абырвалг</p>

<pre>111</pre>

<p>Абырвалг</p>

<pre>222</pre>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_04 (self):
        src = ur"""Абырвалг
<   pre   >111
Абырвалг
йцукен</   pre   >
<pre>222</pre>"""

        expectedResult = ur"""<p>Абырвалг</p>

<   pre   >111
Абырвалг
йцукен</   pre   >

<pre>222</pre>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_01 (self):
        src = ur"""Абырвалг

<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        expectedResult = ur"""<p>Абырвалг</p>

<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_02 (self):
        src = ur"""Абырвалг
<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        expectedResult = ur"""<p>Абырвалг</p>

<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_03 (self):
        src = ur"""Абырвалг
<   script   >111
Абырвалг
йцукен</   script   >
<script>222</script>"""

        expectedResult = ur"""<p>Абырвалг</p>

<   script   >111
Абырвалг
йцукен</   script   >

<script>222</script>"""

        result = self.improver.run (src)

        self.assertEqual (expectedResult, result, result)


    def test_script_pre_01 (self):
        src = ur"""Абырвалг
<script>Абырвалг
<pre>
йцукен
qwerty
</pre>
фыва
</script>"""

        expectedResult = ur"""<p>Абырвалг</p>

<script>Абырвалг
<pre>
йцукен
qwerty
</pre>
фыва
</script>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_pre_02 (self):
        src = ur"""Абырвалг
<script>Абырвалг
<pre>
йцукен
qwerty
</pre>
фыва
</script>Абырвалг"""

        expectedResult = ur"""<p>Абырвалг</p>

<script>Абырвалг
<pre>
йцукен
qwerty
</pre>
фыва
</script>

<p>Абырвалг</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_blockquote_01 (self):
        src = ur"""<blockquote>Абырвалг</blockquote>"""

        expectedResult = ur"""<blockquote>
<p>Абырвалг</p>
</blockquote>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_blockquote_02 (self):
        src = ur"""Абзац 1<blockquote>Абырвалг</blockquote>Абзац 2"""

        expectedResult = ur"""<p>Абзац 1</p>
<blockquote>
<p>Абырвалг</p>
</blockquote>
<p>Абзац 2</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_blockquote_03 (self):
        src = ur"""Абзац 1

<blockquote>Абырвалг</blockquote>

Абзац 2"""

        expectedResult = ur"""<p>Абзац 1</p>
<blockquote>
<p>Абырвалг</p>
</blockquote>
<p>Абзац 2</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_blockquote_04 (self):
        src = ur"""Абзац 1

<blockquote>
Абырвалг
</blockquote>

Абзац 2"""

        expectedResult = ur"""<p>Абзац 1</p>
<blockquote>
<p>Абырвалг</p>
</blockquote>
<p>Абзац 2</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_table_01 (self):
        src = ur"""Абзац 1<table><tr><td>Ячейка таблицы</td></tr></table>Абзац 2"""

        expectedResult = ur"""<p>Абзац 1
<table>
<tr>
<td>Ячейка таблицы</td>
</tr>
</table>
Абзац 2</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_table_02 (self):
        src = ur"""Абзац 1
<table><tr><td>Ячейка таблицы</td></tr></table>
Абзац 2"""

        expectedResult = ur"""<p>Абзац 1
<table>
<tr>
<td>Ячейка таблицы</td>
</tr>
</table>
Абзац 2</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)


    def test_table_03 (self):
        src = ur"""Абзац 1

<table><tr><td>Ячейка таблицы</td></tr></table>
Абзац 2"""

        expectedResult = ur"""<p>Абзац 1</p>
<p>
<table>
<tr>
<td>Ячейка таблицы</td>
</tr>
</table>
Абзац 2</p>"""

        result = self.improver.run (src)
        self.assertEqual (expectedResult, result, result)
