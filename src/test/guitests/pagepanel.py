#!/usr/bin/env python
# -*- coding: UTF-8 -*-


from basemainwnd import BaseMainWndTest
from core.tree import RootWikiPage, WikiDocument
from core.application import Application
from test.utils import removeWiki

from pages.text.textpage import TextPageFactory
from pages.text.TextPanel import TextPanel

from pages.html.htmlpage import HtmlPageFactory
from pages.html.HtmlPanel import HtmlPagePanel

from pages.wiki.wikipage import WikiPageFactory
from pages.wiki.wikipanel import WikiPagePanel

from pages.search.searchpage import SearchPageFactory
from pages.search.SearchPanel import SearchPanel


class PagePanelTest (BaseMainWndTest):
	"""
	Тесты окна со списком прикрепленных файлов
	"""
	def setUp (self):
		BaseMainWndTest.setUp (self)

		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.wikiroot = WikiDocument.create (self.path)

		TextPageFactory.create (self.wikiroot, u"Текстовая страница", [])
		HtmlPageFactory.create (self.wikiroot, u"HTML-страница", [])
		WikiPageFactory.create (self.wikiroot, u"Викистраница", [])
		SearchPageFactory.create (self.wikiroot, u"Поисковая страница", [])


	def tearDown (self):
		BaseMainWndTest.tearDown (self)
		Application.wikiroot = None
		removeWiki (self.path)


	def testEmpty (self):
		Application.wikiroot = self.wikiroot
		self.assertNotEqual (None, self.wnd.pagePanel)
		self.assertEqual (None, self.wnd.pagePanel.pageView)


	def testSelect (self):
		Application.wikiroot = self.wikiroot
		self.wikiroot.selectedPage = self.wikiroot[u"Текстовая страница"]
		self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))

		self.wikiroot.selectedPage = self.wikiroot[u"HTML-страница"]
		self.assertEqual (HtmlPagePanel, type (self.wnd.pagePanel.pageView))

		self.wikiroot.selectedPage = self.wikiroot[u"Викистраница"]
		self.assertEqual (WikiPagePanel, type (self.wnd.pagePanel.pageView))

		self.wikiroot.selectedPage = self.wikiroot[u"Поисковая страница"]
		self.assertEqual (SearchPanel, type (self.wnd.pagePanel.pageView))

		self.wikiroot.selectedPage = None
		self.assertEqual (None, self.wnd.pagePanel.pageView)


	def testLoadSelected (self):
		# Открытие вики с уже выбранной страницей
		self.wikiroot.selectedPage = self.wikiroot[u"Текстовая страница"]

		Application.wikiroot = self.wikiroot
		self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))


	def testReload (self):
		Application.wikiroot = self.wikiroot
		self.wikiroot.selectedPage = self.wikiroot[u"Текстовая страница"]
		self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))

		# "Закроем" вики
		Application.wikiroot = None
		self.assertEqual (None, self.wnd.pagePanel.pageView)

		# Откроем ее еще раз
		Application.wikiroot = self.wikiroot
		self.assertEqual (TextPanel, type (self.wnd.pagePanel.pageView))
