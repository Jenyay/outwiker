# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.htmlimprover import BrHtmlImprover


class BrHtmlImproverTest (unittest.TestCase):
    def setUp (self):
        self.maxDiff = None


    def test1 (self):
        src = ur"""<h2>Attach links</h2>Attach:file.odt<br/><a href="__attach/file.odt">file.odt</a><br/><a href="__attach/file.odt">alternative text</a><br/><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><h2>Images</h2>"""

        expectedResult = ur"""<h2>Attach links</h2>
Attach:file.odt<br/>
<a href="__attach/file.odt">file.odt</a><br/>
<a href="__attach/file.odt">alternative text</a><br/>
<a href="__attach/file with spaces.pdf">file with spaces.pdf</a>
<h2>Images</h2>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result)


    def test_pre_01 (self):
        src = ur"""qweqweqw qweqwe<br/>qwewqeqwe wqe<p>qweqweqw qwe qweqwe<pre>
аап ываыв ываываыываы ыва ыва
ываыва выа выа

ываыв фывфв фывфывыф ыфв
вапвапввап вапвапвап

вапвапвап вапваапва</pre><p>sdfsdf sdfsdf<br/>sdfsdf<br/>sdf sdfsdf sdf"""

        expectedResult = ur"""qweqweqw qweqwe<br/>
qwewqeqwe wqe
<p>qweqweqw qwe qweqwe
<pre>
аап ываыв ываываыываы ыва ыва
ываыва выа выа

ываыв фывфв фывфывыф ыфв
вапвапввап вапвапвап

вапвапвап вапваапва</pre>

<p>sdfsdf sdfsdf<br/>
sdfsdf<br/>
sdf sdfsdf sdf"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_02 (self):
        src = ur"""Абырвалг<pre><br/><h1>111</h1></pre>Абырвалг<pre><br/><h1>111</h1></pre>"""

        expectedResult = ur"""Абырвалг
<pre><br/><h1>111</h1></pre>
Абырвалг
<pre><br/><h1>111</h1></pre>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_03 (self):
        src = ur"""Абырвалг
<pre>111</pre>
Абырвалг
<pre>222</pre>"""

        expectedResult = ur"""Абырвалг
<pre>111</pre>
Абырвалг
<pre>222</pre>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_04 (self):
        src = ur"""Абырвалг
<   pre   >111
Абырвалг
йцукен</   pre   >
<pre>222</pre>"""

        expectedResult = ur"""Абырвалг
<   pre   >111
Абырвалг
йцукен</   pre   >

<pre>222</pre>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_01 (self):
        src = ur"""Абырвалг<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        expectedResult = ur"""Абырвалг
<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_02 (self):
        src = ur"""Абырвалг
<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        expectedResult = ur"""Абырвалг
<script>Абырвалг
йцукен
qwerty
фыва
</script>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_03 (self):
        src = ur"""Абырвалг
<   script   >111
Абырвалг
йцукен</   script   >
<script>222</script>"""

        expectedResult = ur"""Абырвалг
<   script   >111
Абырвалг
йцукен</   script   >

<script>222</script>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_04 (self):
        src = ur"""Абырвалг<script>Абырвалг
йцукен
qwerty
фыва"""

        expectedResult = ur"""Абырвалг
<script>Абырвалг
йцукен
qwerty
фыва"""

        result = BrHtmlImprover().run (src)
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

        expectedResult = ur"""Абырвалг
<script>Абырвалг
<pre>
йцукен
qwerty
</pre>
фыва
</script>"""

        result = BrHtmlImprover().run (src)
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

        expectedResult = ur"""Абырвалг
<script>Абырвалг
<pre>
йцукен
qwerty
</pre>
фыва
</script>
Абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test3 (self):
        src = ur"""<H2>Attach links</H2>Attach:file.odt<br/><A HREF="__attach/file.odt">file.odt</A><br/><A HREF="__attach/file.odt">alternative text</A><br/><A HREF="__attach/file with spaces.pdf">file with spaces.pdf</A><H2>Images</H2>"""

        expectedResult = ur"""<H2>Attach links</H2>
Attach:file.odt<br/>
<A HREF="__attach/file.odt">file.odt</A><br/>
<A HREF="__attach/file.odt">alternative text</A><br/>
<A HREF="__attach/file with spaces.pdf">file with spaces.pdf</A>
<H2>Images</H2>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result)


    def test_br_01 (self):
        src = ur"""абырвалг<br/>абырвалг"""

        expectedResult = ur"""абырвалг<br/>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_br_02 (self):
        src = ur"""абырвалг<br />абырвалг"""

        expectedResult = ur"""абырвалг<br />
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_br_03 (self):
        src = ur"""абырвалг
абырвалг"""

        expectedResult = ur"""абырвалг<br/>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_br_04 (self):
        src = ur"""абырвалг

абырвалг"""

        expectedResult = ur"""абырвалг<br/>
<br/>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_br_05 (self):
        src = ur"""абырвалг<br/><br/>абырвалг"""

        expectedResult = ur"""абырвалг<br/>
<br/>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_br_06 (self):
        src = ur"""абырвалг



абырвалг"""

        expectedResult = ur"""абырвалг<br/>
<br/>
<br/>
<br/>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_hr_01 (self):
        src = ur"""абырвалг<hr>абырвалг"""

        expectedResult = ur"""абырвалг
<hr>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_hr_02 (self):
        src = ur"""абырвалг
<hr>
абырвалг"""

        expectedResult = ur"""абырвалг
<hr>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_p_01 (self):
        src = ur"""абырвалг<p>абырвалг</p>абырвалг"""

        expectedResult = ur"""абырвалг
<p>абырвалг</p>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_h_01 (self):
        src = ur"""абырвалг<h1>абырвалг</h1>абырвалг"""

        expectedResult = ur"""абырвалг
<h1>абырвалг</h1>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_h_02 (self):
        src = ur"""абырвалг
<h1>абырвалг</h1>
абырвалг"""

        expectedResult = ur"""абырвалг
<h1>абырвалг</h1>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_h_03 (self):
        src = ur"""абырвалг
<h1>абырвалг</h1>

абырвалг"""

        expectedResult = ur"""абырвалг
<h1>абырвалг</h1>
<br/>
абырвалг"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_list_01 (self):
        src = ur"""<ul><li>sadfasdf</li><li>asdfasdf</li><li>adsfasdf</li></ul>"""

        expectedResult = ur"""<ul>
<li>sadfasdf</li>
<li>asdfasdf</li>
<li>adsfasdf</li>
</ul>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_list_02 (self):
        src = ur"""<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>"""

        expectedResult = ur"""<ul>
<li>Несортированный список. Элемент 1</li>
<li>Несортированный список. Элемент 2</li>
<li>Несортированный список. Элемент 3</li>
<ol>
<li>Вложенный сортированный список. Элемент 1</li>
<li>Вложенный сортированный список. Элемент 2</li>
<li>Вложенный сортированный список. Элемент 3</li>
<li>Вложенный сортированный список. Элемент 4</li>
<ul>
<li>Совсем вложенный сортированный список. Элемент 1</li>
<li>Совсем вложенный сортированный список. Элемент 2</li>
</ul>
<li>Вложенный сортированный список. Элемент 5</li>
</ol>
<ul>
<li>Вложенный несортированный список. Элемент 1</li>
</ul>
</ul>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_list_03 (self):
        src = ur"""<UL><LI>Несортированный список. Элемент 1</LI><LI>Несортированный список. Элемент 2</LI><LI>Несортированный список. Элемент 3</LI><OL><LI>Вложенный сортированный список. Элемент 1</LI><LI>Вложенный сортированный список. Элемент 2</LI><LI>Вложенный сортированный список. Элемент 3</LI><LI>Вложенный сортированный список. Элемент 4</LI><UL><LI>Совсем вложенный сортированный список. Элемент 1</LI><LI>Совсем вложенный сортированный список. Элемент 2</LI></UL><LI>Вложенный сортированный список. Элемент 5</LI></OL><UL><LI>Вложенный несортированный список. Элемент 1</LI></UL></UL>"""

        expectedResult = ur"""<UL>
<LI>Несортированный список. Элемент 1</LI>
<LI>Несортированный список. Элемент 2</LI>
<LI>Несортированный список. Элемент 3</LI>
<OL>
<LI>Вложенный сортированный список. Элемент 1</LI>
<LI>Вложенный сортированный список. Элемент 2</LI>
<LI>Вложенный сортированный список. Элемент 3</LI>
<LI>Вложенный сортированный список. Элемент 4</LI>
<UL>
<LI>Совсем вложенный сортированный список. Элемент 1</LI>
<LI>Совсем вложенный сортированный список. Элемент 2</LI>
</UL>
<LI>Вложенный сортированный список. Элемент 5</LI>
</OL>
<UL>
<LI>Вложенный несортированный список. Элемент 1</LI>
</UL>
</UL>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result)


    def test_table_01 (self):
        src = ur'''<table><tr><td>Абырвалг</td><td>Абырвалг</td><td>Абырвалг</td></tr></table>'''
        expectedResult = u'''<table>
<tr>
<td>Абырвалг</td>
<td>Абырвалг</td>
<td>Абырвалг</td>
</tr>
</table>'''

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result)


    def test_empty (self):
        src = u""
        expectedResult = u""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_pre_only (self):
        src = u"<pre>Абырвалг</pre>"
        expectedResult = u"""<pre>Абырвалг</pre>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)


    def test_script_only (self):
        src = u"<script>Абырвалг</script>"
        expectedResult = u"""<script>Абырвалг</script>"""

        result = BrHtmlImprover().run (src)
        self.assertEqual (expectedResult, result, result)
