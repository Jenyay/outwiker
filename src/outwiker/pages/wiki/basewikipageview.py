# -*- coding: utf-8 -*-

import logging
import wx

from outwiker.core.treetools import getPageHtmlPath
from outwiker.app.services.messages import showError
from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW, PAGE_MODE_HTML
from outwiker.gui.defines import TOOLBAR_ORDER_TEXT
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from outwiker.pages.wiki.htmlcodeview import HtmlCodeView
from outwiker.utilites.textfile import readTextFile

from .actions.openhtmlcode import WikiOpenHtmlCodeAction
from .actions.updatehtml import WikiUpdateHtmlAction


logger = logging.getLogger("outwiker.pages.wiki.basewikipageview")


class BaseWikiPageView(BaseHtmlPanel):
    HTML_RESULT_PAGE_INDEX = BaseHtmlPanel.RESULT_PAGE_INDEX + 1

    def __init__(self, parent, application):
        logger.debug("BaseWikiPageView creation started")
        super(BaseWikiPageView, self).__init__(parent, application)

        # Редактор с просмотром получившегося HTML (если есть)
        self.htmlCodeWindow = None

        self.__WIKI_MENU_INDEX = 7

        # Список используемых полиморфных действий
        self.__polyActions = self._getPolyActions()

        # Список действий, которые нужно удалять с панелей и из меню.
        # А еще их надо дизаблить при переходе на вкладки просмотра
        # результата или HTML
        self.__wikiNotationActions = self._getSpecificActions()

        self._toolbars = self._getToolbarsInfo(self.mainWindow)
        for toolbar_id, title in self._toolbars:
            self.mainWindow.toolbars.createToolBar(
                toolbar_id, title, order=TOOLBAR_ORDER_TEXT
            )

        self.notebook.SetPageText(0, self._getPageTitle())

        self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.htmlSizer.AddGrowableRow(0)
        self.htmlSizer.AddGrowableCol(0)

        # Номер вкладки с кодом HTML. -1, если вкладки нет
        self.htmlcodePageIndex = -1

        self._wikiMenu = wx.Menu()

        logger.debug("Wiki page GUI creation started")
        self._createCommonTools()
        self._createWikiTools()
        logger.debug("Wiki page GUI creation ended")

        self.mainWindow.UpdateAuiManager()

        if self._isHtmlCodeShown():
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()

        self._application.onPageModeChange += self.onTabChanged
        logger.debug("BaseWikiPageView creation ended")

    # Методы, которые необходимо переопределить в производном классе
    def _createWikiTools(self):
        pass

    def _getPageTitle(self):
        """
        Метод должен возвращать строку, показываемую на вкладке
        страницы с кодом
        """
        pass

    def _getMenuTitle(self):
        """
        Метод должен возвращать заголовок меню
        """
        pass

    def _getMenuId(self):
        """
        Метод должен возвращать идентификатор меню
        """
        pass

    def _getToolbarsInfo(self, mainWindow):
        """
        Метод должен возвращать список кортежей: (id панели, заголовок панели)
        """
        pass

    def _getPolyActions(self):
        """
        Метод должен возвращать список используемых полиморфных actions
        (или пустой список)
        """
        pass

    def _getSpecificActions(self):
        """
        Метод должен возвращать список actions, которые нужно дизаблить при
        переходе на страницу просмотра (или пустой список)
        """
        pass

    def _isHtmlCodeShown(self):
        """
        Возвращает True, если нужно показывать вкладку с кодом HTML,
        и False в противном случае
        """
        pass

    # Конец методов, которые необходимо переопределить в производном классе

    def GetPageMode(self):
        """
        Return the current page mode.
        """
        if self._selectedPageIndex == self.CODE_PAGE_INDEX:
            return PAGE_MODE_TEXT
        elif self._selectedPageIndex == self.RESULT_PAGE_INDEX:
            return PAGE_MODE_PREVIEW
        elif self._selectedPageIndex == self.HTML_RESULT_PAGE_INDEX:
            return PAGE_MODE_HTML

        assert False

    def SetPageMode(self, pagemode):
        if pagemode == PAGE_MODE_TEXT:
            self._selectedPageIndex = self.CODE_PAGE_INDEX
        elif pagemode == PAGE_MODE_PREVIEW:
            self._selectedPageIndex = self.RESULT_PAGE_INDEX
        elif pagemode == PAGE_MODE_HTML:
            self._selectedPageIndex = self.HTML_RESULT_PAGE_INDEX
        else:
            raise ValueError()

    def Clear(self):
        logger.debug("GUI destroying started")
        self._removeActionTools()
        self._application.onPageModeChange -= self.onTabChanged

        for toolbar_info in self._toolbars:
            self.mainWindow.toolbars.destroyToolBar(toolbar_info[0])

        super().Clear()
        logger.debug("GUI destroying ended")

    def onPreferencesDialogClose(self, prefDialog):
        super(BaseWikiPageView, self).onPreferencesDialogClose(prefDialog)
        if self.htmlCodeWindow is not None:
            self.htmlCodeWindow.setDefaultSettings()

    def _removeActionTools(self):
        actionController = self._application.actionController

        # Удалим элементы меню
        for action in self.__wikiNotationActions:
            actionController.removeMenuItem(action.stringId)

        # Удалим элементы меню полиморфных действий
        for strid in self.__polyActions:
            actionController.removeMenuItem(strid)

        actionController.removeMenuItem(WikiOpenHtmlCodeAction.stringId)
        actionController.removeMenuItem(WikiUpdateHtmlAction.stringId)
        actionController.removeMenuItem(SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        if self._toolbars:
            for action in self.__wikiNotationActions:
                actionController.removeToolbarButton(action.stringId)

            for strid in self.__polyActions:
                actionController.removeToolbarButton(strid)

        # Обнулим функции действия в полиморфных действиях
        for strid in self.__polyActions:
            actionController.getAction(strid).setFunc(None)

    @property
    def toolsMenu(self):
        return self._wikiMenu

    def __createHtmlCodePanel(self, parentSizer):
        # Окно для просмотра получившегося кода HTML
        self.htmlCodeWindow = HtmlCodeView(self.notebook, self._application)
        self.htmlCodeWindow.SetReadOnly(True)
        parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 2)

        self.addPage(self.htmlCodeWindow, _("HTML"))
        return self.pageCount - 1

    def SetFocus(self):
        if self._selectedPageIndex == self.htmlcodePageIndex:
            self.htmlCodeWindow.SetFocus()
        else:
            super(BaseWikiPageView, self).SetFocus()

    def GetSearchPanel(self):
        if self._selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel
        elif self._selectedPageIndex == self.RESULT_PAGE_INDEX:
            return self.htmlWindow.searchPanel
        elif self._selectedPageIndex == self.htmlcodePageIndex:
            return self.htmlCodeWindow.searchPanel

    def onTabChanged(self, page, params):
        if self._currentpage is not None:
            if params.pagemode == PAGE_MODE_TEXT:
                self._onSwitchToCode()
            elif params.pagemode == PAGE_MODE_PREVIEW:
                self._onSwitchToPreview()
            elif params.pagemode == PAGE_MODE_HTML:
                self._onSwitchCodeHtml()
            else:
                assert False

            self.savePageTab(self._currentpage)

    def _enableActions(self, enabled):
        actionController = self._application.actionController

        # Активируем / дизактивируем собственные действия
        [
            actionController.enableTools(action.stringId, enabled)
            for action in self.__wikiNotationActions
        ]

        # Активируем / дизактивируем полиморфные действия
        [actionController.enableTools(strid, enabled) for strid in self.__polyActions]

    def _onSwitchCodeHtml(self):
        assert self._currentpage is not None

        self.Save()
        self._enableActions(False)
        self._updatePage()
        self._updateHtmlCode()
        self._enableAllTools()
        self.htmlCodeWindow.SetFocus()
        self.htmlCodeWindow.Update()

    def _updateHtmlCode(self):
        if self.htmlcodePageIndex == -1:
            # Нет вкладки с кодом HTML. Ничего не делаем
            return

        try:
            path = getPageHtmlPath(self._currentpage)
            html = readTextFile(path)

            self.htmlCodeWindow.SetReadOnly(False)
            self.htmlCodeWindow.SetText(html)
            self.htmlCodeWindow.SetReadOnly(True)
        except IOError as e:
            showError(
                self._application.mainWindow,
                _("Can't load file %s") % (unicode(e.filename)),
            )

    @BaseHtmlPanel._selectedPageIndex.setter
    def _selectedPageIndex(self, index):
        """
        Устанавливает выбранную страницу (код, просмотр или полученный HTML)
        """
        if index == self.HTML_RESULT_PAGE_INDEX and self.htmlcodePageIndex == -1:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)
            selectedPage = self.htmlcodePageIndex
        else:
            selectedPage = index

        BaseHtmlPanel._selectedPageIndex.fset(self, selectedPage)

    def openHtmlCode(self):
        self.SetPageMode(PAGE_MODE_HTML)

    def removeMenu(self):
        mainMenu = self._application.mainWindow.menuController.getRootMenu()
        index = mainMenu.FindMenu(self._getMenuTitle())
        assert index != wx.NOT_FOUND

        mainMenu.Remove(index)
        self._application.mainWindow.menuController.removeMenu(self._getMenuId())

    def removeGui(self):
        super(BaseWikiPageView, self).removeGui()
        self.removeMenu()

    def updateHtml(self):
        if self.GetPageMode() == PAGE_MODE_PREVIEW:
            self._onSwitchToPreview()
        elif self.GetPageMode() == PAGE_MODE_HTML:
            self._onSwitchCodeHtml()

    def _createCommonTools(self):
        mainMenu = self._application.mainWindow.menuController.getRootMenu()
        mainMenu.Insert(self.__WIKI_MENU_INDEX, self.toolsMenu, self._getMenuTitle())
        self.mainWindow.menuController.addMenu(self._getMenuId(), self.toolsMenu)

        # Переключиться с кода на результат и обратно
        self._application.actionController.appendMenuItem(
            SwitchCodeResultAction.stringId, self.toolsMenu
        )

        # Переключиться на код HTML
        self._application.actionController.appendMenuItem(
            WikiOpenHtmlCodeAction.stringId, self.toolsMenu
        )

        # Обновить код HTML
        self._application.actionController.appendMenuItem(
            WikiUpdateHtmlAction.stringId, self.toolsMenu
        )

    def _onSpellOnOff(self, event):
        super()._onSpellOnOff(event)

        if self.htmlCodeWindow is not None:
            self.htmlCodeWindow.setDefaultSettings()
