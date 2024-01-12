# -*- coding: utf-8 -*-

import logging

import wx
import wx.aui

from outwiker.app.actions.about import AboutAction
from outwiker.app.actions.addbookmark import AddBookmarkAction
from outwiker.app.actions.addchildpage import AddChildPageAction
from outwiker.app.actions.addsiblingpage import AddSiblingPageAction
from outwiker.app.actions.applystyle import SetStyleToBranchAction
from outwiker.app.actions.attachcreatesubdir import AttachCreateSubdirAction
from outwiker.app.actions.attachfiles import AttachFilesAction
from outwiker.app.actions.attachfolder import AttachFolderAction
from outwiker.app.actions.attachopenfolder import OpenAttachFolderAction
from outwiker.app.actions.close import CloseAction
from outwiker.app.actions.clipboard import (
    CopyAttachPathAction,
    CopyPageLinkAction,
    CopyPagePathAction,
    CopyPageTitleAction,
)
from outwiker.app.actions.editpageprop import EditPagePropertiesAction
from outwiker.app.actions.exit import ExitAction
from outwiker.app.actions.fullscreen import FullScreenAction
from outwiker.app.actions.globalsearch import GlobalSearchAction
from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.app.actions.movepagedown import MovePageDownAction
from outwiker.app.actions.movepageup import MovePageUpAction
from outwiker.app.actions.moving import (
    GoToParentAction,
    GoToFirstChildAction,
    GoToNextSiblingAction,
    GoToPrevSiblingAction,
)
from outwiker.app.actions.new import NewAction
from outwiker.app.actions.open import OpenAction
from outwiker.app.actions.openhelp import OpenHelpAction
from outwiker.app.actions.openpluginsfolder import OpenPluginsFolderAction
from outwiker.app.actions.openreadonly import OpenReadOnlyAction
from outwiker.app.actions.preferences import PreferencesAction
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
import outwiker.app.actions.switchto as switchto
import outwiker.app.actions.tags as tags

from outwiker.app.gui.mainwndcontroller import MainWndController
from outwiker.app.gui.mainpanes.tagscloudmainpane import TagsCloudMainPane
from outwiker.app.gui.mainpanes.attachmainpane import AttachMainPane
from outwiker.app.gui.mainpanes.treemainpane import TreeMainPane
from outwiker.app.gui.mainpanes.pagemainpane import PageMainPane
from outwiker.app.gui.mainpanescontroller import MainPanesController
from outwiker.app.gui.menucontroller import MenuController
from outwiker.app.gui.preferences.prefcontroller import PrefController
from outwiker.app.gui.tabscontroller import TabsController
from outwiker.app.gui.toolbarscontroller import ToolBarsController
from outwiker.app.gui.trayicon import getTrayIconController

from outwiker.app.services.messages import showError

from outwiker.core.attachwatcher import AttachWatcher
from outwiker.core.system import getOS, getBuiltinImagePath

from outwiker.gui import defines as guidefines
from outwiker.gui.guiconfig import MainWindowConfig
from outwiker.gui.controls.toolbar2 import ToolBar2Container
from outwiker.gui.controls.toastercontroller import ToasterController
from outwiker.gui.statusbar import StatusBarController

from outwiker.pages.wiki.wikipagecontroller import WikiPageController
from outwiker.pages.html.htmlpagecontroller import HtmlPageController
from outwiker.pages.text.textpagecontroller import TextPageController
from outwiker.pages.search.searchpagecontroller import SearchPageController


logger = logging.getLogger("outwiker.app.gui.mainwindow")


class MainWindow(wx.Frame):
    def __init__(self, application):
        super().__init__(None)
        logger.debug("MainWindow initializing begin")
        self._application = application

        # Variables to accurate watch for main window state
        self._realSize = None
        self._realPosition = None
        self._realMaximized = False

        self.mainWindowConfig = MainWindowConfig(self._application.config)

        # Флаг, обозначающий, что в цикле обработки стандартных сообщений
        # (например, копирования в буфер обмена) сообщение вернулось обратно
        self.__stdEventLoop = False

        logger.debug("MainWindow initializing end")

    def updateTrayIcon(self):
        self.trayController.updateTrayIcon()

    def showTrayIcon(self):
        self.trayController.showTrayIcon()

    def removeTrayIcon(self):
        self.trayController.removeTrayIcon()

    def hideToTray(self):
        self.Iconize()
        self.Hide()
        self.showTrayIcon()

    def _createMenu(self):
        logger.debug("MainWindow. Create the main menu")
        self._mainMenu = wx.MenuBar()
        self.SetMenuBar(self._mainMenu)
        self.menuController = MenuController(self._mainMenu)

        self.menuController.createSubMenu(guidefines.MENU_FILE, _("File"))

        self.menuController.createSubMenu(guidefines.MENU_EDIT, _("Edit"))

        self.menuController.createSubMenu(guidefines.MENU_TREE, _("Tree"))

        self.menuController.createSubMenu(guidefines.MENU_TOOLS, _("Tools"))

        self.menuController.createSubMenu(guidefines.MENU_BOOKMARKS, _("Bookmarks"))

        self.menuController.createSubMenu(guidefines.MENU_VIEW, _("View"))
        self.menuController.createSubMenu(
            guidefines.MENU_VIEW_GOTO, _("Go to"), guidefines.MENU_VIEW
        )

        self.menuController.createSubMenu(guidefines.MENU_HELP, _("Help"))

    def _createToolbars(self):
        toolbars_menu = self.menuController.createSubMenu(
            guidefines.MENU_TOOLBARS, _("Toolbars"), guidefines.MENU_VIEW
        )

        self._toolbars = ToolBarsController(
            toolbars_menu, self._toolbarContainer, self._application.config
        )

        self._toolbars.createToolBar(
            guidefines.TOOLBAR_GENERAL,
            _("General"),
            order=guidefines.TOOLBAR_ORDER_GENERAL,
        )

        self._toolbars.createToolBar(
            guidefines.TOOLBAR_PLUGINS,
            _("Plugins"),
            order=guidefines.TOOLBAR_ORDER_PLUGINS_OTHER,
        )

    def _initCoreControllers(self):
        [controller.initialize() for controller in self._coreControllers]

    def _destroyCoreControllers(self):
        # TODO: the clear() methods replace to destroy()
        [controller.clear() for controller in self._coreControllers]
        self._coreControllers = []

    def createGui(self):
        """
        Создать пункты меню, кнопки на панелях инструментов и т.п.
        """
        logger.debug("MainWindow createGui started")
        logger.debug("MainWindow. Setup icon")
        self._setIcon()
        self.SetTitle("OutWiker")
        self._createMenu()
        self._createStatusBar()

        if self.mainWindowConfig.maximized.value:
            self.Maximize()

        self._mainSizer = wx.FlexGridSizer(cols=1)
        self._mainSizer.AddGrowableCol(0)
        self._mainSizer.AddGrowableRow(1)
        self._toolbarContainer = ToolBar2Container(self)
        self._mainContentPanel = wx.Panel(self)

        self._mainSizer.Add(self._toolbarContainer, flag=wx.EXPAND)
        self._mainSizer.Add(self._mainContentPanel, flag=wx.EXPAND)
        self.SetSizer(self._mainSizer)

        logger.debug("MainWindow. Create the AuiManager")

        self.auiManager = wx.aui.AuiManager(
            self._mainContentPanel,
            flags=wx.aui.AUI_MGR_DEFAULT
            | wx.aui.AUI_MGR_LIVE_RESIZE
            | wx.aui.AUI_MGR_ALLOW_FLOATING,
        )

        self._createAuiPanes()
        self._createToolbars()

        logger.debug("MainWindow. Create the MainWndController")
        self.controller = MainWndController(self, self._application)
        self.controller.loadMainWindowParams()

        logger.debug("MainWindow. Create the MainPanesController")
        self.__panesController = MainPanesController(self._application, self)

        self._bindGuiEvents()

        logger.debug("MainWindow. Create the TabsController")
        self.tabsController = TabsController(
            self.pagePanel.panel.tabsCtrl, self._application
        )

        self.attachWatcher = AttachWatcher(
            self._application, guidefines.ATTACH_CHECK_PERIOD
        )

        self._coreControllers = [
            WikiPageController(self._application),
            HtmlPageController(self._application),
            TextPageController(self._application),
            SearchPageController(self._application),
            PrefController(self._application),
            self.attachWatcher,
        ]

        logger.debug("MainWindow. Initialize the core controllers")
        self._initCoreControllers()

        logger.debug("MainWindow. Create the tray icon")
        self.trayController = getTrayIconController(self._application, self)

        self.__panesController.loadPanesSize()
        self._addActionsGui()
        self.controller.enableGui()
        self.controller.updateRecentMenu()
        self.__panesController.updateViewMenu()
        self.treePanel.panel.addButtons()
        self.toaster = ToasterController(self, self._application)

        if self.mainWindowConfig.fullscreen.value:
            self._application.actionController.check(FullScreenAction.stringId, True)
        logger.debug("MainWindow createGui ended")

    def _createSwitchToMenu(self):
        actionController = self._application.actionController
        menu = self.menuController[guidefines.MENU_VIEW_GOTO]

        actionController.appendMenuItem(switchto.SwitchToMainPanelAction.stringId, menu)

        actionController.appendMenuItem(switchto.SwitchToTreeAction.stringId, menu)

        actionController.appendMenuItem(
            switchto.SwitchToAttachmentsAction.stringId, menu
        )

        actionController.appendMenuItem(switchto.SwitchToTagsCloudAction.stringId, menu)

    def _createEditMenu(self):
        editMenu = self.menuController[guidefines.MENU_EDIT]

        editMenu.Append(wx.ID_UNDO, _("Undo") + "\tCtrl+Z", "", wx.ITEM_NORMAL)

        editMenu.Append(wx.ID_REDO, _("Redo") + "\tCtrl+Y", "", wx.ITEM_NORMAL)

        editMenu.AppendSeparator()

        editMenu.Append(wx.ID_CUT, _("Cut") + "\tCtrl+X", "", wx.ITEM_NORMAL)

        editMenu.Append(wx.ID_COPY, _("Copy") + "\tCtrl+C", "", wx.ITEM_NORMAL)

        editMenu.Append(wx.ID_PASTE, _("Paste") + "\tCtrl+V", "", wx.ITEM_NORMAL)

        editMenu.AppendSeparator()

        editMenu.Append(
            wx.ID_SELECTALL, _("Select All") + "\tCtrl+A", "", wx.ITEM_NORMAL
        )

    def _createFileMenu(self):
        """
        Заполнить действиями меню Файл
        """
        toolbar = self.toolbars[guidefines.TOOLBAR_GENERAL]
        menu = self.menuController[guidefines.MENU_FILE]
        actionController = self._application.actionController

        # Create new...
        actionController.appendMenuItem(NewAction.stringId, menu)

        actionController.appendToolbarButton(
            NewAction.stringId, toolbar, getBuiltinImagePath("new.svg"), True
        )

        # Opem...
        actionController.appendMenuItem(OpenAction.stringId, menu)

        actionController.appendToolbarButton(
            OpenAction.stringId, toolbar, getBuiltinImagePath("open.svg"), True
        )

        # Open read only
        actionController.appendMenuItem(OpenReadOnlyAction.stringId, menu)

        menu.AppendSeparator()
        toolbar.AddSeparator()

        # Close
        actionController.appendMenuItem(CloseAction.stringId, menu)

        # Save
        actionController.appendMenuItem(SaveAction.stringId, menu)

        actionController.appendMenuItem(ReloadWikiAction.stringId, menu)

        menu.AppendSeparator()

        # Print
        actionController.appendMenuItem(PrintAction.stringId, menu)

        # Exit
        actionController.appendMenuItem(ExitAction.stringId, menu)

        menu.AppendSeparator()

    def _createTreeMenu(self):
        """
        Заполнить действиями меню Дерево
        """
        actionController = self._application.actionController
        menu = self.menuController[guidefines.MENU_TREE]
        toolbar = self.toolbars[guidefines.TOOLBAR_GENERAL]

        actionController.appendMenuItem(HistoryBackAction.stringId, menu)

        actionController.appendToolbarButton(
            HistoryBackAction.stringId, toolbar, getBuiltinImagePath("back.svg"), True
        )

        actionController.enableTools(HistoryBackAction.stringId, False)

        actionController.appendMenuItem(HistoryForwardAction.stringId, menu)

        actionController.appendToolbarButton(
            HistoryForwardAction.stringId,
            toolbar,
            getBuiltinImagePath("forward.svg"),
            True,
        )

        actionController.enableTools(HistoryForwardAction.stringId, False)

        toolbar.AddSeparator()
        menu.AppendSeparator()

        actionController.appendMenuItem(AddSiblingPageAction.stringId, menu)
        actionController.appendMenuItem(AddChildPageAction.stringId, menu)
        actionController.appendMenuItem(RenamePageAction.stringId, menu)
        actionController.appendMenuItem(RemovePageAction.stringId, menu)

        menu.AppendSeparator()

        self._createMovementSubmenu()
        self._createGoToSubmenu()

        menu.AppendSeparator()

        actionController.appendMenuItem(EditPagePropertiesAction.stringId, menu)

    def _createMovementSubmenu(self):
        menu = self.menuController[guidefines.MENU_TREE]
        actionController = self._application.actionController
        submenu = wx.Menu()

        actionController.appendMenuItem(MovePageUpAction.stringId, submenu)
        actionController.appendMenuItem(MovePageDownAction.stringId, submenu)
        actionController.appendMenuItem(SortChildAlphabeticalAction.stringId, submenu)
        actionController.appendMenuItem(SortSiblingsAlphabeticalAction.stringId, submenu)

        menu.AppendSubMenu(submenu, _("Movement"))

    def _createGoToSubmenu(self):
        menu = self.menuController[guidefines.MENU_TREE]
        actionController = self._application.actionController
        submenu = wx.Menu()

        actionController.appendMenuItem(GoToParentAction.stringId, submenu)
        actionController.appendMenuItem(GoToFirstChildAction.stringId, submenu)
        actionController.appendMenuItem(GoToPrevSiblingAction.stringId, submenu)
        actionController.appendMenuItem(GoToNextSiblingAction.stringId, submenu)

        menu.AppendSubMenu(submenu, _("Go to"))

    def _createToolsMenu(self):
        toolbar = self.toolbars[guidefines.TOOLBAR_GENERAL]
        menu = self.menuController[guidefines.MENU_TOOLS]
        actionController = self._application.actionController

        self._createTabsSubmenu()
        self._createAtachmentsSubmenu()
        self._createPathsSubmenu()
        self._createTagsSubmenu()

        menu.AppendSeparator()

        actionController.appendMenuItem(GlobalSearchAction.stringId, menu)

        actionController.appendToolbarButton(
            GlobalSearchAction.stringId,
            toolbar,
            getBuiltinImagePath("global_search.svg"),
            True,
        )

        actionController.appendMenuItem(SetStyleToBranchAction.stringId, menu)

        menu.AppendSeparator()

    def _createTabsSubmenu(self):
        menu = self.menuController[guidefines.MENU_TOOLS]
        actionController = self._application.actionController
        submenu = wx.Menu()

        actionController.appendMenuItem(AddTabAction.stringId, submenu)
        actionController.appendMenuItem(CloseTabAction.stringId, submenu)
        actionController.appendMenuItem(PreviousTabAction.stringId, submenu)
        actionController.appendMenuItem(NextTabAction.stringId, submenu)

        menu.AppendSubMenu(submenu, _("Tabs"))

    def _createPathsSubmenu(self):
        menu = self.menuController[guidefines.MENU_TOOLS]
        actionController = self._application.actionController
        submenu = wx.Menu()

        actionController.appendMenuItem(CopyPageTitleAction.stringId, submenu)
        actionController.appendMenuItem(CopyPagePathAction.stringId, submenu)
        actionController.appendMenuItem(CopyAttachPathAction.stringId, submenu)
        actionController.appendMenuItem(CopyPageLinkAction.stringId, submenu)

        menu.AppendSubMenu(submenu, _("Paths"))

    def _createAtachmentsSubmenu(self):
        toolbar = self.toolbars[guidefines.TOOLBAR_GENERAL]
        menu = self.menuController[guidefines.MENU_TOOLS]
        actionController = self._application.actionController
        submenu = wx.Menu()

        actionController.appendMenuItem(AttachFilesAction.stringId, submenu)

        actionController.appendToolbarButton(
            AttachFilesAction.stringId, toolbar, getBuiltinImagePath("attach.svg"), True
        )

        actionController.appendMenuItem(AttachFolderAction.stringId, submenu)

        actionController.appendToolbarButton(
            AttachFolderAction.stringId,
            toolbar,
            getBuiltinImagePath("attach_folder.svg"),
            True,
        )

        actionController.appendMenuItem(AttachCreateSubdirAction.stringId, submenu)
        actionController.appendMenuItem(OpenAttachFolderAction.stringId, submenu)

        menu.AppendSubMenu(submenu, _("Attachments"))

    def _createTagsSubmenu(self):
        menu = self.menuController[guidefines.MENU_TOOLS]
        actionController = self._application.actionController
        submenu = wx.Menu()

        actionController.appendMenuItem(tags.AddTagsToBranchAction.stringId, submenu)
        actionController.appendMenuItem(tags.RemoveTagsFromBranchAction.stringId, submenu)
        actionController.appendMenuItem(tags.RenameTagAction.stringId, submenu)
        menu.AppendSubMenu(submenu, _("Tags"))

    def _createHelpMenu(self):
        menu = self.menuController[guidefines.MENU_HELP]
        actionController = self._application.actionController

        actionController.appendMenuItem(OpenHelpAction.stringId, menu)
        actionController.appendMenuItem(AboutAction.stringId, menu)
        actionController.appendMenuItem(OpenPluginsFolderAction.stringId, menu)

    def _addActionsGui(self):
        """
        Создать элементы интерфейса, привязанные к actions
        """
        self._createFileMenu()
        self._createEditMenu()
        self._createTreeMenu()
        self._createToolsMenu()
        self._createHelpMenu()
        self._createSwitchToMenu()
        self.__panesController.createViewMenuItems()

        actionController = self._application.actionController

        viewMenu = self.menuController[guidefines.MENU_VIEW]
        viewMenu.AppendSeparator()

        # Полноэкранный режим
        actionController.appendMenuCheckItem(FullScreenAction.stringId, viewMenu)

        # Вызов диалога настроек
        menu_edit = self.menuController[guidefines.MENU_EDIT]
        menu_edit.AppendSeparator()

        actionController.appendMenuItem(PreferencesAction.stringId, menu_edit)

        # Добавление / удаление закладки
        menu_bookmarks = self.menuController[guidefines.MENU_BOOKMARKS]
        actionController.appendMenuItem(AddBookmarkAction.stringId, menu_bookmarks)

        menu_bookmarks.AppendSeparator()

    def UpdateAuiManager(self):
        """
        Обновление auiManager. Сделано для облегчения доступа
        """
        if self.auiManager:
            self.auiManager.Update()

    def _createAuiPanes(self):
        """
        Создание плавающих панелей
        """
        self.pagePanel = PageMainPane(
            self._mainContentPanel, self.auiManager, self._application
        )
        self.treePanel = TreeMainPane(
            self._mainContentPanel, self.auiManager, self._application
        )
        self.attachPanel = AttachMainPane(
            self._mainContentPanel, self.auiManager, self._application
        )
        self.tagsCloudPanel = TagsCloudMainPane(
            self._mainContentPanel, self.auiManager, self._application
        )

    def _createStatusBar(self):
        """
        Создание статусной панели
        """
        self._statusbar = wx.StatusBar(self, -1)
        self.SetStatusBar(self._statusbar)
        self._statusBarController = StatusBarController(
            self._statusbar, self._application
        )

    def _bindGuiEvents(self):
        """
        Подписаться на события меню, кнопок и т.п.
        """
        self.Bind(wx.EVT_MENU, self._onStdEvent, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, self._onStdEvent, id=wx.ID_REDO)
        self.Bind(wx.EVT_MENU, self._onStdEvent, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU, self._onStdEvent, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, self._onStdEvent, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, self._onStdEvent, id=wx.ID_SELECTALL)
        self.Bind(wx.EVT_SIZE, self._onSizeMove)
        self.Bind(wx.EVT_MOVE, self._onSizeMove)

    def _saveParams(self):
        """
        Сохранить параметры в конфиг
        """
        self._updateRealSize()
        try:
            if not self.IsIconized():
                self.mainWindowConfig.fullscreen.value = self.IsFullScreen()
                self.__panesController.savePanesParams()

            if self._realSize:
                (width, height) = self._realSize
                self.mainWindowConfig.width.value = width
                self.mainWindowConfig.height.value = height

            if self._realPosition:
                (xpos, ypos) = self._realPosition
                self.mainWindowConfig.xPos.value = xpos
                self.mainWindowConfig.yPos.value = ypos

            self.mainWindowConfig.maximized.value = self._realMaximized
        except Exception as e:
            showError(self, _("Can't save config\n%s") % (str(e)))

    def _setIcon(self):
        """
        Установки иконки главного окна
        """
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(getOS().windowIconFile, wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)

    def Destroy(self):
        """
        Убрать за собой
        """
        logger.debug("Begin MainWindow.Destroy.")

        self.toaster.destroy()
        self._statusBarController.destroy()
        self.pagePanel.panel.Save()
        self._application.plugins.clear()
        self._saveParams()
        self.destroyPagePanel(False)
        self.pagePanel.panel.Close()

        self._application.clear()
        self._application.actionController.destroy()
        self._application = None

        self._destroyCoreControllers()

        self.trayController.destroy()
        self.controller.destroy()

        self.auiManager.UnInit()
        self.auiManager.Destroy()

        super().Destroy()
        logger.debug("End MainWindow.Destroy.")

    def destroyPagePanel(self, save):
        """
        Уничтожить панель с текущей страницей.
        save - надо ли предварительно сохранить страницу?
        """
        if save:
            self.pagePanel.panel.destroyPageView()
        else:
            self.pagePanel.panel.destroyWithoutSave()

    def _onStdEvent(self, event):
        """
        Обработчик стандартных событий (копировать, вставить и т.п.)
        """
        if not self.__stdEventLoop:
            self.__stdEventLoop = True
            target = wx.Window.FindFocus()

            if target is not None:
                target.ProcessEvent(event)
                self.__stdEventLoop = False

    def _updateRealSize(self):
        if not self.IsIconized():
            self._realMaximized = self.IsMaximized()

        if not self.IsIconized() and not self.IsFullScreen() and not self.IsMaximized():
            self._realSize = self.GetSize()
            self._realPosition = self.GetPosition()

    def _onSizeMove(self, event):
        self._updateRealSize()
        event.Skip()

    def setFullscreen(self, fullscreen):
        """
        Установить параметры в зависимости от режима fullscreen
        """
        if fullscreen:
            self._toFullscreen()
        else:
            self._fromFullscreen()

    def _toFullscreen(self):
        """
        Переключение в полноэкранный режим
        """
        self.__panesController.savePanesParams()
        # The bug (?) in wxPython under Ubuntu spoils check items
        # after full screen mode
        if getOS().name != "unix":
            self.ShowFullScreen(
                True,
                (
                    wx.FULLSCREEN_NOTOOLBAR
                    | wx.FULLSCREEN_NOBORDER
                    | wx.FULLSCREEN_NOCAPTION
                ),
            )

        self.__panesController.toFullscreen()

    def _fromFullscreen(self):
        """
        Возврат из полноэкранного режима
        """
        self.controller.loadMainWindowParams()
        # The bug (?) in wxPython under Ubuntu spoils check items after
        # full screen mode
        if getOS().name != "unix":
            self.ShowFullScreen(False)

        self.__panesController.fromFullscreen()

    @property
    def toolbars(self):
        return self._toolbars

    @property
    def pageView(self):
        return self.pagePanel.pageView

    @property
    def statusbar(self) -> StatusBarController:
        return self._statusBarController
