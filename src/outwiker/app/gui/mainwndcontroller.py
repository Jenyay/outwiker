# -*- coding: utf-8 -*-

import datetime

import wx

from outwiker.app.actions.addbookmark import AddBookmarkAction
from outwiker.app.actions.addchildpage import AddChildPageAction
from outwiker.app.actions.addsiblingpage import AddSiblingPageAction
from outwiker.app.actions.applystyle import SetStyleToBranchAction
from outwiker.app.actions.attachfiles import AttachFilesAction
from outwiker.app.actions.attachfolder import AttachFolderAction
from outwiker.app.actions.attachopenfolder import OpenAttachFolderAction
from outwiker.app.actions.close import CloseAction
from outwiker.app.actions.editpageprop import EditPagePropertiesAction
from outwiker.app.actions.exit import ExitAction
from outwiker.app.actions.globalsearch import GlobalSearchAction
from outwiker.app.actions.movepagedown import MovePageDownAction
from outwiker.app.actions.movepageup import MovePageUpAction
from outwiker.app.actions.moving import (
    GoToParentAction,
    GoToFirstChildAction,
    GoToNextSiblingAction,
    GoToPrevSiblingAction,
)
from outwiker.app.actions.printaction import PrintAction
from outwiker.app.actions.reloadwiki import ReloadWikiAction
from outwiker.app.actions.removepage import RemovePageAction
from outwiker.app.actions.renamepage import RenamePageAction
from outwiker.app.actions.save import SaveAction
from outwiker.app.actions.sortchildalpha import SortChildAlphabeticalAction
from outwiker.app.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction
from outwiker.app.actions.tabs import (
    AddTabAction,
    CloseTabAction,
    PreviousTabAction,
    NextTabAction,
)
import outwiker.app.actions.clipboard as clipboard
import outwiker.app.actions.tags as tags

from outwiker.app.gui.bookmarkscontroller import BookmarksController
from outwiker.app.gui.mainwindowtools import getMainWindowTitle, setStatusText

from outwiker.app.services.messages import showError
from outwiker.app.services.tree import openWiki

from outwiker.core.events import PAGE_UPDATE_TITLE

from outwiker.gui.autosavetimer import AutosaveTimer
from outwiker.gui.guiconfig import TrayConfig, GeneralGuiConfig, MainWindowConfig
from outwiker.gui.defines import (
    MENU_FILE,
    CLOSE_BUTTON_ACTION_CLOSE,
    CLOSE_BUTTON_ACTION_MINIMIZE,
    CLOSE_BUTTON_ACTION_HIDE_TO_TRAY,
    STATUSBAR_PAGE_DATETIME_ITEM,
)


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
            AttachFolderAction,
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
        aTable = wx.AcceleratorTable(
            [
                (wx.ACCEL_CTRL, wx.WXK_INSERT, wx.ID_COPY),
                (wx.ACCEL_SHIFT, wx.WXK_INSERT, wx.ID_PASTE),
                (wx.ACCEL_SHIFT, wx.WXK_DELETE, wx.ID_CUT),
            ]
        )
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

    def _onBookmarksChanged(self, params):
        self.bookmarks.updateBookmarks()

    def _onTreeUpdate(self, sender):
        """
        Событие при обновлении дерева
        """
        self.bookmarks.updateBookmarks()
        self._updateTitle()
        self._updateStatusBar()

    def _onPageUpdate(self, page, **kwargs):
        if kwargs["change"] & PAGE_UPDATE_TITLE:
            self._updateTitle()
            self._updateStatusBar()
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
                showError(
                    self._application.mainWindow,
                    _("Can't add wiki to recent list.\nCan't save config.\n%s")
                    % (str(e)),
                )

        self.enableGui()
        self.bookmarks.updateBookmarks()
        self._updateTitle()
        self._updateStatusBar()

    ###################################################
    # Обработка событий
    #
    def _onPageSelect(self, newpage):
        """
        Обработчик события выбора страницы в дереве
        """
        self._updateTitle()
        self._updateStatusBar()
        self._updateBookmarksState()

    def _updateBookmarksState(self):
        self._application.actionController.enableTools(
            AddBookmarkAction.stringId, self._application.selectedPage is not None
        )

    def _onPreferencesDialogClose(self, prefDialog):
        """
        Обработчик события изменения настроек главного окна
        """
        self._updateTitle()
        self._updateStatusBar()
        self._updateColors()

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
        for action in self._disabledActions:
            self._application.actionController.enableTools(action.stringId, enabled)

    def _updateTitle(self):
        """
        Обновить заголовок главного окна в зависимости от шаблона
            и текущей страницы
        """
        self._mainWindow.SetTitle(getMainWindowTitle(self._application))

    def _updateStatusBar(self):
        dateFormat = self._generalConfig.dateTimeFormat.value
        text = ""

        if (
            self._application.selectedPage is not None
            and self._application.selectedPage.datetime is not None
        ):
            text = datetime.datetime.strftime(
                self._application.selectedPage.datetime, dateFormat
            )

        setStatusText(self._application.mainWindow, STATUSBAR_PAGE_DATETIME_ITEM, text)

    def loadMainWindowParams(self):
        """
        Загрузить параметры из конфига
        """
        self._mainWindow.Freeze()

        width = self._mainWindow.mainWindowConfig.width.value
        height = self._mainWindow.mainWindowConfig.height.value

        xpos = self._mainWindow.mainWindowConfig.xPos.value
        ypos = self._mainWindow.mainWindowConfig.yPos.value

        self._mainWindow.SetSize(xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

        self._updateColors()
        self._mainWindow.Layout()
        self._mainWindow.Thaw()

    def _updateColors(self):
        config = self._mainWindow.mainWindowConfig
        panels = [
            self._mainWindow.treePanel,
            self._mainWindow.attachPanel,
            self._mainWindow.tagsCloudPanel,
        ]

        for panel in panels:
            backColor = wx.Colour(config.mainPanesBackgroundColor.value)
            textColor = wx.Colour(config.mainPanesTextColor.value)
            if not backColor.IsOk():
                backColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)

            if not textColor.IsOk():
                textColor = wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)

            panel.setBackgroundColour(backColor)
            panel.setForegroundColour(textColor)

        self._mainWindow.Refresh()

    ###################################################
    # Список последних открытых вики
    #
    def updateRecentMenu(self):
        """
        Обновление меню со списком последних открытых вики
        """
        menu_file = self._mainWindow.menuController[MENU_FILE]
        self.removeMenuItemsById(menu_file, list(self._recentId.keys()))
        self._recentId = {}

        for n in range(len(self._application.recentWiki)):
            id = wx.Window.NewControlId()
            path = self._application.recentWiki[n]
            self._recentId[id] = path

            title = path if n + 1 > 9 else "&{n}. {path}".format(n=n + 1, path=path)

            menu_file.Append(id, title, "", wx.ITEM_NORMAL)

            self._mainWindow.Bind(wx.EVT_MENU, self._onRecent, id=id)

    def _onRecent(self, event):
        """
        Выбор пункта меню с недавно открытыми файлами
        """
        assert self._application is not None
        openWiki(self._recentId[event.Id], self._application)
