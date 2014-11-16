# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tree import WikiDocument

from outwiker.pages.html.htmlpage import HtmlPageFactory
from test.utils import removeDir


class HtmlPagesTest(unittest.TestCase):
    """
    Тесты HTML-страниц
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir (self.path)

        self.__eventcount = 0
        self.__eventSender = None

        self.wikiroot = WikiDocument.create (self.path)

        factory = HtmlPageFactory()
        factory.create (self.wikiroot, u"Страница 1", [])
        factory.create (self.wikiroot, u"Страница 2", [])

        self.wikiroot.onPageUpdate += self.__onPageUpdate


    def tearDown(self):
        self.wikiroot.onPageUpdate -= self.__onPageUpdate
        removeDir (self.path)


    def __onPageUpdate (self, sender, **kwargs):
        self.__eventcount += 1
        self.__eventSender = sender


    def testAutoLineWrap (self):
        self.assertTrue (self.wikiroot[u"Страница 1"].autoLineWrap)

        self.wikiroot[u"Страница 1"].autoLineWrap = False
        self.assertFalse (self.wikiroot[u"Страница 1"].autoLineWrap)


    def testAutoLineWrapReload (self):
        self.wikiroot[u"Страница 1"].autoLineWrap = False
        self.assertFalse (self.wikiroot[u"Страница 1"].autoLineWrap)

        wiki = WikiDocument.load (self.path)
        self.assertFalse (wiki[u"Страница 1"].autoLineWrap)


    def testAutoLineWrapRename (self):
        self.wikiroot[u"Страница 1"].autoLineWrap = False
        self.wikiroot[u"Страница 1"].title = u"Страница 666"
        self.assertFalse (self.wikiroot[u"Страница 666"].autoLineWrap)

        wiki = WikiDocument.load (self.path)
        self.assertFalse (wiki[u"Страница 666"].autoLineWrap)


    def testLineWrapEvent (self):
        self.wikiroot[u"Страница 1"].autoLineWrap = False

        self.assertEqual (self.__eventcount, 1)
        self.assertEqual (self.__eventSender, self.wikiroot[u"Страница 1"])
