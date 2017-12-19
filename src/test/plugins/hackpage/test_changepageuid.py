# -*- coding: UTF-8 -*-

import wx

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeDir
from outwiker.gui.tester import Tester


class HackPage_ChangePageUidTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)
        self._application = Application

        self.__createWiki()
        self.testPage = self.wikiroot["Страница 1"]
        self.testPage2 = self.wikiroot["Страница 2"]

        dirlist = ["../plugins/hackpage"]

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
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])
        WikiPageFactory().create(self.wikiroot, "Страница 2", [])

    def _setValue(self, dialog, value):
        dialog.Value = value
        return wx.ID_OK

    def test_UidDefault(self):
        from hackpage.utils import changeUidWithDialog

        Tester.dialogTester.appendOk()
        uid_old = Application.pageUidDepot.createUid(self.testPage)

        changeUidWithDialog(self.testPage, self._application)

        uid_new = Application.pageUidDepot.createUid(self.testPage)

        self.assertEqual(uid_old, uid_new)
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_change_uid_01(self):
        from hackpage.utils import changeUidWithDialog
        uid = 'dsfsfsfssg'

        Tester.dialogTester.append(self._setValue, uid)

        changeUidWithDialog(self.testPage, self._application)

        uid_new = Application.pageUidDepot.createUid(self.testPage)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(uid_new, uid)

    def test_change_uid_02(self):
        from hackpage.utils import changeUidWithDialog
        uid = '     dsfsfsfssg      '

        Tester.dialogTester.append(self._setValue, uid)

        changeUidWithDialog(self.testPage, self._application)

        uid_new = Application.pageUidDepot.createUid(self.testPage)

        self.assertEqual(Tester.dialogTester.count, 0)
        self.assertEqual(uid_new, uid.strip())

    def test_uid_validate_simple(self):
        from hackpage.validators import ChangeUidValidator
        Tester.dialogTester.appendOk()

        uid = 'dofiads7f89qwhrj'
        uidvalidator = ChangeUidValidator(self._application, self.testPage)

        self.assertTrue(uidvalidator(uid))
        self.assertEqual(Tester.dialogTester.count, 1)

    def test_uid_validate_underline(self):
        from hackpage.validators import ChangeUidValidator
        Tester.dialogTester.appendOk()

        uid = '__dofiads7f89qwhrj__'
        uidvalidator = ChangeUidValidator(self._application, self.testPage)

        self.assertTrue(uidvalidator(uid))
        self.assertEqual(Tester.dialogTester.count, 1)

    def test_uid_validate_russian(self):
        from hackpage.validators import ChangeUidValidator
        Tester.dialogTester.appendOk()

        uid = 'ывдратфыщшатф4е6'
        uidvalidator = ChangeUidValidator(self._application, self.testPage)

        self.assertTrue(uidvalidator(uid))
        self.assertEqual(Tester.dialogTester.count, 1)

    def test_uid_validate_error_spaces(self):
        from hackpage.validators import ChangeUidValidator
        Tester.dialogTester.appendOk()

        uid = 'dsfsf sfssgs'
        uidvalidator = ChangeUidValidator(self._application, self.testPage)

        self.assertFalse(uidvalidator(uid))
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_uid_validate_error_duplicate(self):
        from hackpage.validators import ChangeUidValidator
        Tester.dialogTester.appendOk()

        uid = Application.pageUidDepot.createUid(self.testPage2)
        uidvalidator = ChangeUidValidator(self._application, self.testPage)

        self.assertFalse(uidvalidator(uid))
        self.assertEqual(Tester.dialogTester.count, 0)

    def test_uid_validate_spaces_begin_end(self):
        from hackpage.validators import ChangeUidValidator
        Tester.dialogTester.appendOk()

        uid = '  dsfsfsfssgs  '
        uidvalidator = ChangeUidValidator(self._application, self.testPage)

        self.assertTrue(uidvalidator(uid))
        self.assertEqual(Tester.dialogTester.count, 1)
