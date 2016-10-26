# -*- coding: utf-8 -*-

from __future__ import print_function
from abc import ABCMeta, abstractmethod
import os

import wx
import wx.lib.newevent

from outwiker.actions.search import SearchAction, SearchNextAction, SearchPrevAction, SearchAndReplaceAction
from outwiker.actions.attachfiles import AttachFilesAction
from outwiker.actions.globalsearch import GlobalSearchAction
from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.system import getImagesDir
from outwiker.core.attachment import Attachment
from outwiker.core.config import IntegerOption
from outwiker.core.events import PageUpdateNeededParams
from outwiker.core.system import getOS
from outwiker.utilites.textfile import readTextFile
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.guiconfig import GeneralGuiConfig

# Событие вызывается, когда переключаются вкладки страницы (код, HTML, ...)
PageTabChangedEvent, EVT_PAGE_TAB_CHANGED = wx.lib.newevent.NewEvent()


class BaseHtmlPanel(BaseTextPanel):
    __metaclass__ = ABCMeta

    # Номера страниц-вкладок
    CODE_PAGE_INDEX = 0
    RESULT_PAGE_INDEX = 1


    def __init__(self, parent, application):
        super (BaseHtmlPanel, self).__init__ (parent, application)

        # Предыдущее содержимое результирующего HTML, чтобы не переписывать
        # его каждый раз
        self._oldHtmlResult = u""

        # Страница, для которой уже есть сгенерированный HTML
        self._oldPage = None

        # Где хранить параметы текущей страницы страницы (код, просмотр и т.д.)
        self.tabSectionName = u"Misc"
        self.tabParamName = u"PageIndex"

        self._statusbar_item = 0

        self.imagesDir = getImagesDir()

        self.notebook = wx.Notebook(self, -1, style=wx.NB_BOTTOM)
        self._codeEditor = self.getTextEditor()(self.notebook)

        self.htmlWindow = getOS().getHtmlRender (self.notebook)

        self.__do_layout()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self._onTabChanged, self.notebook)
        self.Bind (self.EVT_SPELL_ON_OFF, handler=self._onSpellOnOff)
        self._application.onPageUpdate += self._onPageUpdate

    def Clear (self):
        self.Unbind(wx.EVT_NOTEBOOK_PAGE_CHANGED, source=self.notebook, handler=self._onTabChanged)
        self.Unbind (self.EVT_SPELL_ON_OFF, handler=self._onSpellOnOff)
        self._application.onPageUpdate -= self._onPageUpdate

        super (BaseHtmlPanel, self).Clear()


    def SetCursorPosition (self, position):
        """
        Установить курсор в текстовом редакторе в положение position
        """
        self.codeEditor.SetSelection(position, position)
        self.codeEditor.ScrollLineToCursor()

    def GetCursorPosition (self):
        """
        Возвращает положение курсора в текстовом редакторе
        """
        return self.codeEditor.GetCurrentPosition()

    def GetEditor(self):
        return self._codeEditor

    @property
    def codeEditor (self):
        return self._codeEditor


    def addTool (self,
                 menu,
                 idstring,
                 func,
                 menuText,
                 buttonText,
                 image,
                 alwaysEnabled=False,
                 fullUpdate=True,
                 panelname="plugins"):
        """
        !!! Внимание. Это устаревший способ добавления элементов интерфейса.
        Сохраняется только для совместимости со старыми версиями плагинов
        и в будущих версиях программы может быть убран.

        Добавить пункт меню и кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        """
        super (BaseHtmlPanel, self).addTool (menu,
                                             idstring,
                                             func,
                                             menuText,
                                             buttonText,
                                             image,
                                             alwaysEnabled,
                                             fullUpdate,
                                             panelname)

        tool = self._tools[idstring]
        self.enableTool (tool, self._isEnabledTool (tool))


    def Print (self):
        currpanel = self.notebook.GetCurrentPage()
        if currpanel is not None:
            currpanel.Print()


    @abstractmethod
    def getTextEditor(self):
        pass


    @property
    def selectedPageIndex (self):
        """
        Возвращает номер выбранной страницы (код или просмотр)
        """
        return self.notebook.GetSelection()


    @selectedPageIndex.setter
    def selectedPageIndex (self, index):
        """
        Устанавливает выбранную страницу (код или просмотр)
        """
        if index >= 0 and index < self.pageCount:
            self.notebook.SetSelection (index)


    @property
    def pageCount (self):
        return self.notebook.GetPageCount ()


    def addPage (self, parent, title):
        self.notebook.AddPage(parent, title)


    def onPreferencesDialogClose (self, prefDialog):
        self.codeEditor.setDefaultSettings()


    def onAttachmentPaste (self, fnames):
        text = self._getAttachString (fnames)
        self.codeEditor.AddText (text)
        self.codeEditor.SetFocus()


    def UpdateView (self, page):
        self.Freeze()

        try:
            self.htmlWindow.page = self._currentpage

            self.codeEditor.SetReadOnly (False)
            self.codeEditor.SetText (self._currentpage.content)
            self.codeEditor.EmptyUndoBuffer()
            self.codeEditor.SetReadOnly (page.readonly)
            self.SetCursorPosition(self._getCursorPositionOption(page).value)
            self.codeEditor.SetFocus()

            self._updateHtmlWindow()
            tabIndex = self.loadPageTab (self._currentpage)
            if tabIndex < 0:
                tabIndex = self._getDefaultPage()

            self.selectedPageIndex = tabIndex
        finally:
            self.Thaw()


    def GetContentFromGui(self):
        return self.codeEditor.GetText()


    def __do_layout(self):
        self.addPage(self.codeEditor, _("HTML"))
        self.addPage(self.htmlWindow, _("Preview"))

        mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
        mainSizer.Add(self.notebook, 1, wx.EXPAND, 0)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)
        self.Layout()

    @abstractmethod
    def _enableActions (self, enabled):
        pass


    def _getDefaultPage(self):
        assert self._currentpage is not None

        if (len (self._currentpage.content) > 0 or
                len (Attachment (self._currentpage).attachmentFull) > 0):
            return self.RESULT_PAGE_INDEX

        return self.CODE_PAGE_INDEX


    def _onTabChanged (self, event):
        newevent = PageTabChangedEvent (tab=self.selectedPageIndex)
        wx.PostEvent(self, newevent)


    def savePageTab (self, page):
        """
        Соханить текущую вкладку (код, просмотр и т.п.) в настройки страницы
        """
        assert page is not None
        tabOption = IntegerOption (page.params,
                                   self.tabSectionName,
                                   self.tabParamName,
                                   -1)
        tabOption.value = self.selectedPageIndex


    def loadPageTab (self, page):
        """
        Прочитать из страницы настройки текущей вкладки (код, просмотр и т.п.)
        """
        assert page is not None

        # Get global tab option
        generalConfig = GeneralGuiConfig (self._application.config)
        generalTab = generalConfig.pageTab.value

        if generalTab == GeneralGuiConfig.PAGE_TAB_CODE:
            return self.CODE_PAGE_INDEX
        elif generalTab == GeneralGuiConfig.PAGE_TAB_RESULT:
            return self.RESULT_PAGE_INDEX

        # Get tab option from page
        tabOption = IntegerOption (page.params,
                                   self.tabSectionName,
                                   self.tabParamName,
                                   -1)
        return tabOption.value


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions (not self._application.selectedPage.readonly)
        self.checkForExternalEditAndSave()
        self._enableAllTools ()
        self.codeEditor.SetFocus()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self.Save()
        self._enableActions (False)
        self._enableAllTools ()
        self.htmlWindow.SetFocus()
        self.htmlWindow.Update()
        self._updatePage()
        self._updateHtmlWindow()


    def _updatePage(self):
        assert self._currentpage is not None

        setStatusText (_(u"Page rendered. Please wait…"), self._statusbar_item)
        self._application.onHtmlRenderingBegin(self._currentpage,
                                               self.htmlWindow)

        self._application.onPageUpdateNeeded(self._currentpage,
                                             PageUpdateNeededParams(True))

        setStatusText (u"", self._statusbar_item)
        self._application.onHtmlRenderingEnd (self._currentpage,
                                              self.htmlWindow)


    def _updateHtmlWindow (self):
        """
        Подготовить и показать HTML текущей страницы
        """
        assert self._currentpage is not None

        setStatusText (_(u"Page loading. Please wait…"), self._statusbar_item)

        try:
            path = self._currentpage.getHtmlPath()
            if not os.path.exists(path):
                self._updatePage()

            html = readTextFile(path)

            if (self._oldPage != self._currentpage or
                    self._oldHtmlResult != html):
                self.htmlWindow.LoadPage (path)
                self._oldHtmlResult = html
                self._oldPage = self._currentpage
        except EnvironmentError as e:
            print(e)
            MessageBox (_(u'Page loading error: {}').format(
                self._currentpage.title),
                _(u'Error'), wx.ICON_ERROR | wx.OK)

        setStatusText (u"", self._statusbar_item)


    def _enableAllTools (self):
        """
        Активировать или дезактивировать инструменты (пункты меню и кнопки)
        в зависимости от текущей выбранной вкладки
        """
        for tool in self.allTools:
            self.enableTool (tool, self._isEnabledTool (tool))

        # Отдельно проверим возможность работы поиска по странице
        # Поиск не должен работать только на странице просмотра
        searchEnabled = self.selectedPageIndex != self.RESULT_PAGE_INDEX

        actionController = self._application.actionController

        actionController.enableTools (SearchAction.stringId, searchEnabled)
        actionController.enableTools (SearchNextAction.stringId, searchEnabled)
        actionController.enableTools (SearchPrevAction.stringId, searchEnabled)

        actionController.enableTools (SearchAndReplaceAction.stringId,
                                      searchEnabled and not self._application.selectedPage.readonly)

        actionController.enableTools (AttachFilesAction.stringId,
                                      searchEnabled and not self._application.selectedPage.readonly)

        actionController.enableTools (GlobalSearchAction.stringId,
                                      searchEnabled and not self._application.selectedPage.readonly)

        self.mainWindow.UpdateAuiManager()


    def _isEnabledTool (self, tool):
        if "notebook" not in dir (self):
            return True

        assert self.notebook is not None
        assert self.selectedPageIndex != -1

        enabled = (tool.alwaysEnabled or
                   self.selectedPageIndex == self.CODE_PAGE_INDEX)

        return enabled


    def GetSearchPanel (self):
        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel

        return None


    def switchCodeResult (self):
        """
        Переключение между кодом и результатом
        """
        if self._currentpage is None:
            return

        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            self.selectedPageIndex = self.RESULT_PAGE_INDEX
        else:
            self.selectedPageIndex = self.CODE_PAGE_INDEX


    def turnText (self, left, right):
        """
        Обернуть выделенный текст строками left и right.
        Метод предназначен в первую очередь для упрощения доступа к
        одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.turnText(left, right)


    def replaceText (self, text):
        """
        Заменить выделенный текст строкой text
        Метод предназначен в первую очередь для упрощения доступа к
        одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(text)


    def escapeHtml (self):
        """
        Заменить символы на их HTML-представление
        Метод предназначен в первую очередь для упрощения доступа к
        одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.escapeHtml()


    def _onSpellOnOff (self, event):
        self._codeEditor.setDefaultSettings()

    def SetFocus(self):
        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.SetFocus()
        elif self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            return self.htmlWindow.SetFocus()

    def _onPageUpdate (self, sender, **kwargs):
        if (sender == self._currentpage and
                self.notebook.GetSelection() == self.RESULT_PAGE_INDEX):
            self._updatePage()
            self._updateHtmlWindow()
