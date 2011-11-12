# -*- coding: utf-8 -*-
"""
Модуль с классом диалога настроек
"""

import wx

import GeneralPanel
import EditorPanel
import HtmlRenderPanel
import TextPrintPanel
from pluginspanel import PluginsPanel

from outwiker.core.exceptions import PreferencesException
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.application import Application
from .preferencepanelinfo import PreferencePanelInfo


class PrefDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.THICK_FRAME
        wx.Dialog.__init__(self, *args, **kwds)
        self.__treeBook = wx.Treebook(self, -1)

        self.__set_properties()
        self.__do_layout()

        # Страницы с настройками
        self.__generalPage = None
        self.__editorPage = None
        self.__htmlRenderPage = None
        self.__textPrintPage = None
        self.__pluginsPage = None
        self.__createPages()

        self.__treeBook.Bind (wx.EVT_TREEBOOK_PAGE_CHANGING, self.__onPageChanging)
        self.__treeBook.Bind (wx.EVT_TREEBOOK_PAGE_CHANGED, self.__onPageChanged)

        Application.onPreferencesDialogCreate (self)


    def appendPreferenceGroup (self, groupname, panelsList):
        """
        Добавить группу настроек
        groupname - имя группы
        panels - массив экземпляров класса PreferencePanelInfo

        Страница корня группы - первая страница в списке панелей.
        Массив не должен быть пустым
        """
        assert len (panelsList) != 0
        self.__treeBook.AddPage (panelsList[0].panel, groupname)

        # Если всего одна страница в списке, то не будем добавлять вложенные страницы
        if len (panelsList) > 1:
            for panelInfo in panelsList:
                self.__treeBook.AddSubPage (panelInfo.panel, panelInfo.name)

        self.__expandAllPages()


    def __set_properties(self):
        self.SetTitle(_("Preferences"))
        self.SetSize((700, 500))
        self.__treeBook.SetMinSize((300, 400))


    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(2, 1, 0, 0)
        main_sizer.Add(self.__treeBook, 1, wx.ALL|wx.EXPAND, 4)
        self.SetSizer(main_sizer)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableCol(0)
        self.Layout()
        
        self.__createOkCancelButtons(main_sizer)
        self.Layout()
    

    def __createInterfacePages (self):
        """
        Создать страницы с подгруппой "Interface"
        """
        self.__generalPage = GeneralPanel.GeneralPanel (self.__treeBook)
        self.__editorPage = EditorPanel.EditorPanel (self.__treeBook)
        self.__htmlRenderPage = HtmlRenderPanel.HtmlRenderPanel (self.__treeBook)
        self.__textPrintPage = TextPrintPanel.TextPrintPanel (self.__treeBook)

        interfacePanelsList = [PreferencePanelInfo (self.__generalPage, _(u"General")),
                PreferencePanelInfo (self.__editorPage, _(u"Editor")),
                PreferencePanelInfo (self.__htmlRenderPage, _(u"Preview")),
                PreferencePanelInfo (self.__textPrintPage, _(u"Text Printout"))]

        self.appendPreferenceGroup (_(u"Interface"), interfacePanelsList)


    def __createPluginsPage (self):
        self.__pluginsPage = PluginsPanel (self.__treeBook)
        self.__treeBook.AddPage (self.__pluginsPage, _(u"Plugins") )


    def __createPages (self):
        """
        Создать страницы окна настроек
        """
        self.__createInterfacePages()
        self.__createPagesForPages()
        self.__createPluginsPage()

        self.__expandAllPages()
        self.__treeBook.SetSelection (0)

        self.__generalPage.minimizeCheckBox.SetFocus()
    

    def __createPagesForPages (self):
        """
        Создать страницы настроек для типов страниц
        """
        for factory in FactorySelector.factories:
            # Список экземпляров класса PreferencePanelInfo
            panelsList = factory.getPrefPanels(self.__treeBook)

            if len (panelsList) > 0:
                self.appendPreferenceGroup (factory.title, panelsList)


    def __expandAllPages (self):
        """
        Развернуть все узлы в дереве настроек
        """
        for pageindex in range (self.__treeBook.GetPageCount()):
            self.__treeBook.ExpandNode (pageindex)


    def __createOkCancelButtons (self, sizer):
        """
        Создать кнопки Ok / Cancel
        """
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        sizer.AddSpacer(0)
        sizer.Add (buttonsSizer, 1, wx.ALIGN_RIGHT | wx.ALL, border = 4)

        self.Bind (wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)
        self.Bind (wx.EVT_BUTTON, self.__onCancel, id=wx.ID_CANCEL)
        
        self.Layout()
    

    def __onOk (self, event):
        try:
            self.__saveCurrentPage()
        except PreferencesException:
            pass

        Application.onPreferencesDialogClose(self)
        self.EndModal (wx.ID_OK)


    def __onCancel (self, event):
        Application.onPreferencesDialogClose(self)
        self.EndModal(wx.ID_CANCEL)
    

    def __saveCurrentPage (self):
        selectedPage = self.__treeBook.GetCurrentPage()

        if selectedPage == None:
            return

        # У страницы должен быть метод Save, который сохраняет настройки 
        # или бросает исключение outwiker.core.exceptions.PreferencesException
        selectedPage.Save()


    def __onPageChanging (self, event):
        try:
            self.__saveCurrentPage()
        except PreferencesException:
            event.Veto()


    def __onPageChanged (self, event):
        pageIndex = event.GetSelection()

        if pageIndex == wx.NOT_FOUND:
            return

        selectedPage = self.__treeBook.GetPage (pageIndex)

        if selectedPage == None:
            return

        selectedPage.LoadState()
        selectedPage.SetFocus()
