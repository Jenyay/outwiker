# -*- coding: utf-8 -*-
"""
Модуль с классом диалога настроек
"""

import wx

from generalpanel import GeneralPanel
from editorpanel import EditorPanel
from htmlrenderpanel import HtmlRenderPanel
from textprintpanel import TextPrintPanel
from pluginspanel import PluginsPanel
from hotkeyspanel import HotKeysPanel
from htmleditorpanel import HtmlEditorPanel
from wikieditorpanel import WikiEditorPanel
from iconsetpanel import IconsetPanel

from outwiker.core.exceptions import PreferencesException
from outwiker.core.factoryselector import FactorySelector
from outwiker.core.application import Application
from .preferencepanelinfo import PreferencePanelInfo


class PrefDialog(wx.Dialog):
    """
    Класс диалога настроек
    """
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
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
        self.__hotkeysPage = None
        self.__htmlEditorPage = None
        self.__iconsetPage = None
        self.__createPages()

        Application.onPreferencesDialogCreate (self)

        self.__loadAllOptions()
        self.Center(wx.CENTRE_ON_SCREEN)


    @property
    def treeBook (self):
        """
        Возвращает указатель на дерево с панелями, который должен быть родителем для панелей с настройками
        """
        return self.__treeBook


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
        title = _("Preferences")
        self.SetTitle(title)

        width = 800
        height = 500

        self.SetSize((width, height))
        self.__treeBook.SetMinSize((300, 400))

        self.__centerWindow()


    def __centerWindow (self):
        """
        Расположить окно по центру родителя
        """
        selfWidth, selfHeight = self.GetSize()

        parentWidth, parentHeight = self.GetParent().GetSize()
        parentX, parentY = self.GetParent().GetPosition()

        posX = parentX + (parentWidth - selfWidth) / 2
        posY = parentY + (parentHeight - selfHeight) / 2

        self.SetPosition ((posX, posY))


    def __do_layout(self):
        main_sizer = wx.FlexGridSizer(rows=2)
        main_sizer.AddGrowableRow(0)
        main_sizer.AddGrowableCol(0)
        main_sizer.Add(self.__treeBook, 1, wx.ALL | wx.EXPAND, 4)

        self.__createOkCancelButtons(main_sizer)

        self.SetSizer(main_sizer)
        self.Layout()


    def __createInterfaceGroup (self):
        """
        Создать страницы с подгруппой "Interface"
        """
        self.__generalPage = GeneralPanel (self.__treeBook)
        self.__htmlRenderPage = HtmlRenderPanel (self.__treeBook)
        self.__textPrintPage = TextPrintPanel (self.__treeBook)

        interfacePanelsList = [PreferencePanelInfo (self.__generalPage, _(u"General")),
                               PreferencePanelInfo (self.__htmlRenderPage, _(u"Preview")),
                               PreferencePanelInfo (self.__textPrintPage, _(u"Text Printout"))]

        self.appendPreferenceGroup (_(u"Interface"), interfacePanelsList)


    def __createEditorGroup (self):
        """
        Создать страницы с подгруппой "Редактор"
        """
        self.__editorPage = EditorPanel (self.__treeBook)
        self.__htmlEditorPage = HtmlEditorPanel (self.__treeBook)
        self.__wikiEditorPage = WikiEditorPanel (self.__treeBook)

        editorPanesList = [
            PreferencePanelInfo (self.__editorPage, _(u"General")),
            PreferencePanelInfo (self.__htmlEditorPage, _(u"HTML Editor")),
            PreferencePanelInfo (self.__wikiEditorPage, _(u"Wiki Editor")),
        ]

        self.appendPreferenceGroup (_(u"Editor"), editorPanesList)


    def __createPluginsPage (self):
        self.__pluginsPage = PluginsPanel (self.__treeBook)
        self.__treeBook.AddPage (self.__pluginsPage, _(u"Plugins"))


    def __createHotKeysPage (self):
        self.__hotkeysPage = HotKeysPanel (self.__treeBook)
        self.__treeBook.AddPage (self.__hotkeysPage, _(u"Hotkeys"))


    def __createIconsetPage (self):
        self.__iconsetPage = IconsetPanel (self.__treeBook)
        self.__treeBook.AddPage (self.__iconsetPage, _(u"User's iconset"))


    def __createPages (self):
        """
        Создать страницы окна настроек
        """
        self.__createInterfaceGroup ()
        self.__createEditorGroup ()
        self.__createPagesForPages ()
        self.__createIconsetPage ()
        self.__createPluginsPage ()
        self.__createHotKeysPage ()

        self.__expandAllPages()
        self.__treeBook.SetSelection (0)

        self.__generalPage.minimizeCheckBox.SetFocus()


    def __loadAllOptions (self):
        """
        Загрузить настройки для всех страниц
        """
        for pageIndex in range (self.__treeBook.GetPageCount()):
            page = self.__treeBook.GetPage (pageIndex)
            page.LoadState()


    def __createPagesForPages (self):
        """
        Создать страницы настроек для типов страниц
        """
        for factory in FactorySelector.getFactories():
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
            # self.__saveCurrentPage()
            self.__saveAll()
        except PreferencesException:
            pass

        Application.onPreferencesDialogClose(self)
        self.EndModal (wx.ID_OK)


    def __onCancel (self, event):
        Application.onPreferencesDialogClose(self)
        self.EndModal(wx.ID_CANCEL)


    def __saveCurrentPage (self):
        selectedPage = self.__treeBook.GetCurrentPage()

        if selectedPage is None:
            return

        # У страницы должен быть метод Save, который сохраняет настройки
        # или бросает исключение outwiker.core.exceptions.PreferencesException
        selectedPage.Save()


    def __saveAll (self):
        """
        Сохранить настройки для всех страниц
        """
        for pageIndex in range (self.__treeBook.GetPageCount()):
            page = self.__treeBook.GetPage (pageIndex)
            page.Save()


    def __onPageChanged (self, event):
        pageIndex = event.GetSelection()

        if pageIndex == wx.NOT_FOUND:
            return

        selectedPage = self.__treeBook.GetPage (pageIndex)

        if selectedPage is None:
            return

        # selectedPage.LoadState()
        selectedPage.SetFocus()
