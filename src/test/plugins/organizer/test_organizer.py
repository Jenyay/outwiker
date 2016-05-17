# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from outwiker.core.style import Style


class OrganizerTest (unittest.TestCase):
    """Organizer plug-in tests"""
    def setUp (self):
        self.__createWiki()

        dirlist = [u"../plugins/organizer"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        removeDir (self.path)
        self.loader.clear()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory().create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def test_empty (self):
        text = u'''(:org:)(:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'<table', result)
        self.assertEqual (self.testPage.tags, [])


    def test_add_tags_01 (self):
        text = u'''(:org:)
Теги: тег1
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'тег1', self.testPage.tags)


    def test_add_tags_02 (self):
        text = u'''(:org:)
Теги: тег 1, тег 2, тег 3
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'тег 1', self.testPage.tags)
        self.assertIn (u'тег 2', self.testPage.tags)
        self.assertIn (u'тег 3', self.testPage.tags)


    def test_add_tags_03 (self):
        text = u'''(:org:)
    Теги: тег 1, тег 2, тег 3
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'тег 1', self.testPage.tags)
        self.assertIn (u'тег 2', self.testPage.tags)
        self.assertIn (u'тег 3', self.testPage.tags)


    def test_add_tags_04 (self):
        text = u'''(:org:)
    Теги: тег 1, тег 2, тег 3
    Теги:   тег 4
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertNotIn (u'тег 1', self.testPage.tags)
        self.assertNotIn (u'тег 2', self.testPage.tags)
        self.assertNotIn (u'тег 3', self.testPage.tags)

        self.assertIn (u'тег 4', self.testPage.tags)


    def test_add_tags_05 (self):
        text = u'''(:org:)
    Теги: тег 1, тег 2, тег 3

    Теги:   тег 4
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'тег 1', self.testPage.tags)
        self.assertIn (u'тег 2', self.testPage.tags)
        self.assertIn (u'тег 3', self.testPage.tags)
        self.assertIn (u'тег 4', self.testPage.tags)


    def test_add_tags_06 (self):
        text = u'''(:org:)
    Описание: бла-бла-бла
    Теги: тег 1, тег 2, тег 3

    Описание: бла-бла-бла
    Теги:   тег 4
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'тег 1', self.testPage.tags)
        self.assertIn (u'тег 2', self.testPage.tags)
        self.assertIn (u'тег 3', self.testPage.tags)
        self.assertIn (u'тег 4', self.testPage.tags)


    def test_add_tags_07 (self):
        text = u'''(:org:)
    Description: бла-бла-бла
    Tags: тег 1, тег 2, тег 3

    Description: бла-бла-бла
    Tags:   тег 4

    Описание: бла-бла-бла
    Теги: тег 5
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertIn (u'тег 1', self.testPage.tags)
        self.assertIn (u'тег 2', self.testPage.tags)
        self.assertIn (u'тег 3', self.testPage.tags)
        self.assertIn (u'тег 4', self.testPage.tags)
        self.assertIn (u'тег 5', self.testPage.tags)


    def test_add_tags_08 (self):
        text = u'''(:org:)
    Description: бла-бла-бла
    Теги: -
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))

        self.assertNotIn (u'-', self.testPage.tags)


    def test_add_tags_09 (self):
        text = u'''(:org:)
    Description: бла-бла-бла
        (:orgend:)'''

        self.testPage.content = text

        generator = HtmlGenerator (self.testPage)
        result = generator.makeHtml (Style().getPageStyle (self.testPage))
        self.assertIn (u'<table', result)
