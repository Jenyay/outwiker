# -*- coding: utf-8 -*-

import datetime

import wx

from outwiker.app.gui.bookmarkscontroller import BookmarksController

from outwiker.api.gui.mainwindow import getMainWindowTitle, setStatusText
from outwiker.api.services.messages import showError
from outwiker.api.services.tree import openWiki
from outwiker.core.events import PAGE_UPDATE_TITLE

from outwiker.gui.autosavetimer import AutosaveTimer
from outwiker.gui.guiconfig import TrayConfig, GeneralGuiConfig, MainWindowConfig
from outwiker.gui.defines import (MENU_FILE,
                                  TOOLBAR_GENERAL,
                                  CLOSE_BUTTON_ACTION_CLOSE,
                                  CLOSE_BUTTON_ACTION_MINIMIZE,
                                  CLOSE_BUTTON_ACTION_HIDE_TO_TRAY,
                                  STATUSBAR_PAGE_DATETIME_ITEM,
                                  )

from outwiker.actions.save import SaveAction
from outwiker.actions.close import CloseAction
from outwiker.actions.printaction import PrintAction
from outwiker.actions.addsiblingpage import AddSiblingPageAction
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.actions.movepageup import MovePageUpAction
from outwiker.actions.movepagedown import MovePageDownAction
from outwiker.actions.sortchildalpha import SortChildAlphabeticalAction
from outwiker.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction
from outwiker.actions.renamepage import RenamePageAction
from outwiker.actions.removepage import RemovePageAction
from outwiker.actions.editpageprop import EditPagePropertiesAction
from outwiker.actions.exit import ExitAction
from outwiker.actions.addbookmark import AddBookmarkAction
from outwiker.actions.tabs import (AddTabAction,
                                   CloseTabAction,
                                   PreviousTabAction,
                                   NextTabAction)
from outwiker.actions.globalsearch import GlobalSearchAction
from outwiker.actions.attachfiles import AttachFilesAction
import outwiker.actions.clipboard as clipboard
import outwiker.actions.tags as tags
from outwiker.actions.reloadwiki import ReloadWikiAction
from outwiker.actions.moving import (GoToParentAction,
                                     GoToFirstChildAction,
                                     GoToNextSiblingAction,
                                     GoToPrevSiblingAction)
from outwiker.actions.attachopenfolder import OpenAttachFolderAction
from outwiker.actions.applystyle import SetStyleToBranchAction


class MainWndController:
    """
    Контроллер для управления главным окном
    """

    def __init__(self, parent, application):
        """
        parent - instance of the MainWindow class
        application - instance of the ApplicationParams class
        """
        self._mainWindow = parent
        self._application = application
        self._tray_config = TrayConfig(self._application.config)
        self._generalConfig = GeneralGuiConfig(self._application.config)
        self._mainWindowConfig = MainWindowConfig(self._application.config)

        # Идентификаторы пунктов меню и кнопок, которые надо задизаблить,
        # если не открыта вики
        self.disabledTools = [
            wx.ID_UNDO,
            wx.ID_REDO,
            wx.ID_CUT,
            wx.ID_COPY,
            wx.ID_PASTE,
            wx.ID_SELECTALL,
        ]

        # Действия, которые надо дизаблить, если не открыта вики
        self._disabledActions = [
            SaveAction,
            CloseAction,
            PrintAction,
            AddSiblingPageAction,
            AddChildPageAction,
            MovePageDownAction,
            MovePageUpAction,
            SortChildAlphabeticalAction,
            SortSiblingsAlphabeticalAction,
            RenamePageAction,
            RemovePageAction,
            EditPagePropertiesAction,
            AddBookmarkAction,
            AddTabAction,
            CloseTabAction,
            PreviousTabAction,
            NextTabAction,
            GlobalSearchAction,
            AttachFilesAction,
            clipboard.CopyPageTitleAction,
            clipboard.CopyPagePathAction,
            clipboard.CopyAttachPathAction,
            clipboard.CopyPageLinkAction,
            tags.AddTagsToBranchAction,
            tags.RemoveTagsFromBranchAction,
            tags.RenameTagAction,
            ReloadWikiAction,
            GoToParentAction,
            GoToFirstChildAction,
            GoToNextSiblingAction,
            GoToPrevSiblingAction,
            OpenAttachFolderAction,
            SetStyleToBranchAction,
        ]

        # Идентификаторы для пунктов меню последних открытых вики
        # Ключ - id, значение - путь до вики
        self._recentId = {}

        self.bookmarks = BookmarksController(self, self._application)
        self._autosaveTimer = AutosaveTimer(self._application)

        datetime_width = self._mainWindowConfig.datetimeStatusWidth.value
        self._mainWindow.statusbar.addItem(STATUSBAR_PAGE_DATETIME_ITEM, datetime_width)

        self.init()
        self._createAcceleratorTable()

    def _createAcceleratorTable(self):
        """
        Создать горячие клавиши, которые не попали в меню
        """
        aTable = wx.AcceleratorTable([
           (wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
           (wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
           (wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
        self._mainWindow.SetAcceleratorTable(aTable)

    def init(self):
        """
        Начальные установки для главного окна
        """
        self._bindAppEvents()
        self._mainWindow.Bind(wx.EVT_CLOSE, handler=self._onClose)
        self._mainWindow.Bind(wx.EVT_ICONIZE, handler=self._onIconize)

    def _onClose(self, event):
        event.Veto()
        action = self._tray_config.closeButtonAction.value

        if action == CLOSE_BUTTON_ACTION_CLOSE:
            self._application.actionController.getAction(ExitAction.stringId).run(None)
        elif action == CLOSE_BUTTON_ACTION_MINIMIZE:
            self._mainWindow.Unbind(wx.EVT_ICONIZE, handler=self._onIconize)
            self._mainWindow.Iconize(True)
            wx.SafeYield()
            self._mainWindow.Bind(wx.EVT_ICONIZE, handler=self._onIconize)
        elif action == CLOSE_BUTTON_ACTION_HIDE_TO_TRAY:
            self._mainWindow.hideToTray()

    def _onIconize(self, event):
        if event.IsIconized() and self._tray_config.minimizeToTray.value == 1:
            # Окно свернули
            self._mainWindow.hideToTray()

    def destroy(self):
        self._unbindAppEvents()
        self._autosaveTimer.Destroy()
        self._autosaveTimer = None
        self._mainWindow.Unbind(wx.EVT_CLOSE, handler=self._onClose)
        self._mainWindow.Unbind(wx.EVT_ICONIZE, handler=self._onIconize)
        self._mainWindow = None
        self._application = None

    @property
    def mainWindow(self):
        return self._mainWindow

    @property
    def mainMenu(self):
        return self._mainWindow.menuController.getRootMenu()

    def removeMenuItemsById(self, menu, keys):
        """
        Удалить все элементы меню по идентификаторам
        """
        for key in keys:
            menu.Delete(key)
            self._mainWindow.Unbind(wx.EVT_MENU, id=key)

    def _bindAppEvents(self):
        self._application.onPageSelect += self._onPageSelect
        self._application.onPreferencesDialogClose += self._onPreferencesDialogClose
        self._application.onBookmarksChanged += self._onBookmarksChanged
        self._application.onTreeUpdate += self._onTreeUpdate
        self._application.onWikiOpen += self._onWikiOpen
        self._application.onPageUpdate += self._onPageUpdate

    def _unbindAppEvents(self):
        self._application.onPageSelect -= self._onPageSelect
        self._application.onPreferencesDialogClose -= self._onPreferencesDialogClose
        self._application.onBookmarksChanged -= self._onBookmarksChanged
        self._application.onTreeUpdate -= self._onTreeUpdate
        self._application.onWikiOpen -= self._onWikiOpen
        self._application.onPageUpdate -= self._onPageUpdate

    def _onBookmarksChanged(self, event):
        self.bookmarks.updateBookmarks()

    def _onTreeUpdate(self, sender):
        """
        Событие при обновлении дерева
        """
        self.bookmarks.updateBookmarks()
        self.updateTitle()
        self.updateStatusBar()

    def _onPageUpdate(self, page, **kwargs):
        if kwargs['change'] & PAGE_UPDATE_TITLE:
            self.updateTitle()
            self.updateStatusBar()
            self.bookmarks.updateBookmarks()

    def _onWikiOpen(self, wikiroot):
        """
        Обновить окно после того как загрузили вики
        """
        if wikiroot is not None and not wikiroot.readonly:
            try:
                self._application.recentWiki.add(wikiroot.path)
                self.updateRecentMenu()
            except IOError as e:
                showError(self._application.mainWindow,
                    _("Can't add wiki to recent list.\nCan't save config.\n%s") % (str(e)))

        self.enableGui()
        self.bookmarks.updateBookmarks()
        self.updateTitle()
        self.updateStatusBar()

    ###################################################
    # Обработка событий
    #
    def _onPageSelect(self, newpage):
        """
        Обработчик события выбора страницы в дереве
        """
        self.updateTitle()
        self.updateStatusBar()
        self._updateBookmarksState()

    def _updateBookmarksState(self):
        self._application.actionController.enableTools(
            AddBookmarkAction.stringId,
            self._application.selectedPage is not None
        )

    def _onPreferencesDialogClose(self, prefDialog):
        """
        Обработчик события изменения настроек главного окна
        """
        self.updateTitle()
        self.updateStatusBar()
        self.updateColors()

    ###################################################
    # Активировать/дизактивировать интерфейс
    #
    def enableGui(self):
        """
        Проверить открыта ли вики и включить или выключить кнопки на панели
        """
        enabled = self._application.wikiroot is not None

        self._enableTools(enabled)
        self._mainWindow.treePanel.panel.Enable(enabled)
        self._mainWindow.attachPanel.panel.Enable(enabled)

        self._updateBookmarksState()

    def _enableTools(self, enabled):
        toolbar = self._mainWindow.toolbars[TOOLBAR_GENERAL]

        for toolId in self.disabledTools:
            if toolbar.FindById(toolId) is not None:
                toolbar.EnableTool(toolId, enabled)

            if self.mainMenu.FindItemById(toolId) is not None:
                self.mainMenu.Enable(toolId, enabled)

        [self._application.actionController.enableTools(action.stringId, enabled)
         for action in self._disabledActions]

    def updateTitle(self):
        """
        Обновить заголовок главного окна в зависимости от шаблона
            и текущей страницы
        """
        self._mainWindow.SetTitle(getMainWindowTitle(self._application))

    def updateStatusBar(self):
        dateFormat = self._generalConfig.dateTimeFormat.value
        text = ''

        if(self._application.selectedPage is not None and
                self._application.selectedPage.datetime is not None):
            text = datetime.datetime.strftime(
                self._application.selectedPage.datetime,
                dateFormat)

        setStatusText(STATUSBAR_PAGE_DATETIME_ITEM, text)

    def loadMainWindowParams(self):
        """
        Загрузить параметры из конфига
        """
        self._mainWindow.Freeze()

        width = self._mainWindow.mainWindowConfig.width.value
        height = self._mainWindow.mainWindowConfig.height.value

        xpos = self._mainWindow.mainWindowConfig.xPos.value
        ypos = self._mainWindow.mainWindowConfig.yPos.value

        self._mainWindow.SetSize(
            xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

        self.updateColors()
        self._mainWindow.Layout()
        self._mainWindow.Thaw()

    def updateColors(self):
        config = self._mainWindow.mainWindowConfig
        panels = [
            self._mainWindow.treePanel,
            self._mainWindow.attachPanel,
            self._mainWindow.tagsCloudPanel,
            # self._mainWindow.pagePanel,
        ]

        for panel in panels:
            panel.setBackgroundColour(config.mainPanesBackgroundColor.value)
            panel.setForegroundColour(config.mainPanesTextColor.value)

        self._mainWindow.Refresh()

    ###################################################
    # Список последних открытых вики
    #
    def updateRecentMenu(self):
        """
        Обновление меню со списком последних открытых вики
        """
        menu_file = self._mainWindow.menuController[MENU_FILE]
        self.removeMenuItemsById(menu_file,
                                 list(self._recentId.keys()))
        self._recentId = {}

        for n in range(len(self._application.recentWiki)):
            id = wx.Window.NewControlId()
            path = self._application.recentWiki[n]
            self._recentId[id] = path

            title = path if n + 1 > 9 else u"&{n}. {path}".format(n=n+1,
                                                                  path=path)

            menu_file.Append(id, title, "", wx.ITEM_NORMAL)

            self._mainWindow.Bind(wx.EVT_MENU, self._onRecent, id=id)

    def _onRecent(self, event):
        """
        Выбор пункта меню с недавно открытыми файлами
        """
        openWiki(self._recentId[event.Id])
