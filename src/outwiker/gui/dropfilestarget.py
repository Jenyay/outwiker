# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import wx

from outwiker.core.commands import attachFiles


class DropFilesTargetBase (wx.FileDropTarget):
    """
    Класс для возможности перетаскивания файлов
    между другими программами и OutWiker
    """
    __metaclass__ = ABCMeta

    def __init__(self, application, dropWnd):
        wx.FileDropTarget.__init__(self)
        self._application = application
        self._dropWnd = dropWnd
        self._dropWnd.SetDropTarget(self)

    def destroy(self):
        self._dropWnd.SetDropTarget(None)
        self._dropWnd = None

    @abstractmethod
    def OnDropFiles(self, x, y, files):
        pass


class DropFilesTarget (DropFilesTargetBase):
    def OnDropFiles(self, x, y, files):
        if (self._application.wikiroot is not None and
                self._application.wikiroot.selectedPage is not None):
            attachFiles(self._dropWnd,
                        self._application.wikiroot.selectedPage,
                        files)
            return True
