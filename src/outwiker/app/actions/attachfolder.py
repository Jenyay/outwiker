# -*- coding: utf-8 -*-

import wx

from outwiker.app.services.attachment import attachFiles
from outwiker.core.treetools import testreadonly
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.system import getOS
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDirDialog


class AttachFolderAction(BaseAction):
    """
    Open dialog to select folder and attach selected folder
    """

    stringId = "AttachFolder"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Attach Folder…")

    @property
    def description(self):
        return _("Attach folder with files to current page")

    def run(self, params):
        assert self._application.mainWindow is not None

        if self._application.selectedPage is not None:
            self._attachFolderWithDialog(
                self._application.mainWindow, self._application.wikiroot.selectedPage
            )

    @testreadonly
    def _attachFolderWithDialog(self, parent, page):
        if page.readonly:
            raise ReadonlyException

        subdir = (
            page.currentAttachSubdir if self._application.selectedPage == page else None
        )

        with TestedDirDialog(
            parent, style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        ) as dlg:
            dlg.SetPath(getOS().documentsDir)
            if dlg.ShowModal() == wx.ID_OK:
                dirname = dlg.GetPath()
                attachFiles(parent, page, [dirname], subdir)


class AttachFolderActionForAttachPanel(AttachFolderAction):
    stringId = "AttachFolderForAttachPanel"
