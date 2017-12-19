# -*- coding: UTF-8 -*-

import os.path
import logging

import wx
import wx.aui

import outwiker.core.commands as cmd
from outwiker.core.application import Application

from .guiconfig import MainWindowConfig

from .mainmenu import MainMenu
from .mainwndcontroller import MainWndController
from .mainpanescontroller import MainPanesController
from outwiker.gui.mainpanes.tagscloudmainpane import TagsCloudMainPane
from outwiker.gui.mainpanes.attachmainpane import AttachMainPane
from outwiker.gui.mainpanes.treemainpane import TreeMainPane
from outwiker.gui.mainpanes.pagemainpane import PageMainPane
from outwiker.gui.tabscontroller import TabsController
from outwiker.gui.trayicon import getTrayIconController
from outwiker.core.system import getImagesDir

from .toolbars.generaltoolbar import GeneralToolBar
from .toolbars.pluginstoolbar import PluginsToolBar
from .toolbars.toolbarscontroller import ToolBarsController

from outwiker.actions.new import NewAction
from outwiker.actions.open import OpenAction
from outwiker.actions.openreadonly import OpenReadOnlyAction
from outwiker.actions.close import CloseAction
from outwiker.actions.save import SaveAction
from outwiker.actions.printaction import PrintAction
from outwiker.actions.exit import ExitAction
from outwiker.actions.fullscreen import FullScreenAction
from outwiker.actions.preferences import PreferencesAction
from outwiker.actions.addsiblingpage import AddSiblingPageAction
from outwiker.actions.addchildpage import AddChildPageAction
from outwiker.actions.movepageup import MovePageUpAction
from outwiker.actions.movepagedown import MovePageDownAction
from outwiker.actions.sortchildalpha import SortChildAlphabeticalAction
from outwiker.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction
from outwiker.actions.renamepage import RenamePageAction
from outwiker.actions.removepage import RemovePageAction
from outwiker.actions.editpageprop import EditPagePropertiesAction
from outwiker.actions.addbookmark import AddBookmarkAction
from outwiker.actions.tabs import (AddTabAction, CloseTabAction,
                                   PreviousTabAction, NextTabAction)
from outwiker.actions.globalsearch import GlobalSearchAction
from outwiker.actions.attachfiles import AttachFilesAction
import outwiker.actions.clipboard as clipboard
import outwiker.actions.tags as tags
import outwiker.actions.switchto as switchto
from outwiker.actions.reloadwiki import ReloadWikiAction
from outwiker.actions.openhelp import OpenHelpAction
from outwiker.actions.about import AboutAction
from outwiker.actions.openattachfolder import OpenAttachFolderAction
from outwiker.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.actions.applystyle import SetStyleToBranchAction
from outwiker.actions.openpluginsfolder import OpenPluginsFolderAction
from outwiker.actions.moving import (GoToParentAction,
                                     GoToFirstChildAction,
                                     GoToNextSiblingAction,
                                     GoToPrevSiblingAction)

from outwiker.pages.wiki.wikipagecontroller import WikiPageController
from outwiker.pages.html.htmlpagecontroller import HtmlPageController
from outwiker.pages.text.textpagecontroller import TextPageController
from outwiker.pages.search.searchpagecontroller import SearchPageController
from outwiker.gui.preferences.prefcontroller import PrefController
from outwiker.core.system import getOS


logger = logging.getLogger('outwiker.gui.mainwindow')

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.mainWindowConfig = MainWindowConfig(Application.config)

        # Флаг, обозначающий, что в цикле обработки стандартных сообщений
        # (например, копирования в буфер обмена) сообщение вернулось обратно
        self.__stdEventLoop = False

        self.__setIcon()
        self.SetTitle(u"OutWiker")

        self.mainMenu = MainMenu()
        self.SetMenuBar(self.mainMenu)

        self.__createStatusBar()

        self.controller = MainWndController(self)
        self.controller.loadMainWindowParams()

        if self.mainWindowConfig.maximized.value:
            self.Maximize()

        self.auiManager = wx.aui.AuiManager(self)
        self.__createAuiPanes()
        self.__createToolbars()

        self.__panesController = MainPanesController(Application, self)

        self.__bindGuiEvents()

        self.taskBarIconController = getTrayIconController(Application, self)
        self.taskBarIconController.initialize()

        self.tabsController = TabsController(self.pagePanel.panel.tabsCtrl,
                                             Application)

        self._coreControllers = [
            WikiPageController(Application),
            HtmlPageController(Application),
            TextPageController(Application),
            SearchPageController(Application),
            PrefController(Application),
        ]

        self._initCoreControllers()

    @property
    def mainToolbar(self):
        return self._mainToolbar

    @property
    def pluginsToolbar(self):
        '''
        Added in outwiker.gui 1.4
        '''
        return self._pluginsToolbar

    def __createToolbars(self):
        self._mainToolbar = GeneralToolBar(self, self.auiManager)
        self._pluginsToolbar = PluginsToolBar(self, self.auiManager)

        self.GENERAL_TOOLBAR_STR = self._mainToolbar.name
        self.PLUGINS_TOOLBAR_STR = self._pluginsToolbar.name
        self.toolbars = ToolBarsController(self)

        self.toolbars[self.mainToolbar.name] = self.mainToolbar
        self.toolbars[self._pluginsToolbar.name] = self._pluginsToolbar

    def _initCoreControllers(self):
        [controller.initialize() for controller in self._coreControllers]

    def _destroyCoreControllers(self):
        [controller.clear() for controller in self._coreControllers]
        self._coreControllers = []

    def createGui(self):
        """
        Создать пункты меню, кнопки на панелях инструментов и т.п.
        """
        self.__panesController.loadPanesSize()
        self.__addActionsGui()
        self.controller.enableGui()
        self.controller.updateRecentMenu()
        self.__panesController.updateViewMenu()
        self.treePanel.panel.addButtons()

        if self.mainWindowConfig.fullscreen.value:
            Application.actionController.check(FullScreenAction.stringId, True)

    def __createSwitchToMenu(self):
        actionController = Application.actionController
        menu = Application.mainWindow.mainMenu.switchToMenu

        actionController.appendMenuItem(
            switchto.SwitchToMainPanelAction.stringId,
            menu)

        actionController.appendMenuItem(
            switchto.SwitchToTreeAction.stringId,
            menu)

        actionController.appendMenuItem(
            switchto.SwitchToAttachmentsAction.stringId,
            menu)

        actionController.appendMenuItem(
            switchto.SwitchToTagsCloudAction.stringId,
            menu)

    def __createFileMenu(self):
        """
        Заполнить действиями меню Файл
        """
        imagesDir = getImagesDir()
        toolbar = Application.mainWindow.mainToolbar
        menu = Application.mainWindow.mainMenu.fileMenu
        actionController = Application.actionController

        # Создать...
        actionController.appendMenuItem(
            NewAction.stringId,
            menu)

        actionController.appendToolbarButton(
            NewAction.stringId,
            toolbar,
            os.path.join(imagesDir, u"new.png"),
            True)

        # Открыть...
        actionController.appendMenuItem(
            OpenAction.stringId,
            menu)

        actionController.appendToolbarButton(
            OpenAction.stringId,
            toolbar,
            os.path.join(imagesDir, u"open.png"),
            True)

        # Открыть только для чтения
        actionController.appendMenuItem(
            OpenReadOnlyAction.stringId,
            menu)

        menu.AppendSeparator()
        toolbar.AddSeparator()

        # Закрыть
        actionController.appendMenuItem(
            CloseAction.stringId,
            menu)

        # Сохранить
        actionController.appendMenuItem(
            SaveAction.stringId,
            menu)

        menu.AppendSeparator()

        # Печать
        actionController.appendMenuItem(
            PrintAction.stringId,
            menu)

        # Выход
        actionController.appendMenuItem(
            ExitAction.stringId,
            menu)

        menu.AppendSeparator()

    def __createTreeMenu(self):
        """
        Заполнить действиями меню Дерево
        """
        actionController = Application.actionController
        menu = Application.mainWindow.mainMenu.treeMenu
        toolbar = Application.mainWindow.mainToolbar
        imagesDir = getImagesDir()

        actionController.appendMenuItem(
            HistoryBackAction.stringId,
            menu)

        actionController.appendToolbarButton(
            HistoryBackAction.stringId,
            toolbar,
            os.path.join(imagesDir, u"back.png"),
            True)

        actionController.enableTools(HistoryBackAction.stringId, False)

        actionController.appendMenuItem(HistoryForwardAction.stringId, menu)

        actionController.appendToolbarButton(
            HistoryForwardAction.stringId,
            toolbar,
            os.path.join(imagesDir, u"forward.png"),
            True)

        actionController.enableTools(HistoryForwardAction.stringId, False)

        toolbar.AddSeparator()
        menu.AppendSeparator()

        actionController.appendMenuItem(AddSiblingPageAction.stringId, menu)
        actionController.appendMenuItem(AddChildPageAction.stringId, menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(MovePageUpAction.stringId, menu)
        actionController.appendMenuItem(MovePageDownAction.stringId, menu)

        actionController.appendMenuItem(SortChildAlphabeticalAction.stringId,
                                        menu)

        actionController.appendMenuItem(
            SortSiblingsAlphabeticalAction.stringId,
            menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(GoToParentAction.stringId, menu)
        actionController.appendMenuItem(GoToFirstChildAction.stringId, menu)
        actionController.appendMenuItem(GoToPrevSiblingAction.stringId, menu)
        actionController.appendMenuItem(GoToNextSiblingAction.stringId, menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(RenamePageAction.stringId, menu)
        actionController.appendMenuItem(RemovePageAction.stringId, menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(EditPagePropertiesAction.stringId,
                                        menu)

    def __createToolsMenu(self):
        imagesDir = getImagesDir()
        toolbar = Application.mainWindow.mainToolbar
        menu = Application.mainWindow.mainMenu.toolsMenu
        actionController = Application.actionController

        actionController.appendMenuItem(AddTabAction.stringId, menu)
        actionController.appendMenuItem(CloseTabAction.stringId, menu)
        actionController.appendMenuItem(PreviousTabAction.stringId, menu)
        actionController.appendMenuItem(NextTabAction.stringId, menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(GlobalSearchAction.stringId, menu)

        actionController.appendToolbarButton(
            GlobalSearchAction.stringId,
            toolbar,
            os.path.join(imagesDir, u"global_search.png"),
            True)

        actionController.appendMenuItem(AttachFilesAction.stringId, menu)

        actionController.appendToolbarButton(
            AttachFilesAction.stringId,
            toolbar,
            os.path.join(imagesDir, u"attach.png"),
            True)

        menu.AppendSeparator()

        actionController.appendMenuItem(
            clipboard.CopyPageTitleAction.stringId,
            menu)

        actionController.appendMenuItem(
            clipboard.CopyPagePathAction.stringId,
            menu)

        actionController.appendMenuItem(
            clipboard.CopyAttachPathAction.stringId,
            menu)

        actionController.appendMenuItem(
            clipboard.CopyPageLinkAction.stringId,
            menu)

        actionController.appendMenuItem(
            OpenAttachFolderAction.stringId,
            menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(
            tags.AddTagsToBranchAction.stringId,
            menu)

        actionController.appendMenuItem(
            tags.RemoveTagsFromBranchAction.stringId,
            menu)

        actionController.appendMenuItem(tags.RenameTagAction.stringId, menu)

        menu.AppendSeparator()

        actionController.appendMenuItem(ReloadWikiAction.stringId, menu)
        actionController.appendMenuItem(SetStyleToBranchAction.stringId, menu)

    def __createHelpMenu(self):
        menu = Application.mainWindow.mainMenu.helpMenu
        actionController = Application.actionController

        actionController.appendMenuItem(OpenHelpAction.stringId, menu)

        actionController.appendMenuItem(AboutAction.stringId, menu)

        actionController.appendMenuItem(OpenPluginsFolderAction.stringId, menu)

    def __addActionsGui(self):
        """
        Создать элементы интерфейса, привязанные к actions
        """
        self.__createFileMenu()
        self.__createTreeMenu()
        self.__createToolsMenu()
        self.__createHelpMenu()
        self.__createSwitchToMenu()
        self.__panesController.createViewMenuItems()

        actionController = Application.actionController

        Application.mainWindow.mainMenu.viewMenu.AppendSeparator()

        # Полноэкранный режим
        actionController.appendMenuCheckItem(FullScreenAction.stringId,
                                             self.mainMenu.viewMenu)

        # Вызов диалога настроек
        Application.mainWindow.mainMenu.editMenu.AppendSeparator()

        actionController.appendMenuItem(
            PreferencesAction.stringId,
            Application.mainWindow.mainMenu.editMenu)

        # Добавление / удаление закладки
        actionController.appendMenuItem(
            AddBookmarkAction.stringId,
            Application.mainWindow.mainMenu.bookmarksMenu)

        Application.mainWindow.mainMenu.bookmarksMenu.AppendSeparator()

    # Оставлено, чтобы не ломать совместимость с плагином WebPage
    def updateShortcuts(self):
        pass

    def UpdateAuiManager(self):
        """
        Обновление auiManager. Сделано для облегчения доступа
        """
        if self.auiManager:
            self.auiManager.Update()

    def __createAuiPanes(self):
        """
        Создание плавающих панелей
        """
        self.pagePanel = PageMainPane(self, self.auiManager, Application)
        self.treePanel = TreeMainPane(self, self.auiManager, Application)
        self.attachPanel = AttachMainPane(self, self.auiManager, Application)
        self.tagsCloudPanel = TagsCloudMainPane(self,
                                                self.auiManager,
                                                Application)

    def __createStatusBar(self):
        """
        Создание статусной панели
        """
        self.statusbar = wx.StatusBar(self, -1)

        datetime_width = self.mainWindowConfig.datetimeStatusWidth.value
        items_count = 2
        self.statusbar.SetFieldsCount(items_count)
        self.statusbar.SetStatusWidths([-1, datetime_width])
        self.SetStatusBar(self.statusbar)

    def __bindGuiEvents(self):
        """
        Подписаться на события меню, кнопок и т.п.
        """
        self.Bind(wx.EVT_MENU, self.__onStdEvent, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self.__onStdEvent, id=wx.ID_REDO)
        self.Bind(wx.EVT_MENU, self.__onStdEvent, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU, self.__onStdEvent, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self.__onStdEvent, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, self.__onStdEvent, id=wx.ID_SELECTALL)

    def __unbindGuiEvents(self):
        """
        Подписаться на события меню, кнопок и т.п.
        """
        self.Unbind(wx.EVT_MENU, id=wx.ID_UNDO, handler=self.__onStdEvent)
        self.Unbind(wx.EVT_MENU, id=wx.ID_REDO, handler=self.__onStdEvent)
        self.Unbind(wx.EVT_MENU, id=wx.ID_CUT, handler=self.__onStdEvent)
        self.Unbind(wx.EVT_MENU, id=wx.ID_COPY, handler=self.__onStdEvent)
        self.Unbind(wx.EVT_MENU, id=wx.ID_PASTE, handler=self.__onStdEvent)
        self.Unbind(wx.EVT_MENU, id=wx.ID_SELECTALL, handler=self.__onStdEvent)

    def __saveParams(self):
        """
        Сохранить параметры в конфиг
        """
        try:
            if not self.IsIconized():
                if (not self.IsFullScreen() and not self.IsMaximized()):
                    (width, height) = self.GetSize()
                    (xpos, ypos) = self.GetPosition()

                    if xpos < 0:
                        width += xpos
                        xpos = 0

                    if ypos < 0:
                        height += ypos
                        ypos = 0

                    self.mainWindowConfig.width.value = width
                    self.mainWindowConfig.height.value = height

                    self.mainWindowConfig.xPos.value = xpos
                    self.mainWindowConfig.yPos.value = ypos

                self.mainWindowConfig.fullscreen.value = self.IsFullScreen()
                self.mainWindowConfig.maximized.value = self.IsMaximized()

                self.__panesController.savePanesParams()
        except Exception as e:
            cmd.MessageBox(_(u"Can't save config\n%s") % (str(e)),
                           _(u"Error"), wx.ICON_ERROR | wx.OK)

    def __setIcon(self):
        """
        Установки иконки главного окна
        """
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join(getImagesDir(),
                                                   "outwiker.ico"),
                                      wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)

    def Destroy(self):
        """
        Убрать за собой
        """
        logger.debug(u'Begin MainWindow.Destroy.')

        assert self.toolbars is not None
        assert self.__panesController is not None
        assert self.pagePanel is not None
        assert self.treePanel is not None
        assert self.attachPanel is not None
        assert self.tagsCloudPanel is not None

        Application.plugins.clear()
        self.__saveParams()
        self.toolbars.updatePanesInfo()
        self.destroyPagePanel(True)
        Application.actionController.saveHotKeys()

        self._destroyCoreControllers()

        self.__unbindGuiEvents()

        self.toolbars.destroyAllToolBars()
        self.tabsController.destroy()

        self.auiManager.UnInit()

        self.pagePanel.close()
        self.__panesController.closePanes()
        self.__panesController = None

        self.statusbar.Close()
        self.taskBarIconController.destroy()
        self.controller.destroy()
        self.auiManager.Destroy()
        self.auiManager = None

        self.toolbars = None
        self.SetMenuBar(None)
        self.mainMenu.Destroy()

        self.pagePanel = None
        self.treePanel = None
        self.attachPanel = None
        self.tagsCloudPanel = None

        super(MainWindow, self).Destroy()
        logger.debug(u'End MainWindow.Destroy.')

    def destroyPagePanel(self, save):
        """
        Уничтожить панель с текущей страницей.
        save - надо ли предварительно сохранить страницу?
        """
        if save:
            self.pagePanel.panel.destroyPageView()
        else:
            self.pagePanel.panel.destroyWithoutSave()

    def __onStdEvent(self, event):
        """
        Обработчик стандартных событий (копировать, вставить и т.п.)
        """
        if not self.__stdEventLoop:
            self.__stdEventLoop = True
            target = wx.Window.FindFocus()

            if target is not None:
                target.ProcessEvent(event)
                self.__stdEventLoop = False

    def setFullscreen(self, fullscreen):
        """
        Установить параметры в зависимости от режима fullscreen
        """
        if fullscreen:
            self.__toFullscreen()
        else:
            self.__fromFullscreen()

    def __toFullscreen(self):
        """
        Переключение в полноэкранный режим
        """
        self.__panesController.savePanesParams()
        # The bug (?) in wxPython under Ubuntu spoils check items
        # after full screen mode
        if getOS().name != 'unix':
            self.ShowFullScreen(True,
                                (wx.FULLSCREEN_NOTOOLBAR |
                                 wx.FULLSCREEN_NOBORDER |
                                 wx.FULLSCREEN_NOCAPTION))

        self.__panesController.toFullscreen()

    def __fromFullscreen(self):
        """
        Возврат из полноэкранного режима
        """
        self.controller.loadMainWindowParams()
        # The bug (?) in wxPython under Ubuntu spoils check items after
        # full screen mode
        if getOS().name != 'unix':
            self.ShowFullScreen(False)

        self.__panesController.fromFullscreen()
