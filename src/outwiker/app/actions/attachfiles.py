# -*- coding: utf-8 -*-

import wx

from outwiker.app.services.attachment import attachFiles
from outwiker.core.treetools import testreadonly
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.system import getOS
from outwiker.gui.baseaction import BaseAction


class AttachFilesAction(BaseAction):
    """
    Вызвать диалог для выбора файлов, которые нужно прикрепить к странице
    """

    stringId = "AttachFiles"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Attach Files…")

    @property
    def description(self):
        return _("Attach files to current page")

    def run(self, params):
        assert self._application.mainWindow is not None

        if self._application.selectedPage is not None:
            self._attachFilesWithDialog(
                self._application.mainWindow, self._application.wikiroot.selectedPage
            )

    @testreadonly
    def _attachFilesWithDialog(self, parent, page):
        """
        Вызвать диалог для приаттачивания файлов к странице
        parent - родительское окно
        page - страница, куда прикрепляем файлы
        """
        if page.readonly:
            raise ReadonlyException

        subdir = (
            page.currentAttachSubdir if self._application.selectedPage == page else None
        )

        with wx.FileDialog(
            parent, style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE
        ) as dlg:
            dlg.SetDirectory(getOS().documentsDir)

            if dlg.ShowModal() == wx.ID_OK:
                files = dlg.GetPaths()
                files.sort()
                attachFiles(parent, page, files, subdir)


class AttachFilesActionForAttachPanel(AttachFilesAction):
    stringId = "AttachFilesForAttachPanel"
