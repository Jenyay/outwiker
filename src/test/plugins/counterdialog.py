#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeWiki


class CounterDialogTest (BaseMainWndTest):
    """
    Тесты диалога для плагина Counter
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/counter"]

        self._loader = PluginsLoader(Application)
        self._loader.load (dirlist)

        self._dlg = self._loader["Counter"].InsertDialog (Application.mainWindow)
        self._dlg.SetModalResult (wx.ID_OK)

        self._controller = self._loader["Counter"].InsertDialogController (self._dlg, Application.config)


    def tearDown(self):
        BaseMainWndTest.tearDown (self)
        Application.wikiroot = None

        removeWiki (self.path)
        self._dlg.Destroy()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]


    def testDefault (self):
        result = self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (result, wx.ID_OK)
        self.assertEqual (self._dlg.counterName, u"")

        self.assertEqual (text, u'(:counter:)')


    def testSetEmptyName (self):
        self._dlg.counterName = u""

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetName (self):
        self._dlg.counterName = u"Имя счетчика"

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter name="Имя счетчика":)')
