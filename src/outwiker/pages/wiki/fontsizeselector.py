# -*- coding: UTF-8 -*-

import wx


class FontSizeSelector(object):
    """
    Класс для выбора размера шрифта
    """

    def __init__(self, parentWnd):
        self._parentWnd = parentWnd

        self._fontSizeList = [
            "20%",
            "40%",
            "60%",
            "80%",
            "120%",
            "140%",
            "160%",
            "180%",
            "200%",
        ]
        self._fontSizeFormat = [
            ("[----", "----]"),
            ("[---", "---]"),
            ("[--", "--]"),
            ("[-", "-]"),
            ("[+", "+]"),
            ("[++", "++]"),
            ("[+++", "+++]"),
            ("[++++", "++++]"),
            ("[+++++", "+++++]"),
        ]

    def selectFontSize(self, selIndex):
        """
        Показать диалог с выбором размера шрифта.
        selIndex - первоначально выбранный индекс
        возвращает кортеж из тегов, которые форматируют текст под нужный размер, или None, если пользователь нажал на Отмену
        """
        dlg = wx.SingleChoiceDialog(
            self._parentWnd, _("Select font size"), _("Font size"), self._fontSizeList
        )

        dlg.SetSelection(selIndex)
        result = None

        if dlg.ShowModal() == wx.ID_OK:
            sizeIndex = dlg.GetSelection()
            result = self._fontSizeFormat[sizeIndex]

        dlg.Destroy()

        return result
