# -*- coding: utf-8 -*-

import html

import wx
import wx.html

from outwiker.gui.dialogs.messagebox import MessageBox
from outwiker.gui.guiconfig import TextPrintConfig


class TextPrinter:
    """
    Интерфейс для печати текстовых страниц
    """
    def __init__(self, parent, application):
        self.parent = parent

        self.config = TextPrintConfig(application.config)

        self.normalFont = self.config.fontName.value
        self.monoFont = self.config.fontName.value
        self.fontSizes = list(range(10, 17))

        # Поля на странице: верхнее, нижнее, левое, правое,
        # расстояние между шапкой/подвалом и текстом в мм
        headerspace = 0.0

        self.margins = (self.config.marginTop.value,
                        self.config.marginBottom.value,
                        self.config.marginLeft.value,
                        self.config.marginRight.value,
                        headerspace)

        self.paperId = self.config.paperId.value

        self.htmltemplate = r"""<HTML>
<HEAD>
    <META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>
</HEAD>
<BODY>
{content}
</BODY>
</HTML>"""

    def _preparetext(self, text):
        """
        Подготовить текст с учетом того, что печататься будет HTML
        """
        # Заменим спецсимволы HTML и установим переводы строк
        newtext = html.escape(text, True)
        newtext = newtext.replace("\n\n", "<P>")
        newtext = newtext.replace("\n", "<BR>")

        result = self.htmltemplate.format(content=newtext)
        return result

    def _getPrintout(self, htmltext):
        printout = wx.html.HtmlPrintout()
        printout.SetFonts(self.normalFont, self.monoFont, self.fontSizes)
        printout.SetMargins(self.margins[0],
                            self.margins[1],
                            self.margins[2],
                            self.margins[3],
                            self.margins[4])
        printout.SetHtmlText(htmltext)
        return printout

    def _getPrintData(self):
        """
        Получить параметры печати(страницы) по умолчанию
        """
        pd = wx.PrintData()
        pd.SetPaperId(self.paperId)
        pd.SetOrientation(wx.PORTRAIT)
        return pd

    def _getPrintDialogData(self, printdata):
        """
        Получить настройки диалога печати по умолчанию
        """
        pdd = wx.PrintDialogData(printdata)
        pdd.EnableSelection(False)
        return pdd

    def printout(self, text):
        htmltext = self._preparetext(text)
        printout = self._getPrintout(htmltext)
        pd = self._getPrintData()
        pdd = self._getPrintDialogData(pd)

        printer = wx.Printer(pdd)
        printer.Print(self.parent, printout, True)

        if printer.GetLastError() == wx.PRINTER_ERROR:
            MessageBox(_(u"Printing error"),
                       _(u"Error"),
                       wx.OK | wx.ICON_ERROR,
                       self.parent)
