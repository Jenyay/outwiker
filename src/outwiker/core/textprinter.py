# -*- coding: utf-8 -*-

import html

import wx
import wx.html


class TextPrinter(object):
    """
    Интерфейс для печати текстовых страниц
    """
    def __init__(self, parent):
        self.parent = parent

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
        newtext = newtext.replace("\n", "<BR>")

        result = self.htmltemplate.format(content=newtext)
        return result

    def printout(self, text):
        printing = wx.GetApp().printing

        html = self._preparetext(text)
        printing.PrintText(html)
