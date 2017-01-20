# -*- coding: utf-8 -*-

import wx

from outwiker.core.commands import attachFiles


class DropFilesTarget (wx.FileDropTarget):
    """
    Класс для возможности перетаскивания файлов
    между другими программами и OutWiker
    """
    def __init__(self, application, dropWnd):
        wx.FileDropTarget.__init__(self)
        self._application = application
        self._dropWnd = dropWnd
        self._dropWnd.SetDropTarget(self)

    def OnDropFiles(self, x, y, files):
        if (self._application.wikiroot is not None and
                self._application.wikiroot.selectedPage is not None):
            attachFiles(self._dropWnd,
                        self._application.wikiroot.selectedPage,
                        files)
            return True

    def destroy(self):
        self._dropWnd.SetDropTarget(None)
        self._dropWnd = None
