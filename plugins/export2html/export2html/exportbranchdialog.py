# -*- coding: UTF-8 -*-

import wx

from .exportdialog import ExportDialog
from .branchexporter import BranchExporter
from .logdialog import LogDialog
from .longnamegenerator import LongNameGenerator
from .longprocessrunner import LongProcessRunner
from .titlenamegenerator import TitleNameGenerator


class ExportBranchDialog (ExportDialog):
    """
    Класс диалога для экспорта ветки страниц
    """
    def __init__ (self, application, rootpage):
        ExportDialog.__init__ (self, application.mainWindow, application.config)
        self.__rootpage = rootpage
        self.__application = application

        from .i18n import _
        global _

        self.__addNameFormatCheckBox ()
        self.Fit()
        self.Layout()

        self.longNames = self._config.longNames


    @property
    def longNames (self):
        """
        Создавать файлы с длинными именами (включать заголовки родителей)
        """
        return self.__longNameFormatCheckBox.GetValue()


    @longNames.setter
    def longNames (self, value):
        self.__longNameFormatCheckBox.SetValue (value)


    def __addNameFormatCheckBox (self):
        """
        Добавить чекбокс "Создавать файлы с длинными именами (включать заголовки родителей)"
        """
        self.__longNameFormatCheckBox = wx.CheckBox (self,
                                                     -1,
                                                     _(u"Use long file names (include parent name)"))

        self._mainSizer.Insert (4,
                                self.__longNameFormatCheckBox,
                                flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                                border=2)


    def __getNameGenerator (self):
        """
        Возвращает генератор имен для создаваемых страниц (длинные имена или короткие)
        """
        return LongNameGenerator (self.__rootpage) if self.longNames else TitleNameGenerator (self.path)


    def _threadExport (self, exporter, path, imagesOnly, overwrite):
        """
        Экспорт, выполняемый в отдельном потоке
        """
        return exporter.export (path, imagesOnly, overwrite)


    def _onOk (self):
        self._config.longNames = self.longNames
        self._config.imagesOnly = self.imagesOnly
        self._config.overwrite = self.overwrite

        namegenerator = self.__getNameGenerator()
        exporter = BranchExporter (self.__rootpage, namegenerator, self.__application)

        runner = LongProcessRunner (self._threadExport,
                                    self,
                                    _(u"Export to HTML"),
                                    _(u"Please wait..."))

        result = runner.run (exporter,
                             self.path,
                             self.imagesOnly,
                             self.overwrite)

        if len (result) != 0:
            logdlg = LogDialog (self, result)
            logdlg.ShowModal()
        else:
            self.EndModal (wx.ID_OK)
