# -*- coding: utf-8 -*-

from datetime import datetime

import wx

from outwiker.core.application import Application
from outwiker.core.utils import strftime_safe
from outwiker.gui.dateformatdialog import DateFormatDialog
from outwiker.gui.guiconfig import GeneralGuiConfig


def insertCurrentDate(parent, editor, application: Application) -> None:
    """
    Вызвать диалог для выбора формата даты и вставить в редактор текущую дату согласно выбранному формату.

    parent - родительское окно для диалога
    editor - текстовое поле ввода, куда надо вставить дату (экземпляр класса TextEditor)
    """
    config = GeneralGuiConfig(application.config)
    initial = config.recentDateTimeFormat.value

    with DateFormatDialog(
        parent, _("Enter format of the date"), _("Date format"), initial
    ) as dlg:
        if dlg.ShowModal() == wx.ID_OK:
            date_str = strftime_safe(datetime.now(), dlg.Value)
            editor.replaceText(date_str)
            config.recentDateTimeFormat.value = dlg.Value
