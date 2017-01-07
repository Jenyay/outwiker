# -*- coding: UTF-8 -*-

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeDir
from outwiker.gui.tester import Tester


class HackPage_ChangePageUidTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/hackpage"]

        self._loader = PluginsLoader(Application)
        self._loader.load(dirlist)

        from hackpage.dialog import ChangeUidDialog
        self._dlg = ChangeUidDialog(Application.mainWindow)
        Tester.dialogTester.clear()

        self.testPage = self.wikiroot[u"Страница 1"]

    def tearDown(self):
        Application.wikiroot = None

        removeDir(self.path)
        self._dlg.Destroy()
        self._loader.clear()

        BaseMainWndTest.tearDown(self)

    def __createWiki(self):
        WikiPageFactory().create(self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create(self.wikiroot, u"Страница 2", [])

    def testPluginLoad(self):
        self.assertEqual(len(self._loader), 1)

    def testDestroy(self):
        Application.wikiroot = None
        self._loader.clear()

    def testUidDefault(self):
        self._createDialogController()
        uid = Application.pageUidDepot.createUid(self.testPage)

        self.assertEqual(self._dlg.uid, uid)

    def testUid_01(self):
        controller = self._createDialogController()
        uid = Application.pageUidDepot.createUid(self.testPage)

        # Не изменяем свой идентификатора
        self.assertEqual(len(controller.validate(uid)), 0)

    def testUid_02(self):
        controller = self._createDialogController()
        uid = Application.pageUidDepot.createUid(self.wikiroot[u"Страница 2"])

        # Такой идентификатор уже есть
        self.assertNotEqual(len(controller.validate(uid)), 0)

    def testUid_03(self):
        controller = self._createDialogController()

        self.assertEqual(len(controller.validate(u"asdfsdfasdf_124323")), 0)
        self.assertEqual(len(controller.validate(u"__Абырвалг")), 0)
        self.assertNotEqual(len(controller.validate(u"adfadf/")), 0)
        self.assertNotEqual(len(controller.validate(u"adfadf asdfasdf")), 0)

    def _createDialogController(self):
        from hackpage.dialogcontroller import DialogController
        return DialogController(Application, self._dlg, self.testPage)
