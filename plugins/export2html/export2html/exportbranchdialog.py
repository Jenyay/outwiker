#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.commands import MessageBox

from .exportdialog import ExportDialog
from .branchexporter import BranchExporter


class ExportBranchDialog (ExportDialog):
    """
    Класс диалога для экспорта одной страницы
    """
    def __init__ (self, parent, rootpage):
        ExportDialog.__init__ (self, parent)
        self.__rootpage = rootpage

        from .i18n import _
        global _


    def _onOk (self, event):
        exporter = BranchExporter (self.__rootpage)
        result = exporter.export (self.path,
                self.imagesOnly,
                self.overwrite)

        if len (result) != 0:
            MessageBox (u"\n".join (result), 
                _(u"Errors List"),
                wx.OK | wx.ICON_ERROR )
        else:
            self.EndModal (wx.ID_OK)
