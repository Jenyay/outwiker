# -*- coding: UTF-8 -*-

import os
import os.path
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeWiki


class DiagrammerTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/diagrammer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)

        self.thumbDir = u"__attach/__thumb"
        self.thumbFullPath = os.path.join (self.testPage.path, self.thumbDir)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]


    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)
        self.assertNotEqual (self.loader["Diagrammer"], None)


    def testEmpty (self):
        text = u"(:diagram:)(:diagramend:)"
        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 1)


    def test_simple (self):
        text = u"(:diagram:)Абырвалг -> Блаблабла(:diagramend:)"
        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 1)


    def test_double (self):
        text = u"""(:diagram:)Абырвалг -> Блаблабла(:diagramend:)
(:diagram:)Абыр -> валг -> Блаблабла(:diagramend:)"""

        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 2)


    def test_copy (self):
        text = u"""(:diagram:)Абырвалг -> Блаблабла(:diagramend:)
(:diagram:)Абырвалг -> Блаблабла(:diagramend:)"""

        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertIn (validResult, result)

        # Признак ошибки
        self.assertNotIn (u"<b>", result)

        self.assertTrue (os.path.exists (self.thumbFullPath))
        self.assertEqual (len (os.listdir(self.thumbFullPath)), 1)


    def testError (self):
        text = u"(:diagram:)a - b(:diagramend:)"
        validResult = u'<img src="{}/__diagram_'.format (self.thumbDir)

        result = self.parser.toHtml (text)
        self.assertNotIn (validResult, result)

        # Признак ошибки
        self.assertIn (u"<b>", result)

        # Папка для превьюшек все равно создается
        self.assertTrue (os.path.exists (self.thumbFullPath))
