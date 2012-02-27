#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from .exportdialog import ExportDialog
from .branchexporter import BranchExporter
from .logdialog import LogDialog
from .longnamegenerator import LongNameGenerator
from .titlenamegenerator import TitleNameGenerator


class ExportBranchDialog (ExportDialog):
    """
    Класс диалога для экспорта ветки страниц
    """
    def __init__ (self, parent, rootpage):
        ExportDialog.__init__ (self, parent)
        self.__rootpage = rootpage

        from .i18n import _
        global _

        self.__addNameFormatCheckBox ()
        self.Fit()
        self.Layout()


    def __addNameFormatCheckBox (self):
        self.__longNameFormatCheckBox = wx.CheckBox (self, -1, _(u"Use long file names (include parent name)"))
        self._mainSizer.Insert (4, 
                self.__longNameFormatCheckBox, 
                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, 
                border=2)


    def __getNameGenerator (self):
        if self.__longNameFormatCheckBox.GetValue():
            return LongNameGenerator (self.__rootpage)
        else:
            return TitleNameGenerator (self.path)


    def _onOk (self):
        namegenerator = self.__getNameGenerator()
        exporter = BranchExporter (self.__rootpage, namegenerator)

        result = exporter.export (self.path,
                self.imagesOnly,
                self.overwrite)

        if len (result) != 0:
            logdlg = LogDialog (self, result)
            logdlg.ShowModal()
        else:
            self.EndModal (wx.ID_OK)
