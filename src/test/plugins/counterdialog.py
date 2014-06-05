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
        self.assertEqual (self._dlg.parentName, u"")
        self.assertEqual (self._dlg.separator, u".")
        self.assertEqual (self._dlg.reset, False)
        self.assertEqual (self._dlg.start, 1)
        self.assertEqual (self._dlg.step, 1)
        self.assertEqual (self._dlg.hide, False)

        self.assertEqual (text, u'(:counter:)')


    def testSetEmptyName_01 (self):
        self._dlg.counterName = u""

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetEmptyName_02 (self):
        self._dlg.counterName = u"    "

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetName (self):
        self._dlg.counterName = u"Имя счетчика"

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter name="Имя счетчика":)')


    def testSetParentEmptyName_01 (self):
        self._dlg.parentName = u""

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetParentEmptyName_02 (self):
        self._dlg.parentName = u"     "

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetParentName (self):
        self._dlg.parentName = u"Имя счетчика"

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter parent="Имя счетчика":)')


    def testSetSeparatorDefault (self):
        self._dlg.separator = u"."

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetSeparatorWithoutParent (self):
        self._dlg.separator = u":"

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testSetSeparatorWithParent_01 (self):
        self._dlg.separator = u":"
        self._dlg.parentName = u"Родительский счетчик"

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter parent="Родительский счетчик" separator=":":)')


    def testNotReset_01 (self):
        self._dlg.reset = False
        self._dlg.start = 0

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testNotReset_02 (self):
        self._dlg.reset = False
        self._dlg.start = 100

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testReset_01 (self):
        self._dlg.reset = True
        self._dlg.start = 0

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter start=0:)')


    def testReset_02 (self):
        self._dlg.reset = True
        self._dlg.start = -10

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter start=-10:)')


    def testReset_03 (self):
        self._dlg.reset = True
        self._dlg.start = 1

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter start=1:)')


    def testReset_04 (self):
        self._dlg.reset = True
        self._dlg.start = 10

        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter start=10:)')


    def testStep_01 (self):
        self._dlg.step = 1
        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testStep_02 (self):
        self._dlg.step = 0
        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter step=0:)')


    def testStep_03 (self):
        self._dlg.step = -10
        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter step=-10:)')


    def testStep_04 (self):
        self._dlg.step = 10
        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter step=10:)')


    def testHide_01 (self):
        self._dlg.hide = False
        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter:)')


    def testHide_02 (self):
        self._dlg.hide = True
        self._controller.showDialog()
        text = self._controller.getCommandString()

        self.assertEqual (text, u'(:counter hide:)')
