# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly, attachFiles
from outwiker.core.exceptions import ReadonlyException


class AttachFilesAction (BaseAction):
    """
    Вызвать диалог для выбора файлов, которые нужно прикрепить к странице
    """
    stringId = u"AttachFiles"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Attach Files…")

    @property
    def description(self):
        return _(u"Attach files to current page")

    def run(self, params):
        assert self._application.mainWindow is not None

        if self._application.selectedPage is not None:
            self._attachFilesWithDialog(
                self._application.mainWindow,
                self._application.wikiroot.selectedPage)

    @testreadonly
    def _attachFilesWithDialog(self, parent, page):
        """
        Вызвать диалог для приаттачивания файлов к странице
        parent - родительское окно
        page - страница, куда прикрепляем файлы
        """
        if page.readonly:
            raise ReadonlyException

        dlg = wx.FileDialog(
            parent,
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

        if dlg.ShowModal() == wx.ID_OK:
            files = dlg.GetPaths()
            files.sort()
            attachFiles(parent, page, files)

        dlg.Destroy()
