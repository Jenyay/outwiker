# -*- coding: utf-8 -*-
"""
Модуль с классом диалога настроек
"""

import wx

from outwiker.core.exceptions import PreferencesException
from outwiker.core.application import Application


class PrefDialog(wx.Dialog):
    """
    Класс диалога настроек
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.__treeBook = wx.Treebook(self, -1)

        self.__do_layout()

        Application.onPreferencesDialogCreate(self)
        self.__expandAllPages()
        self.__treeBook.SetSelection(0)

        self.__loadAllOptions()
        self.__set_properties()

    @property
    def treeBook(self):
        """
        Возвращает указатель на дерево с панелями,
        который должен быть родителем для панелей с настройками
        """
        return self.__treeBook

    def appendPreferenceGroup(self, groupname, prefPanelsInfoList):
        """
        Добавить группу настроек
        groupname - имя группы
        prefPanelsInfoList - массив экземпляров класса PreferencePanelInfo

        Страница корня группы - первая страница в списке панелей.
        Массив не должен быть пустым
        """
        assert len(prefPanelsInfoList) != 0
        self.__treeBook.AddPage(prefPanelsInfoList[0].panel, groupname)

        # Если всего одна страница в списке,
        # то не будем добавлять вложенные страницы
        if len(prefPanelsInfoList) > 1:
            for panelInfo in prefPanelsInfoList:
                self.__treeBook.AddSubPage(panelInfo.panel, panelInfo.name)

        self.__expandAllPages()

    def __set_properties(self):
        width = 850
        height = 500

        self.SetTitle(_("Preferences"))
        self.__treeBook.SetMinSize((300, -1))

        self.Fit()
        fitWidth, fitHeight = self.GetSizeTuple()
        self.SetMinSize((fitWidth, fitHeight))
        self.SetSize((width, height))
        self.__centerWindow()

    def __centerWindow(self):
        """
        Расположить окно по центру родителя
        """
        selfWidth, selfHeight = self.GetSize()

        parentWidth, parentHeight = self.GetParent().GetSize()
        parentX, parentY = self.GetParent().GetPosition()

        posX = parentX + (parentWidth - selfWidth) / 2
        posY = parentY + (parentHeight - selfHeight) / 2

        self.SetPosition((posX, posY))

    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableCol(0)
        main_sizer.Add(self.__treeBook, 0, wx.ALL | wx.EXPAND, 4)

        self.__createOkCancelButtons(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()

    def __loadAllOptions(self):
        """
        Загрузить настройки для всех страниц
        """
        for pageIndex in range(self.__treeBook.GetPageCount()):
            page = self.__treeBook.GetPage(pageIndex)
            page.LoadState()

    def __expandAllPages(self):
        """
        Развернуть все узлы в дереве настроек
        """
        for pageindex in range(self.__treeBook.GetPageCount()):
            self.__treeBook.ExpandNode(pageindex)

    def __createOkCancelButtons(self, sizer):
        """
        Создать кнопки Ok / Cancel
        """
        buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(buttonsSizer,
                  0,
                  wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                  border=4)

        self.Bind(wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.__onCancel, id=wx.ID_CANCEL)

    def __onOk(self, event):
        try:
            self.__saveAll()
        except PreferencesException:
            pass

        Application.onPreferencesDialogClose(self)
        self.EndModal(wx.ID_OK)

    def __onCancel(self, event):
        Application.onPreferencesDialogClose(self)
        self.EndModal(wx.ID_CANCEL)

    def __saveCurrentPage(self):
        selectedPage = self.__treeBook.GetCurrentPage()

        if selectedPage is None:
            return

        # У страницы должен быть метод Save, который сохраняет настройки
        # или бросает исключение outwiker.core.exceptions.PreferencesException
        selectedPage.Save()

    def __saveAll(self):
        """
        Сохранить настройки для всех страниц
        """
        for pageIndex in range(self.__treeBook.GetPageCount()):
            page = self.__treeBook.GetPage(pageIndex)
            page.Save()
