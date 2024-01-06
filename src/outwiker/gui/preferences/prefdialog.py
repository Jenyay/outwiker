# -*- coding: utf-8 -*-
"""
Модуль с классом диалога настроек
"""

from typing import List, Optional

import wx

from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.treebook2 import Treebook2, BasePrefPanel


class PrefDialog(TestedDialog):
    """
    Класс диалога настроек
    """

    def __init__(self, parent, application):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super().__init__(parent, style=style)

        self._default_icon = getBuiltinImagePath("page.png")

        self._application = application
        self._treeBook = Treebook2(self, self._default_icon)
        self._do_layout()
        self._application.onPreferencesDialogCreate(self)

    def Destroy(self):
        self._treeBook.Clear()
        super().Destroy()

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

    def appendPreferenceGroup(
        self,
        groupname,
        prefPanelsInfoList,
        parent_page_tag: Optional[str] = None,
        icon_fname: Optional[str] = None,
    ):
        """
        Добавить группу настроек
        groupname - имя группы
        prefPanelsInfoList - массив экземпляров класса PreferencePanelInfo

        Страница корня группы - первая страница в списке панелей.
        Массив не должен быть пустым
        """
        assert len(prefPanelsInfoList) != 0
        self._treeBook.AddPage(
            prefPanelsInfoList[0].panel,
            groupname,
            tag=parent_page_tag,
            icon_fname=icon_fname,
        )

        # Если всего одна страница в списке,
        # то не будем добавлять вложенные страницы
        if len(prefPanelsInfoList) > 1:
            for panelInfo in prefPanelsInfoList:
                self._treeBook.AddPage(panelInfo.panel, panelInfo.name, parent_page_tag)

    def addPage(
        self,
        page: BasePrefPanel,
        label: str,
        parent_page_tag: Optional[str] = None,
        icon_fname=None,
        tag: Optional[str] = None,
    ):
        self._treeBook.AddPage(page, label, parent_page_tag, icon_fname, tag)

    def expandAll(self):
        self._treeBook.ExpandAll()

    def setSelection(self, tag: str):
        self._treeBook.SetSelection(tag)

    def getPages(self) -> List[BasePrefPanel]:
        return self._treeBook.GetPages()

    def _do_layout(self):
        self._treeBook.SetMinSize((300, 100))
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableCol(0)
        main_sizer.Add(self._treeBook, flag=wx.ALL | wx.EXPAND, border=4)

        self._createOkCancelButtons(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def _createOkCancelButtons(self, sizer):
        """
        Создать кнопки Ok / Cancel
        """
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL | wx.HELP)
        sizer.Add(buttonsSizer, flag=wx.EXPAND | wx.ALIGN_BOTTOM | wx.ALL, border=4)
