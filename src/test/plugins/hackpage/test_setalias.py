# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeDir
from outwiker.gui.tester import Tester


class HackPage_SetAliasTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)
        self._application = Application

        self.__createWiki()
        self.testPage = self.wikiroot[u"Страница 1"]

        dirlist = [u"../plugins/hackpage"]

        self._loader = PluginsLoader(Application)
        self._loader.load(dirlist)

        Tester.dialogTester.clear()

    def tearDown(self):
        Tester.dialogTester.clear()
        Application.wikiroot = None

        removeDir(self.path)
        self._loader.clear()

        BaseMainWndTest.tearDown(self)

    def __createWiki(self):
        WikiPageFactory().create(self.wikiroot, u"Страница 1", [])
        WikiPageFactory().create(self.wikiroot, u"Страница 2", [])

    def _getFuncChangeDialogValue(self, value):
        def func(dialog):
            dialog.Value = value
            return wx.ID_OK

        return func

    def test_set_alias_default_01(self):
        from hackpage.utils import setAliasWithDialog

        Tester.dialogTester.appendOk()

        setAliasWithDialog(self.testPage, self._application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_default_02(self):
        from hackpage.utils import setAliasWithDialog

        Tester.dialogTester.appendCancel()

        setAliasWithDialog(self.testPage, self._application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_01(self):
        from hackpage.utils import setAliasWithDialog

        alias = u'Псевдоним страницы'

        Tester.dialogTester.append(self._getFuncChangeDialogValue(alias))

        setAliasWithDialog(self.testPage, self._application)

        self.assertEqual(self.testPage.alias, alias)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_02(self):
        from hackpage.utils import setAliasWithDialog

        alias = u'   Псевдоним страницы   '

        Tester.dialogTester.append(self._getFuncChangeDialogValue(alias))

        setAliasWithDialog(self.testPage, self._application)

        self.assertEqual(self.testPage.alias, alias)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_set_alias_03(self):
        from hackpage.utils import setAliasWithDialog

        self.testPage.alias = u'Псевдоним страницы'

        Tester.dialogTester.append(self._getFuncChangeDialogValue(''))

        setAliasWithDialog(self.testPage, self._application)

        self.assertEqual(self.testPage.alias, None)
        self.assertEqual(Tester.dialogTester.count, 0)
