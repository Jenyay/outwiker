# -*- coding: utf-8 -*-

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.tester import Tester
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUITest


class HackPage_ChangeTitleTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])
        self.testPage2 = WikiPageFactory().create(self.wikiroot,
                                                  "Страница 2",
                                                  [])

        dirlist = ["../plugins/hackpage"]

        self._loader = PluginsLoader(self.application)
        self._loader.load(dirlist)

        Tester.dialogTester.clear()

    def tearDown(self):
        Tester.dialogTester.clear()
        self.application.wikiroot = None

        removeDir(self.wikiroot.path)
        self._loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def _setValue(self, dialog, value):
        dialog.Value = value
        return wx.ID_OK

    def test_change_title_default_01(self):
        from hackpage.utils import setPageFolderWithDialog

        Tester.dialogTester.appendOk()

        setPageFolderWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(self.testPage.title, "Страница 1")
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_change_title_default_02(self):
        from hackpage.utils import setPageFolderWithDialog

        Tester.dialogTester.appendOk()
        self.testPage.alias = 'Псевдоним'

        setPageFolderWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, 'Псевдоним')
        self.assertEqual(self.testPage.title, "Страница 1")
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_change_title_cancel_01(self):
        from hackpage.utils import setPageFolderWithDialog

        Tester.dialogTester.appendCancel()
        self.testPage.alias = 'Псевдоним'

        setPageFolderWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, 'Псевдоним')
        self.assertEqual(self.testPage.title, "Страница 1")
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_change_title_cancel_02(self):
        from hackpage.utils import setPageFolderWithDialog

        Tester.dialogTester.appendCancel()
        self.testPage.alias = None

        setPageFolderWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(self.testPage.title, "Страница 1")
        self.assertEqual(Tester.dialogTester.count, 0)

    # def test_change_title_invalid_01(self):
    #     from hackpage.utils import setPageFolderWithDialog
    #
    #     self.testPage.alias = u'Псевдоним'
    #     Tester.dialogTester.append(self._setValue, u'')
    #     Tester.dialogTester.appendOk()
    #     Tester.dialogTester.appendCancel()
    #
    #     setPageFolderWithDialog(self.testPage, self.application)
    #
    #     self.assertEqual(self.testPage.alias, 'Псевдоним')
    #     self.assertEqual(self.testPage.title, u"Страница 1")
    #     self.assertEqual(Tester.dialogTester.count, 0)

    def test_change_title_01(self):
        from hackpage.utils import setPageFolderWithDialog

        old_title = self.testPage.title
        new_title = 'Новая папка'

        Tester.dialogTester.append(self._setValue, new_title)
        self.testPage.alias = None

        setPageFolderWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, old_title)
        self.assertEqual(self.testPage.title, new_title)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_change_title_02(self):
        from hackpage.utils import setPageFolderWithDialog

        new_title = 'Новая папка'

        Tester.dialogTester.append(self._setValue, new_title)
        self.testPage.alias = 'Псевдоним'

        setPageFolderWithDialog(self.testPage, self.application)

        self.assertEqual(self.testPage.alias, 'Псевдоним')
        self.assertEqual(self.testPage.title, new_title)
        self.assertEqual(Tester.dialogTester.count, 0)
