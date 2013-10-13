#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx


class FontSizeSelector (object):
    """
    Класс для выбора размера шрифта
    """
    def __init__ (self, parentWnd):
        self._parentWnd = parentWnd

        self._fontSizeList = [u"20%", u"40%", u"60%", u"80%", u"120%", u"140%", u"160%", u"180%", u"200%"]
        self._fontSizeFormat = [(u"[----", u"----]"),
                (u"[---", u"---]"),
                (u"[--", u"--]"),
                (u"[-", u"-]"),
                (u"[+", u"+]"),
                (u"[++", u"++]"),
                (u"[+++", u"+++]"),
                (u"[++++", u"++++]"),
                (u"[+++++", u"+++++]")]


    def selectFontSize (self, selIndex):
        """
        Показать диалог с выбором размера шрифта.
        selIndex - первоначально выбранный индекс
        возвращает кортеж из тегов, которые форматируют текст под нужный размер, или None, если пользователь нажал на Отмену
        """
        dlg = wx.SingleChoiceDialog (self._parentWnd, 
                _(u"Select font size"),
                _(u"Font size"),
                self._fontSizeList)

        dlg.SetSelection (selIndex)
        result = None

        if dlg.ShowModal() == wx.ID_OK:
            sizeIndex = dlg.GetSelection()
            result = self._fontSizeFormat[sizeIndex]

        dlg.Destroy() 

        return result
