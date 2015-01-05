# -*- coding: UTF-8 -*-

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


class CommandPlotHighchartsTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/datagraph", u"../plugins/htmlheads"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.path = mkdtemp (prefix=u'Абырвалг абыр')
        self.wikiroot = WikiDocument.create (self.path)
        self.page = WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        Application.wikiroot = None

        self.parser = ParserFactory().make (self.page, Application.config)


    def tearDown (self):
        self.loader.clear()
        Application.wikiroot = None
        removeDir (self.path)


    def testEmpty (self):
        text = u'(:plot:)'

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        attachpath = Attachment (self.page).getAttachPath ()

        self.assertIn (u'<div id="graph-0" style="width:700px; height:300px;"></div>', result)
        self.assertIn (u'excanvas.min.js">', result)
        self.assertIn (u'jquery.min.js">', result)
        self.assertIn (u'highcharts.js">', result)
        self.assertIn (u"$('#graph-0').highcharts({", result)

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'excanvas.min.js')))

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'jquery.min.js')))

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'highcharts.js')))


    def testHeads_01 (self):
        text = u'''(:htmlhead:)
excanvas.min.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        attachpath = Attachment (self.page).getAttachPath ()

        self.assertIn (u'<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertNotIn (u'excanvas.min.js">', result)
        self.assertIn (u'jquery.min.js">', result)
        self.assertIn (u'highcharts.js">', result)

        self.assertIn (u"$('#graph-0').highcharts({", result)

        self.assertFalse (os.path.exists (os.path.join (attachpath,
                                                        u'__thumb',
                                                        u'__js',
                                                        u'excanvas.min.js')))

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'jquery.min.js')))

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'highcharts.js')))


    def testHeads_02 (self):
        text = u'''(:htmlhead:)
jquery.min.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        attachpath = Attachment (self.page).getAttachPath ()

        self.assertIn (u'<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertIn (u'excanvas.min.js">', result)
        self.assertNotIn (u'jquery.min.js">', result)
        self.assertIn (u'highcharts.js">', result)

        self.assertIn (u"$('#graph-0').highcharts({", result)

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'excanvas.min.js')))

        self.assertFalse (os.path.exists (os.path.join (attachpath,
                                                        u'__thumb',
                                                        u'__js',
                                                        u'jquery.min.js')))

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'highcharts.js')))


    def testHeads_03 (self):
        text = u'''(:htmlhead:)
highcharts.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        attachpath = Attachment (self.page).getAttachPath ()

        self.assertIn (u'<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertIn (u'excanvas.min.js">', result)
        self.assertIn (u'jquery.min.js">', result)
        self.assertNotIn (u'highcharts.js">', result)

        self.assertIn (u"$('#graph-0').highcharts({", result)

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'excanvas.min.js')))

        self.assertTrue (os.path.exists (os.path.join (attachpath,
                                                       u'__thumb',
                                                       u'__js',
                                                       u'jquery.min.js')))

        self.assertFalse (os.path.exists (os.path.join (attachpath,
                                                        u'__thumb',
                                                        u'__js',
                                                        u'highcharts.js')))


    def testHeads_04 (self):
        text = u'''(:htmlhead:)
excanvas.min.js
jquery.min.js
highcharts.js
(:htmlheadend:)
(:plot:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        attachpath = Attachment (self.page).getAttachPath ()

        self.assertIn (u'<div id="graph-0" style="width:700px; height:300px;"></div>', result)

        self.assertNotIn (u'excanvas.min.js">', result)
        self.assertNotIn (u'jquery.min.js">', result)
        self.assertNotIn (u'highcharts.js">', result)

        self.assertIn (u"$('#graph-0').highcharts({", result)

        self.assertFalse (os.path.exists (os.path.join (attachpath,
                                                        u'__thumb',
                                                        u'__js',
                                                        u'excanvas.min.js')))

        self.assertFalse (os.path.exists (os.path.join (attachpath,
                                                        u'__thumb',
                                                        u'__js',
                                                        u'jquery.min.js')))

        self.assertFalse (os.path.exists (os.path.join (attachpath,
                                                        u'__thumb',
                                                        u'__js',
                                                        u'highcharts.js')))


    def testData_01 (self):
        text = u'''(:plot:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn (text, result)


    def testData_02 (self):
        text = u'''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn (text, result)


    def testXCol_01 (self):
        text = u'''(:plot curve.xcol="number":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn (text, result)


    def testXCol_02 (self):
        text = u'''(:plot curve.xcol="  number  ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn (text, result)


    def testXCol_03 (self):
        text = u'''(:plot curve.xcol=10:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testXCol_04 (self):
        text = u'''(:plot curve.xcol=" 10 ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testXCol_05 (self):
        text = u'''(:plot curve.xcol=1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn (text, result)


    def testXCol_06 (self):
        text = u'''(:plot curve.xcol=2:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[10.0, 10.0], [20.0, 20.0], [30.0, 30.0], [40.0, 40.0]'

        self.assertIn (text, result)


    def testXCol_07 (self):
        text = u'''(:plot curve.xcol="0":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testXCol_08 (self):
        text = u'''(:plot curve.xcol="asdfasdf":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testYCol_01 (self):
        text = u'''(:plot curve.ycol=1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0.5, 0.5], [1.5, 1.5], [2.0, 2.0], [4.0, 4.0]'

        self.assertIn (text, result)


    def testYCol_02 (self):
        text = u'''(:plot curve.ycol=2:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn (text, result)


    def testYCol_03 (self):
        text = u'''(:plot curve.ycol=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testYCol_04 (self):
        text = u'''(:plot curve.ycol=3:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testYCol_05 (self):
        text = u'''(:plot curve.ycol=30:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testYCol_06 (self):
        text = u'''(:plot curve.ycol="абырвалг":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"data"', result)
        self.assertNotIn (u'"series"', result)


    def testYCol_07 (self):
        text = u'''(:plot curve.ycol=" 2  ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn (text, result)


    def testCurves_01 (self):
        text = u'''(:plot curve2.xcol="number":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'
        text2 = u'[0, 10.0], [1, 20.0], [2, 30.0], [3, 40.0]'

        self.assertIn (text1, result)
        self.assertIn (text2, result)


    def testAxis_01 (self):
        text = u'''(:plot:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'"text": null'

        self.assertIn (text, result)


    def testAxisTitle_01 (self):
        text = u'''(:plot x.title="Ось X" y.title="Ось Y":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"text": "\\u041e\\u0441\\u044c X"'
        text2 = u'"text": "\\u041e\\u0441\\u044c Y"'

        self.assertIn (text1, result)
        self.assertIn (text2, result)


    def testAxisTitle_02 (self):
        text = u'''(:plot x.title="Ось X":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"text": "\\u041e\\u0441\\u044c X"'
        text2 = u'"text": null'

        self.assertIn (text1, result)
        self.assertIn (text2, result)


    def testAxisMinMax_01 (self):
        text = u'''(:plot x.min=-2 x.max="5" y.min="-10" y.max="20":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"min": -2.0'
        text2 = u'"max": 5.0'
        text3 = u'"min": -10.0'
        text4 = u'"max": 20.0'

        self.assertIn (text1, result)
        self.assertIn (text2, result)
        self.assertIn (text3, result)
        self.assertIn (text4, result)


    def testAxisMinMax_02 (self):
        text = u'''(:plot:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"min"', result)
        self.assertNotIn (u'"max"', result)


    def testAxisMinMax_03 (self):
        text = u'''(:plot x.min=-2 x.max="Абырвалг":)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"min": -2.0'

        self.assertIn (text1, result)
        self.assertNotIn (u'"max"', result)


    def testAxisMinMax_04 (self):
        text = u'''(:plot x.min="Абырвалг" x.max=-2:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"max": -2.0'

        self.assertIn (text1, result)
        self.assertNotIn (u'"min"', result)


    def testAxisMinMax_05 (self):
        text = u'''(:plot x.min = -2.1 x.max = 2.3:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"min": -2.1'
        text2 = u'"max": 2.3'

        self.assertIn (text1, result)
        self.assertIn (text2, result)


    def testAxisMinMax_06 (self):
        text = u'''(:plot
x.min = -0.2
x.max = 0.2
:)
10
20
30
40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text1 = u'"min": -0.2'
        text2 = u'"max": 0.2'

        self.assertIn (text1, result)
        self.assertIn (text2, result)


    def testAxisDateTime_01 (self):
        text = u'''(:plot:)
01.01.2014    10
02.03.2014    20
29.05.2014    30
02.06.2015    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"type"', result)


    def testAxisDateTime_02 (self):
        text = u'''(:plot x.type="datetime":)
01.01.2014    10    01.02.1905
02.03.2014    20    05.12.1905
29.05.2014    30    06.05.1906
02.06.2015    40    17.10.1917
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"type": "datetime"', result)


    def testAxisDateTime_03 (self):
        text = u'''(:plot y.type="datetime":)
01.01.2014    10    01.02.1905
02.03.2014    20    05.12.1905
29.05.2014    30    06.05.1906
02.06.2015    40    17.10.1917
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"type": "datetime"', result)


    def testCurveColor_01 (self):
        text = u'''(:plot curve.color="#aabbcc" curve2.color="#001100":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"color": "#aabbcc"', result)
        self.assertIn (u'"color": "#001100"', result)


    def testGraphTitle_01 (self):
        text = u'''(:plot title="Abyrvalg":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"text": "Abyrvalg"', result)


    def testTooltip_01 (self):
        text = u'''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"tooltip": {"enabled": false}', result)


    def testTooltip_02 (self):
        text = u'''(:plot tooltip:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"tooltip": {"enabled": true}', result)


    def testTooltip_03 (self):
        text = u'''(:plot tooltip=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"tooltip": {"enabled": false}', result)


    def testTooltip_04 (self):
        text = u'''(:plot tooltip=42:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"tooltip": {"enabled": true}', result)


    def testCurveTitle_01 (self):
        text = u'''(:plot curve.title="abyrvalg":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"name": "abyrvalg"', result)


    def testLegend_01 (self):
        text = u'''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"legend": {"symbolWidth": 60, "enabled": false}', result)


    def testLegend_02 (self):
        text = u'''(:plot legend:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"legend": {"symbolWidth": 60, "enabled": true}', result)


    def testLegend_03 (self):
        text = u'''(:plot legend=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"legend": {"symbolWidth": 60, "enabled": false}', result)


    def testLegend_04 (self):
        text = u'''(:plot legend=42:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))
        self.assertIn (u'"legend": {"symbolWidth": 60, "enabled": true}', result)


    def testSkipRows_01 (self):
        text = u'''(:plot curve.data.skiprows="3":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[0.5, 10.0], [1.5, 20.0], [2.0, 30.0], [4.0, 40.0]'

        self.assertIn (text, result)


    def testSkipRows_02 (self):
        text = u'''(:plot curve.data.skiprows="6":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[4.0, 40.0]'

        self.assertIn (text, result)


    def testSkipRows_03 (self):
        text = u'''(:plot curve.data.skiprows="7":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[4.0, 40.0]'

        self.assertNotIn (text, result)


    def testSkipRows_04 (self):
        text = u'''(:plot curve.data.skiprows="70":)
Бла-бла-бла
Бла-бла
----
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        text = u'[4.0, 40.0]'

        self.assertNotIn (text, result)


    def testCurveHide_01 (self):
        text = u'''(:plot curve.title="abyrvalg" curve.hide :)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"name": "abyrvalg"', result)


    def testCurveHide_02 (self):
        text = u'''(:plot curve.title="abyrvalg" curve.hide = 0 :)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"name": "abyrvalg"', result)


    def testCurveStyle_01 (self):
        text = u'''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "solid"', result)


    def testCurveStyle_02 (self):
        text = u'''(:plot curve.style="Dot":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "dot"', result)


    def testCurveStyle_03 (self):
        text = u'''(:plot curve.style="  Dot  ":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "dot"', result)


    def testCurveStyle_04 (self):
        text = u'''(:plot curve.style=1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "solid"', result)


    def testCurveStyle_05 (self):
        text = u'''(:plot curve.style=5:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "shortdashdot"', result)


    def testCurveStyle_06 (self):
        text = u'''(:plot curve1.style=auto curve2.style=auto curve3.style=auto:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "solid"', result)
        self.assertIn (u'"dashStyle": "longdash"', result)
        self.assertIn (u'"dashStyle": "shortdash"', result)


    def testCurveStyle_07 (self):
        text = u'''(:plot curve.style=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "longdashdotdot"', result)


    def testCurveStyle_08 (self):
        text = u'''(:plot curve.style="-1":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "longdashdot"', result)


    def testCurveStyle_09 (self):
        text = u'''(:plot curve.style=12:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"dashStyle": "solid"', result)


    def testTickInterval_01 (self):
        text = u'''(:plot:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"tickInterval"', result)


    def testTickInterval_02 (self):
        text = u'''(:plot x.tickstep="":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"tickInterval"', result)


    def testTickInterval_03 (self):
        text = u'''(:plot x.tickstep="sadfasdf":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"tickInterval"', result)


    def testTickInterval_04 (self):
        text = u'''(:plot x.tickstep="1":)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'"tickInterval": 1.0', result)


    def testTickInterval_05 (self):
        text = u'''(:plot x.tickstep=-1:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"tickInterval"', result)


    def testTickInterval_06 (self):
        text = u'''(:plot x.tickstep=0:)
0.5    10
1.5    20
2.0    30
4.0    40
(:plotend:)'''

        self.page.content = text

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertNotIn (u'"tickInterval"', result)


    def testColSep_01 (self):
        text = u'''(:plot
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

        generator = HtmlGenerator (self.page)
        result = generator.makeHtml (Style().getPageStyle (self.page))

        self.assertIn (u'10.0', result)
        self.assertIn (u'18.0', result)
        self.assertIn (u'20.0', result)
