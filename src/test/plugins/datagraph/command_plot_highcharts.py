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
        dirlist = [u"../plugins/datagraph"]

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

        self.assertIn (u'<div id="graph-0" style="width:700px; height:400px;"></div>', result)
        self.assertIn (u'excanvas.js', result)
        self.assertIn (u'jquery.min.js', result)
        self.assertIn (u'highcharts.js', result)
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
