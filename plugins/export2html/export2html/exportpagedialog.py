#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.core.commands import MessageBox

from .exportdialog import ExportDialog
from .exporterfactory import ExporterFactory


class ExportPageDialog (ExportDialog):
    """
    Класс диалога для экспорта одной страницы
    """
    def __init__ (self, parent, page):
        ExportDialog.__init__ (self, parent)
        self.__page = page


    def _onOk (self, event):
        try:
            exporter = ExporterFactory.getExporter (self.__page)

            exporter.export (self.path, 
                    self.imagesOnly, 
                    self.overwrite)

        except BaseException, error:
            MessageBox (str(error), 
                _(u"Error"),
                wx.OK | wx.ICON_ERROR )
            return

        self.EndModal (wx.ID_OK)
