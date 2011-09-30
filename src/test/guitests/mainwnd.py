#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.gui.MainWindow import MainWindow
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.pages.text.textpage import TextPageFactory

from .basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class MainWndTest(BaseMainWndTest):
	def setUp (self):
		BaseMainWndTest.setUp (self)

		self.path = u"../test/testwiki"
		removeWiki (self.path)

		self.rootwiki = WikiDocument.create (self.path)

		TextPageFactory.create (self.rootwiki, u"Страница 1", [])
		TextPageFactory.create (self.rootwiki, u"Страница 2", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
		TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
		TextPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])


	def tearDown (self):
		BaseMainWndTest.tearDown (self)
		Application.wikiroot = None
		removeWiki (self.path)


	def testProperties (self):
		self.assertNotEqual (None, self.wnd.tree)
		self.assertNotEqual (None, self.wnd.pagePanel)
		self.assertNotEqual (None, self.wnd.attachPanel)
		self.assertNotEqual (None, self.wnd.mainMenu)
		self.assertNotEqual (None, self.wnd.mainToolbar)
		self.assertNotEqual (None, self.wnd.statusbar)
		self.assertNotEqual (None, self.wnd.taskBarIcon)

		self.assertNotEqual (None, self.wnd.mainWindowConfig)
		self.assertNotEqual (None, self.wnd.treeConfig)
		self.assertNotEqual (None, self.wnd.attachConfig)
		self.assertNotEqual (None, self.wnd.generalConfig)


	def testTitle (self):
		conf = MainWindowConfig (Application.config)
		conf.titleFormatOption.value = u"OutWiker - {page} - {file}"

		Application.wikiroot = self.rootwiki
		self.assertEqual (self.wnd.GetTitle(), u"OutWiker -  - testwiki")

		self.rootwiki.selectedPage = self.rootwiki[u"Страница 1"]
		self.assertEqual (self.wnd.GetTitle(), u"OutWiker - Страница 1 - testwiki")

		self.rootwiki.selectedPage = self.rootwiki[u"Страница 2/Страница 3"]
		self.assertEqual (self.wnd.GetTitle(), u"OutWiker - Страница 3 - testwiki")

