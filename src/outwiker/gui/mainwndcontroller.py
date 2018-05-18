# -*- coding: utf-8 -*-

import datetime

import wx

import outwiker.core.commands
from outwiker.core.commands import setStatusText, getMainWindowTitle
from .bookmarkscontroller import BookmarksController
from .autosavetimer import AutosaveTimer
from .guiconfig import GeneralGuiConfig, TrayConfig
from .defines import MENU_FILE, TOOLBAR_GENERAL

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
from outwiker.actions.openattachfolder import OpenAttachFolderAction
from outwiker.actions.applystyle import SetStyleToBranchAction


class MainWndController(object):
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
        self.__autosaveTimer = AutosaveTimer(self._application)

        self.init()
        self.__createAcceleratorTable()

    def __createAcceleratorTable(self):
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
        self.__bindAppEvents()
        self.mainWindow.Bind(wx.EVT_CLOSE, self.__onClose)

    def __onClose(self, event):
        event.Veto()
        if TrayConfig(self._application.config).minimizeOnClose.value:
            self._mainWindow.Iconize(True)
        else:
            self._application.actionController.getAction(ExitAction.stringId).run(None)

    def destroy(self):
        self.__unbindAppEvents()
        self.__autosaveTimer.Destroy()
        self.__autosaveTimer = None
        self._mainWindow.Unbind(wx.EVT_CLOSE, handler=self.__onClose)
        self._mainWindow = None
        self._application = None

    @property
    def mainWindow(self):
        return self._mainWindow

    @property
    def mainMenu(self):
        return self.mainWindow.menuController.getRootMenu()

    def updatePageDateTime(self):
        statusbar_item = 1
        config = GeneralGuiConfig(self._application.config)

        dateFormat = config.dateTimeFormat.value
        text = u""

        if(self._application.selectedPage is not None and
                self._application.selectedPage.datetime is not None):
            text = datetime.datetime.strftime(
                self._application.selectedPage.datetime,
                dateFormat)

        setStatusText(text, statusbar_item)

    def removeMenuItemsById(self, menu, keys):
        """
        Удалить все элементы меню по идентификаторам
        """
        for key in keys:
            menu.Delete(key)
            self.mainWindow.Unbind(wx.EVT_MENU, id=key)

    def __bindAppEvents(self):
        self._application.onPageSelect += self.__onPageSelect
        self._application.onPreferencesDialogClose += self.__onPreferencesDialogClose
        self._application.onBookmarksChanged += self.__onBookmarksChanged
        self._application.onTreeUpdate += self.__onTreeUpdate
        self._application.onWikiOpen += self.__onWikiOpen
        self._application.onPageUpdate += self.__onPageUpdate

    def __unbindAppEvents(self):
        self._application.onPageSelect -= self.__onPageSelect
        self._application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
        self._application.onBookmarksChanged -= self.__onBookmarksChanged
        self._application.onTreeUpdate -= self.__onTreeUpdate
        self._application.onWikiOpen -= self.__onWikiOpen
        self._application.onPageUpdate -= self.__onPageUpdate

    def __onBookmarksChanged(self, event):
        self.bookmarks.updateBookmarks()

    def __onTreeUpdate(self, sender):
        """
        Событие при обновлении дерева
        """
        self.bookmarks.updateBookmarks()
        self.updateTitle()
        self.updatePageDateTime()

    def __onPageUpdate(self, page, **kwargs):
        self.updatePageDateTime()

    def __onWikiOpen(self, wikiroot):
        """
        Обновить окно после того как загрузили вики
        """
        if wikiroot is not None and not wikiroot.readonly:
            try:
                self._application.recentWiki.add(wikiroot.path)
                self.updateRecentMenu()
            except IOError as e:
                outwiker.core.commands.MessageBox(
                    _(u"Can't add wiki to recent list.\nCan't save config.\n%s") % (str(e)),
                    _(u"Error"), wx.ICON_ERROR | wx.OK)

        self.enableGui()
        self.bookmarks.updateBookmarks()
        self.updateTitle()
        self.updatePageDateTime()

    ###################################################
    # Обработка событий
    #
    def __onPageSelect(self, newpage):
        """
        Обработчик события выбора страницы в дереве
        """
        self.updateTitle()
        self.updatePageDateTime()
        self._updateBookmarksState()

    def _updateBookmarksState(self):
        self._application.actionController.enableTools(
            AddBookmarkAction.stringId,
            self._application.selectedPage is not None
        )

    def __onPreferencesDialogClose(self, prefDialog):
        """
        Обработчик события изменения настроек главного окна
        """
        self.updateTitle()
        self.updatePageDateTime()
    #
    ###################################################

    ###################################################
    # Активировать/дизактивировать интерфейс
    #
    def enableGui(self):
        """
        Проверить открыта ли вики и включить или выключить кнопки на панели
        """
        enabled = self._application.wikiroot is not None

        self.__enableTools(enabled)
        self.mainWindow.pagePanel.panel.Enable(enabled)
        self.mainWindow.treePanel.panel.Enable(enabled)
        self.mainWindow.attachPanel.panel.Enable(enabled)

        self._updateBookmarksState()

    def __enableTools(self, enabled):
        toolbar = self.mainWindow.toolbars[TOOLBAR_GENERAL]

        for toolId in self.disabledTools:
            if toolbar.FindById(toolId) is not None:
                toolbar.EnableTool(toolId, enabled)

            if self.mainMenu.FindItemById(toolId) is not None:
                self.mainMenu.Enable(toolId, enabled)

        [self._application.actionController.enableTools(action.stringId, enabled)
         for action in self._disabledActions]

    #
    ###################################################

    def updateTitle(self):
        """
        Обновить заголовок главного окна в зависимости от шаблона
            и текущей страницы
        """
        self.mainWindow.SetTitle(getMainWindowTitle(self._application))

    def loadMainWindowParams(self):
        """
        Загрузить параметры из конфига
        """
        self.mainWindow.Freeze()

        width = self.mainWindow.mainWindowConfig.width.value
        height = self.mainWindow.mainWindowConfig.height.value

        xpos = self.mainWindow.mainWindowConfig.xPos.value
        ypos = self.mainWindow.mainWindowConfig.yPos.value

        self.mainWindow.SetSize(
            xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

        self.mainWindow.Layout()
        self.mainWindow.Thaw()

    ###################################################
    # Список последних открытых вики
    #
    def updateRecentMenu(self):
        """
        Обновление меню со списком последних открытых вики
        """
        menu_file = self.mainWindow.menuController[MENU_FILE]
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

            self.mainWindow.Bind(wx.EVT_MENU, self.__onRecent, id=id)

    def __onRecent(self, event):
        """
        Выбор пункта меню с недавно открытыми файлами
        """
        outwiker.core.commands.openWiki(self._recentId[event.Id])

    #
    ###################################################
