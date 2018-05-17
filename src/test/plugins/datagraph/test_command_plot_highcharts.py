# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp
import os.path

from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.style import Style
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeDir


class CommandPlotHighchartsTest(unittest.TestCase):
    def setUp(self):
        dirlist = ["../plugins/datagraph", "../plugins/htmlheads"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.wikiroot = WikiDocument.create(self.path)
        self.page = WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        Application.wikiroot = None

        self.parser = ParserFactory().make(self.page, Application.config)

    def tearDown(self):
        self.loader.clear()
        Application.wikiroot = None
        removeDir(self.path)

    def testEmpty(self):
        text = '(:plot:)'

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        attachpath = Attachment(self.page).getAttachPath()

        self.assertIn('<div id="graph-0" style="width:700px; height:300px;"></div>', result)
        self.assertIn('excanvas.min.js">', result)
        self.assertIn('jquery.min.js">', result)
        self.assertIn('highcharts.js">', result)
        self.assertIn("$('#graph-0').highcharts({", result)

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'excanvas.min.js')))

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'jquery.min.js')))

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'highcharts.js')))

    def testHeads_01(self):
        text = '''(:htmlhead:)
excanvas.min.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        attachpath = Attachment(self.page).getAttachPath()

        self.assertIn('<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertNotIn('excanvas.min.js">', result)
        self.assertIn('jquery.min.js">', result)
        self.assertIn('highcharts.js">', result)

        self.assertIn("$('#graph-0').highcharts({", result)

        self.assertFalse(os.path.exists(os.path.join(attachpath,
                                                     '__thumb',
                                                     '__js',
                                                     'excanvas.min.js')))

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'jquery.min.js')))

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'highcharts.js')))

    def testHeads_02(self):
        text = '''(:htmlhead:)
jquery.min.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        attachpath = Attachment(self.page).getAttachPath()

        self.assertIn('<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertIn('excanvas.min.js">', result)
        self.assertNotIn('jquery.min.js">', result)
        self.assertIn('highcharts.js">', result)

        self.assertIn("$('#graph-0').highcharts({", result)

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'excanvas.min.js')))

        self.assertFalse(os.path.exists(os.path.join(attachpath,
                                                     '__thumb',
                                                     '__js',
                                                     'jquery.min.js')))

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'highcharts.js')))

    def testHeads_03(self):
        text = '''(:htmlhead:)
highcharts.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        attachpath = Attachment(self.page).getAttachPath()

        self.assertIn('<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertIn('excanvas.min.js">', result)
        self.assertIn('jquery.min.js">', result)
        self.assertNotIn('highcharts.js">', result)

        self.assertIn("$('#graph-0').highcharts({", result)

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'excanvas.min.js')))

        self.assertTrue(os.path.exists(os.path.join(attachpath,
                                                    '__thumb',
                                                    '__js',
                                                    'jquery.min.js')))

        self.assertFalse(os.path.exists(os.path.join(attachpath,
                                                     '__thumb',
                                                     '__js',
                                                     'highcharts.js')))

    def testHeads_04(self):
        text = '''(:htmlhead:)
excanvas.min.js
jquery.min.js
highcharts.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        attachpath = Attachment(self.page).getAttachPath()

        self.assertIn('<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertNotIn('excanvas.min.js">', result)
        self.assertNotIn('jquery.min.js">', result)
        self.assertNotIn('highcharts.js">', result)

        self.assertIn("$('#graph-0').highcharts({", result)

        self.assertFalse(os.path.exists(os.path.join(attachpath,
                                                     '__thumb',
                                                     '__js',
                                                     'excanvas.min.js')))

        self.assertFalse(os.path.exists(os.path.join(attachpath,
                                                     '__thumb',
                                                     '__js',
                                                     'jquery.min.js')))

        self.assertFalse(os.path.exists(os.path.join(attachpath,
                                                     '__thumb',
                                                     '__js',
                                                     'highcharts.js')))

    def testData_01(self):
        text = '''(:plot:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn(text, result)

    def testData_02(self):
        text = '''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn(text, result)

    def testXCol_01(self):
        text = '''(:plot curve.xcol="number":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn(text, result)

    def testXCol_02(self):
        text = '''(:plot curve.xcol="  number  ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn(text, result)

    def testXCol_03(self):
        text = '''(:plot curve.xcol=10:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testXCol_04(self):
        text = '''(:plot curve.xcol=" 10 ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testXCol_05(self):
        text = '''(:plot curve.xcol=1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn(text, result)

    def testXCol_06(self):
        text = '''(:plot curve.xcol=2:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[10.0, 10.0], [20.0, 20.0], [30.0, 30.0], [40.0, 40.0]'

        self.assertIn(text, result)

    def testXCol_07(self):
        text = '''(:plot curve.xcol="0":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testXCol_08(self):
        text = '''(:plot curve.xcol="asdfasdf":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testYCol_01(self):
        text = '''(:plot curve.ycol=1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0.5, 0.5], [1.5, 1.5], [2.0, 2.0], [4.0, 4.0]'

        self.assertIn(text, result)

    def testYCol_02(self):
        text = '''(:plot curve.ycol=2:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn(text, result)

    def testYCol_03(self):
        text = '''(:plot curve.ycol=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testYCol_04(self):
        text = '''(:plot curve.ycol=3:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testYCol_05(self):
        text = '''(:plot curve.ycol=30:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testYCol_06(self):
        text = '''(:plot curve.ycol="абырвалг":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"data"', result)
        self.assertNotIn('"series"', result)

    def testYCol_07(self):
        text = '''(:plot curve.ycol=" 2  ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn(text, result)

    def testCurves_01(self):
        text = '''(:plot curve2.xcol="number":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'
        text2 = '[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn(text1, result)
        self.assertIn(text2, result)

    def testAxis_01(self):
        text = '''(:plot:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '"text": null'

        self.assertIn(text, result)

    def testAxisTitle_01(self):
        text = '''(:plot x.title="Ось X" y.title="Ось Y":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"text": "\\u041e\\u0441\\u044c X"'
        text2 = '"text": "\\u041e\\u0441\\u044c Y"'

        self.assertIn(text1, result)
        self.assertIn(text2, result)

    def testAxisTitle_02(self):
        text = '''(:plot x.title="Ось X":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"text": "\\u041e\\u0441\\u044c X"'
        text2 = '"text": null'

        self.assertIn(text1, result)
        self.assertIn(text2, result)

    def testAxisMinMax_01(self):
        text = '''(:plot x.min=-2 x.max="5" y.min="-10" y.max="20":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"min": -2.0'
        text2 = '"max": 5.0'
        text3 = '"min": -10.0'
        text4 = '"max": 20.0'

        self.assertIn(text1, result)
        self.assertIn(text2, result)
        self.assertIn(text3, result)
        self.assertIn(text4, result)

    def testAxisMinMax_02(self):
        text = '''(:plot:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"min"', result)
        self.assertNotIn('"max"', result)

    def testAxisMinMax_03(self):
        text = '''(:plot x.min=-2 x.max="Абырвалг":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"min": -2.0'

        self.assertIn(text1, result)
        self.assertNotIn('"max"', result)

    def testAxisMinMax_04(self):
        text = '''(:plot x.min="Абырвалг" x.max=-2:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"max": -2.0'

        self.assertIn(text1, result)
        self.assertNotIn('"min"', result)

    def testAxisMinMax_05(self):
        text = '''(:plot x.min = -2.1 x.max = 2.3:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"min": -2.1'
        text2 = '"max": 2.3'

        self.assertIn(text1, result)
        self.assertIn(text2, result)

    def testAxisMinMax_06(self):
        text = '''(:plot
x.min = -0.2
x.max = 0.2
:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text1 = '"min": -0.2'
        text2 = '"max": 0.2'

        self.assertIn(text1, result)
        self.assertIn(text2, result)

    def testAxisDateTime_01(self):
        text = '''(:plot:)
01.01.2014    10
02.03.2014    20
29.05.2014    30
02.06.2015    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"type"', result)

    def testAxisDateTime_02(self):
        text = '''(:plot x.type="datetime":)
01.01.2014    10    01.02.1905
02.03.2014    20    05.12.1905
29.05.2014    30    06.05.1906
02.06.2015    40    17.10.1917
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"type": "datetime"', result)

    def testAxisDateTime_03(self):
        text = '''(:plot y.type="datetime":)
01.01.2014    10    01.02.1905
02.03.2014    20    05.12.1905
29.05.2014    30    06.05.1906
02.06.2015    40    17.10.1917
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"type": "datetime"', result)

    def testCurveColor_01(self):
        text = '''(:plot curve.color="#aabbcc" curve2.color="#001100":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"color": "#aabbcc"', result)
        self.assertIn('"color": "#001100"', result)

    def testGraphTitle_01(self):
        text = '''(:plot title="Abyrvalg":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"text": "Abyrvalg"', result)

    def testTooltip_01(self):
        text = '''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertIn('"tooltip": {"enabled": false}', result)

    def testTooltip_02(self):
        text = '''(:plot tooltip:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertIn('"tooltip": {"enabled": true}', result)

    def testTooltip_03(self):
        text = '''(:plot tooltip=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertIn('"tooltip": {"enabled": false}', result)

    def testTooltip_04(self):
        text = '''(:plot tooltip=42:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertIn('"tooltip": {"enabled": true}', result)

    def testCurveTitle_01(self):
        text = '''(:plot curve.title="abyrvalg":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"name": "abyrvalg"', result)

    def testLegend_01(self):
        text = '''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertTrue('"legend": {"enabled": false, "symbolWidth": 60}' in result or
                        '"legend": {"symbolWidth": 60, "enabled": false}' in result)

    def testLegend_02(self):
        text = '''(:plot legend:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertTrue('"legend": {"enabled": true, "symbolWidth": 60}' in result or
                        '"legend": {"symbolWidth": 60, "enabled": true}' in result)

    def testLegend_03(self):
        text = '''(:plot legend=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertTrue('"legend": {"enabled": false, "symbolWidth": 60}' in result or
                        '"legend": {"symbolWidth": 60, "enabled": false}' in result)

    def testLegend_04(self):
        text = '''(:plot legend=42:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))
        self.assertTrue('"legend": {"enabled": true, "symbolWidth": 60}' in result or
                        '"legend": {"symbolWidth": 60, "enabled": true}' in result)

    def testSkipRows_01(self):
        text = '''(:plot curve.data.skiprows="3":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn(text, result)

    def testSkipRows_02(self):
        text = '''(:plot curve.data.skiprows="6":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[4.0, 40.0]'

        self.assertIn(text, result)

    def testSkipRows_03(self):
        text = '''(:plot curve.data.skiprows="7":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[4.0, 40.0]'

        self.assertNotIn(text, result)

    def testSkipRows_04(self):
        text = '''(:plot curve.data.skiprows="70":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        text = '[4.0, 40.0]'

        self.assertNotIn(text, result)

    def testCurveHide_01(self):
        text = '''(:plot curve.title="abyrvalg" curve.hide :)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"name": "abyrvalg"', result)

    def testCurveHide_02(self):
        text = '''(:plot curve.title="abyrvalg" curve.hide = 0 :)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"name": "abyrvalg"', result)

    def testCurveStyle_01(self):
        text = '''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "solid"', result)

    def testCurveStyle_02(self):
        text = '''(:plot curve.style="Dot":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "dot"', result)

    def testCurveStyle_03(self):
        text = '''(:plot curve.style="  Dot  ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "dot"', result)

    def testCurveStyle_04(self):
        text = '''(:plot curve.style=1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "solid"', result)

    def testCurveStyle_05(self):
        text = '''(:plot curve.style=5:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "shortdashdot"', result)

    def testCurveStyle_06(self):
        text = '''(:plot curve1.style=auto curve2.style=auto curve3.style=auto:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "solid"', result)
        self.assertIn('"dashStyle": "longdash"', result)
        self.assertIn('"dashStyle": "shortdash"', result)

    def testCurveStyle_07(self):
        text = '''(:plot curve.style=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "longdashdotdot"', result)

    def testCurveStyle_08(self):
        text = '''(:plot curve.style="-1":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "longdashdot"', result)

    def testCurveStyle_09(self):
        text = '''(:plot curve.style=12:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"dashStyle": "solid"', result)

    def testTickInterval_01(self):
        text = '''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"tickInterval"', result)

    def testTickInterval_02(self):
        text = '''(:plot x.tickstep="":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"tickInterval"', result)

    def testTickInterval_03(self):
        text = '''(:plot x.tickstep="sadfasdf":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"tickInterval"', result)

    def testTickInterval_04(self):
        text = '''(:plot x.tickstep="1":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('"tickInterval": 1.0', result)

    def testTickInterval_05(self):
        text = '''(:plot x.tickstep=-1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"tickInterval"', result)

    def testTickInterval_06(self):
        text = '''(:plot x.tickstep=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertNotIn('"tickInterval"', result)

    def testColSep_01(self):
        text = '''(:plot
curve.data.colsep=",\s*"
:)
1, 10, 20, 30, 40
2, 11, 22, 31, 41
3, 13, 24, 33, 42
4, 15, 25, 35, 43
5, 16, 26, 36, 44
6, 18, 27, 37, 45
7, 20, 30, 38, 46
8, 20, 30, 38, 46
9, 20, 30, 38, 46
10, 20, 30, 38, 46
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('10.0', result)
        self.assertIn('18.0', result)
        self.assertIn('20.0', result)

    def testColSep_02(self):
        text = '''(:plot
curve.data.colsep=","
:)
1, 10, 20, 30, 40
2, 11, 22, 31, 41
3, 13, 24, 33, 42
4, 15, 25, 35, 43
5, 16, 26, 36, 44
6, 18, 27, 37, 45
7, 20, 30, 38, 46
8, 20, 30, 38, 46
9, 20, 30, 38, 46
10, 20, 30, 38, 46
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator(self.page)
        result = generator.makeHtml(Style().getPageStyle(self.page))

        self.assertIn('10.0', result)
        self.assertIn('18.0', result)
        self.assertIn('20.0', result)
