# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeWiki
from outwiker.gui.tester import Tester


class ChangePageUidTest (BaseMainWndTest):
    """Тесты плагина ChangePageUid"""
    def setUp (self):
        BaseMainWndTest.setUp (self)

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/changepageuid"]

        self._loader = PluginsLoader(Application)
        self._loader.load (dirlist)

        self._dlg = self._loader["ChangePageUID"].ChangeUidDialog (Application.mainWindow)
        Tester.dialogTester.clear()

        self.testPage = self.wikiroot[u"Страница 1"]


    def tearDown(self):
        Application.wikiroot = None

        removeWiki (self.path)
        self._dlg.Destroy()
        self._loader.clear()

        BaseMainWndTest.tearDown (self)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create (self.wikiroot, u"Страница 2", [])


    def testPluginLoad (self):
        self.assertEqual (len (self._loader), 1)


    def testDestroy (self):
        Application.wikiroot = None
        self._loader.clear()


    def testUidDefault (self):
        self._createDialogController()
        uid = Application.pageUidDepot.createUid (self.testPage)

        self.assertEqual (self._dlg.uid, uid)


    def testUid_01 (self):
        controller = self._createDialogController()
        uid = Application.pageUidDepot.createUid (self.testPage)

        # Не изменяем свой идентификатора
        self.assertEqual (len (controller.validate (uid)), 0)


    def testUid_02 (self):
        controller = self._createDialogController()
        uid = Application.pageUidDepot.createUid (self.wikiroot[u"Страница 2"])

        # Такой идентификатор уже есть
        self.assertNotEqual (len (controller.validate (uid)), 0)


    def testUid_03 (self):
        controller = self._createDialogController()

        self.assertEqual (len (controller.validate (u"asdfsdfasdf_124323")), 0)
        self.assertEqual (len (controller.validate (u"__Абырвалг")), 0)
        self.assertNotEqual (len (controller.validate (u"adfadf/")), 0)
        self.assertNotEqual (len (controller.validate (u"adfadf asdfasdf")), 0)


    def _createDialogController (self):
        return self._loader["ChangePageUID"].DialogController (Application, self._dlg, self.testPage)
