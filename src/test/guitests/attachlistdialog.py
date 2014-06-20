# -*- coding: UTF-8 -*-

import wx

from basemainwnd import BaseMainWndTest
from outwiker.pages.wiki.actions.attachlist import AttachListDialog, AttachListDialogController
from outwiker.core.application import Application


class AttachListDialogTest (BaseMainWndTest):
    """
    Тесты диалога для вставки команды (:attachlist:)
    """
    def setUp (self):
        BaseMainWndTest.setUp (self)
        self._dialog = AttachListDialog (Application.mainWindow)


    def testCancel (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_CANCEL)
        result = controller.getDialogResult()

        self.assertEqual (result, None)


    def testSortByName (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 0
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=name:)")


    def testSortByNameDescend (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 0
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=descendname:)")


    def testSortByExt (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 1
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=ext:)")


    def testSortByExtDescend (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 1
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=descendext:)")


    def testSortBySize (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 2
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=size:)")


    def testSortBySizeDescend (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 2
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=descendsize:)")


    def testSortByDate (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 3
        self._dialog.isDescend = False

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=date:)")


    def testSortByDateDescend (self):
        controller = AttachListDialogController (self._dialog)

        self._dialog.SetModalResult (wx.ID_OK)
        self._dialog.selectedSort = 3
        self._dialog.isDescend = True

        result = controller.getDialogResult()

        self.assertEqual (result, u"(:attachlist sort=descenddate:)")
