# -*- coding: utf-8 -*-
"""
Модуль с классом диалога настроек
"""

from typing import Optional

import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.treebook2 import Treebook2


class PrefDialog(TestedDialog):
    """
    Класс диалога настроек
    """

    def __init__(self, parent, application):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super().__init__(parent, style=style)

        self._default_icon = getBuiltinImagePath('page.png')

        self._application = application
        self._treeBook = Treebook2(self, self._default_icon)
        self._do_layout()
        self._application.onPreferencesDialogCreate(self)

    @property
    def treeBook(self):
        """
        Возвращает указатель на дерево с панелями,
        который должен быть родителем для панелей с настройками
        """
        return self._treeBook

    @property
    def pages(self):
        return self._treeBook.GetPages()

    @property
    def currentPage(self):
        return self._treeBook.GetCurrentPage()

    def appendPreferenceGroup(self, groupname, prefPanelsInfoList, parent_page_tag: Optional[str] = None):
        """
        Добавить группу настроек
        groupname - имя группы
        prefPanelsInfoList - массив экземпляров класса PreferencePanelInfo

        Страница корня группы - первая страница в списке панелей.
        Массив не должен быть пустым
        """
        assert len(prefPanelsInfoList) != 0
        self._treeBook.AddPage(prefPanelsInfoList[0].panel, groupname, tag=parent_page_tag)

        # Если всего одна страница в списке,
        # то не будем добавлять вложенные страницы
        if len(prefPanelsInfoList) > 1:
            for panelInfo in prefPanelsInfoList:
                self._treeBook.AddSubPage(panelInfo.panel, panelInfo.name, parent_page_tag)

    def _do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableCol(0)
        main_sizer.Add(self._treeBook, 0, wx.ALL | wx.EXPAND, 4)

        self._createOkCancelButtons(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def _createOkCancelButtons(self, sizer):
        """
        Создать кнопки Ok / Cancel
        """
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL | wx.HELP)
        sizer.Add(buttonsSizer,
                  0,
                  wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                  border=4)
