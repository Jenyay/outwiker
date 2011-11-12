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

        self.__treeBook.Bind (wx.EVT_TREEBOOK_PAGE_CHANGING, self.onPageChanging)
        self.__treeBook.Bind (wx.EVT_TREEBOOK_PAGE_CHANGED, self.onPageChanged)

        Application.onPreferencesDialogCreate (self)


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
        
        self._createOkCancelButtons(main_sizer)
        self.Layout()
    

    def __createPages (self):
        """
        Создать страницы окна настроек
        """
        self.__generalPage = GeneralPanel.GeneralPanel (self.__treeBook)
        self.__editorPage = EditorPanel.EditorPanel (self.__treeBook)
        self.__htmlRenderPage = HtmlRenderPanel.HtmlRenderPanel (self.__treeBook)
        self.__textPrintPage = TextPrintPanel.TextPrintPanel (self.__treeBook)
        self.__pluginsPage = PluginsPanel (self.__treeBook)

        self.__treeBook.AddPage (self.__generalPage, _(u"Interface"))
        self.__treeBook.AddSubPage (self.__generalPage, _(u"General"))
        self.__treeBook.AddSubPage (self.__editorPage, _(u"Editor"))
        self.__treeBook.AddSubPage (self.__htmlRenderPage, _(u"Preview"))
        self.__treeBook.AddSubPage (self.__textPrintPage, _(u"Text Printout"))
        self.__treeBook.AddPage (self.__pluginsPage, _(u"Plugins") )

        self._createPagesForPages()

        self.__expandAllPages()
        self.__treeBook.SetSelection (0)

        self.__generalPage.minimizeCheckBox.SetFocus()
    

    def _createPagesForPages (self):
        """
        Создать страницы настроек для типов страниц
        """
        for factory in FactorySelector.factories:
            pages = factory.getPrefPanels(self.__treeBook)

            if len (pages) > 0:
                self.__treeBook.AddPage (pages[0][1], factory.title)

                for page in pages:
                    self.__treeBook.AddSubPage (page[1], page[0])


    def __expandAllPages (self):
        """Развернуть все узлы в дереве настроек
        """
        for pageindex in range (self.__treeBook.GetPageCount()):
            self.__treeBook.ExpandNode (pageindex)


    def _createOkCancelButtons (self, sizer):
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


    def onPageChanging (self, event):
        try:
            self.__saveCurrentPage()
        except PreferencesException:
            event.Veto()


    def onPageChanged (self, event):
        pageIndex = event.GetSelection()

        if pageIndex == wx.NOT_FOUND:
            return

        selectedPage = self.__treeBook.GetPage (pageIndex)

        if selectedPage == None:
            return

        selectedPage.LoadState()
        selectedPage.SetFocus()
