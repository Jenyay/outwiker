# -*- coding: utf-8 -*-

from datetime import datetime

import wx

from outwiker.core.application import Application
from outwiker.gui.dateformatdialog import DateFormatDialog
from outwiker.gui.guiconfig import GeneralGuiConfig


def insertCurrentDate(parent, editor) -> None:
    """
    Вызвать диалог для выбора формата даты и вставить в редактор текущую дату согласно выбранному формату.

    parent - родительское окно для диалога
    editor - текстовое поле ввода, куда надо вставить дату (экземпляр класса TextEditor)
    """
    config = GeneralGuiConfig(Application.config)
    initial = config.recentDateTimeFormat.value

    with DateFormatDialog(parent,
                          _("Enter format of the date"),
                          _("Date format"),
                          initial) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            dateStr = datetime.now().strftime(dlg.Value)
            editor.replaceText(dateStr)
            config.recentDateTimeFormat.value = dlg.Value
