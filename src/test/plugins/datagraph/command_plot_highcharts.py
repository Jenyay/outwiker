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
