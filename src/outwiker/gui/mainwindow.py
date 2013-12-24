#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

import wx
import wx.aui

import outwiker.core.config
import outwiker.core.commands as cmd
from outwiker.core.application import Application

import outwiker.pages.search.searchpage
from .guiconfig import MainWindowConfig

from .mainid import MainId
from .mainmenu import MainMenu
from .trayicon import OutwikerTrayIcon
from .mainwndcontroller import MainWndController
from .mainpanescontroller import MainPanesController
from .shortcuter import Shortcuter
from outwiker.gui.mainpanes.tagscloudmainpane import TagsCloudMainPane
from outwiker.gui.mainpanes.attachmainpane import AttachMainPane
from outwiker.gui.mainpanes.treemainpane import TreeMainPane
from outwiker.gui.mainpanes.pagemainpane import PageMainPane
from outwiker.gui.tabscontroller import TabsController
from outwiker.core.system import getImagesDir

from toolbars.generaltoolbar import GeneralToolBar
from toolbars.pluginstoolbar import PluginsToolBar
from toolbars.toolbarscontroller import ToolBarsController

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
from outwiker.actions.tabs import AddTabAction, CloseTabAction, PreviousTabAction, NextTabAction
from outwiker.actions.globalsearch import GlobalSearchAction


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.mainWindowConfig = MainWindowConfig (Application.config)

        # Флаг, обозначающий, что в цикле обработки стандартных сообщений 
        # (например, копирования в буфер обмена) сообщение вернулось обратно
        self.__stdEventLoop = False

        self.__setIcon()
        self.SetTitle (u"OutWiker")

        self.mainMenu = MainMenu()
        self.SetMenuBar(self.mainMenu)

        self.__createStatusBar()

        self.controller = MainWndController (self)
        self.controller.loadMainWindowParams()

        self.auiManager = wx.aui.AuiManager(self)
        self.__createAuiPanes ()

        self.GENERAL_TOOLBAR_STR = "general"
        self.PLUGINS_TOOLBAR_STR = "plugins"
        self.toolbars = ToolBarsController (self)

        self.toolbars[self.GENERAL_TOOLBAR_STR] = GeneralToolBar (self, 
                self.auiManager)

        self.toolbars[self.PLUGINS_TOOLBAR_STR] = PluginsToolBar (self, 
                self.auiManager)

        self.__panesController = MainPanesController (Application, self)

        self.__bindGuiEvents()

        self._dropTarget = DropFilesTarget (self.attachPanel.panel)
        self.Show()

        if self.mainWindowConfig.maximized.value:
            self.Maximize()

        self.taskBarIcon = OutwikerTrayIcon(self)
        self.tabsController = TabsController (self.pagePanel.panel.tabsCtrl, 
                Application)


    def createGui (self):
        """
        Создать пункты меню, кнопки на панелях инструментов и т.п.
        """
        self.__panesController.loadPanesSize ()
        self.__addActionsGui()
        self.controller.enableGui()
        self.controller.updateRecentMenu()
        self.__panesController.updateViewMenu()
        self.treePanel.panel.addButtons()
        self.updateShortcuts()

        if self.mainWindowConfig.fullscreen.value:
            Application.actionController.check (FullScreenAction.stringId, True)


    def __createFileMenu (self):
        """
        Заполнить действиями меню Файл
        """
        imagesDir = getImagesDir()

        # Открыть...
        Application.actionController.appendMenuItem (OpenAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        Application.actionController.appendToolbarButton (OpenAction.stringId, 
                Application.mainWindow.mainToolbar,
                os.path.join (imagesDir, u"open.png"),
                True)

        # Создать...
        Application.actionController.appendMenuItem (NewAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        Application.actionController.appendToolbarButton (NewAction.stringId, 
                Application.mainWindow.mainToolbar,
                os.path.join (imagesDir, u"new.png"),
                True)

        # Открыть только для чтения
        Application.actionController.appendMenuItem (OpenReadOnlyAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        Application.mainWindow.mainMenu.fileMenu.AppendSeparator()
        Application.mainWindow.mainToolbar.AddSeparator()

        # Закрыть
        Application.actionController.appendMenuItem (CloseAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        # Сохранить
        Application.actionController.appendMenuItem (SaveAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        Application.mainWindow.mainMenu.fileMenu.AppendSeparator()

        # Печать
        Application.actionController.appendMenuItem (PrintAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        # Выход
        Application.actionController.appendMenuItem (ExitAction.stringId, 
                Application.mainWindow.mainMenu.fileMenu)

        Application.mainWindow.mainMenu.fileMenu.AppendSeparator()


    def __createTreeMenu (self):
        """
        Заполнить действиями меню Дерево
        """
        imagesDir = getImagesDir()

        Application.actionController.appendMenuItem (AddSiblingPageAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.actionController.appendMenuItem (AddChildPageAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.mainWindow.mainMenu.treeMenu.AppendSeparator()


        Application.actionController.appendMenuItem (MovePageUpAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.actionController.appendMenuItem (MovePageDownAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.actionController.appendMenuItem (SortChildAlphabeticalAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.actionController.appendMenuItem (SortSiblingsAlphabeticalAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.mainWindow.mainMenu.treeMenu.AppendSeparator()


        Application.actionController.appendMenuItem (RenamePageAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.actionController.appendMenuItem (RemovePageAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)

        Application.mainWindow.mainMenu.treeMenu.AppendSeparator()

        Application.actionController.appendMenuItem (EditPagePropertiesAction.stringId, 
                Application.mainWindow.mainMenu.treeMenu)


    def __createToolsMenu (self):
        imagesDir = getImagesDir()
        menu = Application.mainWindow.mainMenu.toolsMenu
        actionController = Application.actionController

        actionController.appendMenuItem (
                AddTabAction.stringId, 
                menu)

        actionController.appendMenuItem (
                CloseTabAction.stringId, 
                menu)

        actionController.appendMenuItem (
                PreviousTabAction.stringId, 
                menu)

        actionController.appendMenuItem (
                NextTabAction.stringId, 
                menu)

        menu.AppendSeparator()

        actionController.appendMenuItem (
                GlobalSearchAction.stringId, 
                menu)

        actionController.appendToolbarButton (GlobalSearchAction.stringId, 
                Application.mainWindow.mainToolbar,
                os.path.join (imagesDir, u"global_search.png"),
                True)



    def __addActionsGui (self):
        """
        Создать элементы интерфейса, привязанные к actions
        """
        imagesDir = getImagesDir()

        self.__createFileMenu ()
        self.__createTreeMenu ()
        self.__createToolsMenu ()

        self.__panesController.createViewMenuItems ()

        Application.mainWindow.mainMenu.viewMenu.AppendSeparator()

        # Полноэкранный режим
        Application.actionController.appendMenuCheckItem (FullScreenAction.stringId, 
                self.mainMenu.viewMenu)

        # Вызов диалога настроек
        Application.mainWindow.mainMenu.editMenu.AppendSeparator()

        Application.actionController.appendMenuItem (PreferencesAction.stringId,
                Application.mainWindow.mainMenu.editMenu)

        # Добавление / удаление закладки
        Application.actionController.appendMenuItem (AddBookmarkAction.stringId,
                Application.mainWindow.mainMenu.bookmarksMenu)

        Application.mainWindow.mainMenu.bookmarksMenu.AppendSeparator()


    @property
    def mainToolbar (self):
        """
        Доступ к основной панели инструментов
        """
        return self.toolbars[self.GENERAL_TOOLBAR_STR]


    def updateShortcuts (self):
        """
        Обновить шорткаты (буквы с подчеркиванием) в меню
        """
        Shortcuter (self.mainMenu).assignShortcuts()


    def UpdateAuiManager (self):
        """
        Обновление auiManager. Сделано для облегчения доступа
        """
        self.auiManager.Update()


    def __createAuiPanes(self):
        """
        Создание плавающих панелей
        """
        self.pagePanel = PageMainPane (
                self, 
                self.auiManager, 
                Application)

        self.treePanel = TreeMainPane (
                self, 
                self.auiManager, 
                Application)

        self.attachPanel = AttachMainPane (
                self, 
                self.auiManager, 
                Application)

        self.tagsCloudPanel = TagsCloudMainPane (
                self, 
                self.auiManager, 
                Application)


    def __createStatusBar (self):
        """
        Создание статусной панели
        """
        self.statusbar = wx.StatusBar(self, -1)

        items_count = 2
        self.statusbar.SetFieldsCount(items_count)
        self.statusbar.SetStatusWidths ([-1, 200])
        self.SetStatusBar (self.statusbar)


    def __bindGuiEvents (self):
        """
        Подписаться на события меню, кнопок и т.п.
        """
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_UNDO)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_REDO)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_CUT)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_COPY)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_PASTE)

        self.Bind (wx.EVT_MENU, self.__onAttach, id=MainId.ID_ATTACH)
        self.Bind (wx.EVT_MENU, self.__onCopyTitle, id=MainId.ID_COPY_TITLE)
        self.Bind (wx.EVT_MENU, self.__onCopyPath, id=MainId.ID_COPYPATH)

        self.Bind (wx.EVT_MENU, 
                self.__onCopyAttaches, 
                id=MainId.ID_COPY_ATTACH_PATH)

        self.Bind (wx.EVT_MENU, self.__onCopyLink, id=MainId.ID_COPY_LINK)
        self.Bind (wx.EVT_MENU, self.__onReload, id=MainId.ID_RELOAD)

        self.Bind (wx.EVT_MENU, self.__onHelp, id=MainId.ID_HELP)
        self.Bind (wx.EVT_MENU, self.__onAbout, id=MainId.ID_ABOUT)
        self.Bind (wx.EVT_TOOL, self.__onReload, id=MainId.ID_RELOAD)
        self.Bind (wx.EVT_TOOL, self.__onAttach, id=MainId.ID_ATTACH)

        self.Bind (wx.EVT_TOOL, 
                self.__onAddTagsToBranch, 
                id=MainId.ID_ADD_TAGS_TO_BRANCH)

        self.Bind (wx.EVT_TOOL, 
                self.__onRemoveTagsFromBranch, 
                id=MainId.ID_REMOVE_TAGS_FROM_BRANCH)

        self.Bind (wx.EVT_TOOL, self.__onRenameTag, id=MainId.ID_RENAME_TAG)


    def __saveParams (self):
        """
        Сохранить параметры в конфиг
        """
        try:
            if not self.IsIconized():
                if (not self.IsFullScreen() and
                        not self.IsMaximized()):
                    (width, height) = self.GetSizeTuple()
                    (xpos, ypos) = self.GetPositionTuple()

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
        except Exception, e:
            cmd.MessageBox (_(u"Can't save config\n%s") % (unicode (e)),
                    _(u"Error"), wx.ICON_ERROR | wx.OK)
    

    def __setIcon (self):
        """
        Установки иконки главного окна
        """
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join (getImagesDir(), 
            "outwiker.ico"), 
            wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)


    def Destroy(self):
        """
        Убрать за собой
        """
        self.__saveParams()
        Application.actionController.saveHotKeys()

        self.tabsController.destroy()
        self.toolbars.destroyAllToolBars()

        self.auiManager.UnInit()

        self.pagePanel.close()
        self.__panesController.closePanes()

        self.statusbar.Close()
        self.taskBarIcon.Destroy()
        self.controller.destroy()

        super (MainWindow, self).Destroy()
    

    def __onReload(self, event):
        """
        Обработчик события перезагрузки вики
        """
        cmd.reloadWiki (self)
    

    def destroyPagePanel (self, save):
        """
        Уничтожить панель с текущей страницей.
        save - надо ли предварительно сохранить страницу?
        """
        if save:
            self.pagePanel.panel.destroyPageView()
        else:
            self.pagePanel.panel.destroyWithoutSave()


    def __onAttach(self, event):
        """
        Обработчик события прикрепления файлов к странице
        """
        if Application.selectedPage != None:
            cmd.attachFilesWithDialog (self, 
                    Application.wikiroot.selectedPage)


    def __onAbout(self, event):
        """
        Обработчик события показа диалога "О программе"
        """
        cmd.showAboutDialog (self)


    def __onCopyPath(self, event):
        """
        Обработчик события копирования пути до текущей страницы в буфер обмена
        """
        if Application.selectedPage != None:
            cmd.copyPathToClipboard (Application.wikiroot.selectedPage)


    def __onCopyAttaches(self, event):
        """
        Обработчик события копирования пути до прикрепленных файлов в буфер обмена
        """
        if Application.selectedPage != None:
            cmd.copyAttachPathToClipboard (Application.wikiroot.selectedPage)

    
    def __onCopyLink(self, event):
        """
        Обработчик события копирования ссылки на текущую страницу в буфер обмена
        """
        if Application.selectedPage != None:
            cmd.copyLinkToClipboard (Application.wikiroot.selectedPage)

    
    def __onCopyTitle(self, event):
        """
        Обработчик события копирования заголовка текущей страницы в буфер обмена
        """
        if Application.selectedPage != None:
            cmd.copyTitleToClipboard (Application.wikiroot.selectedPage)
    

    def __onStdEvent(self, event):
        """
        Обработчик стандартных событий (копировать, вставить и т.п.)
        """
        if not self.__stdEventLoop:
            self.__stdEventLoop = True
            target = wx.Window.FindFocus()

            if target != None:
                target.ProcessEvent (event)
        self.__stdEventLoop = False


    def __onHelp(self, event):
        """
        Обработчик события вызова справки
        """
        cmd.openHelp()


    def setFullscreen (self, fullscreen):
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
        self.ShowFullScreen(True, 
                (wx.FULLSCREEN_NOTOOLBAR | 
                    wx.FULLSCREEN_NOBORDER | 
                    wx.FULLSCREEN_NOCAPTION))

        self.__panesController.hidePanes()
        self.__panesController.updateViewMenu()


    def __fromFullscreen (self):
        """
        Возврат из полноэкранного режима
        """
        self.controller.loadMainWindowParams()
        self.ShowFullScreen(False)

        self.__panesController.showPanes()
        self.__panesController.loadPanesSize ()
        self.__panesController.updateViewMenu()

    
    def __onAddTagsToBranch (self, event):
        """
        Обработчик события добавления меток к ветке
        """
        if Application.wikiroot == None:
            return

        if Application.selectedPage == None:
            cmd.addTagsToBranchGui (Application.wikiroot, 
                    self)
        else:
            cmd.addTagsToBranchGui (Application.selectedPage, self)


    def __onRemoveTagsFromBranch (self, event):
        """
        Обработчик события удаления меток из ветки
        """
        if Application.wikiroot == None:
            return

        if Application.selectedPage == None:
            cmd.removeTagsFromBranchGui (Application.wikiroot, self)
        else:
            cmd.removeTagsFromBranchGui (Application.selectedPage, self)


    def __onRenameTag (self, event):
        """
        Обработчик события переименования метки
        """
        if Application.wikiroot != None:
            cmd.renameTagGui (Application.wikiroot, self)

# end of class MainWindow


class DropFilesTarget (wx.FileDropTarget):
    """
    Класс для возможности перетаскивания файлов между другими программами и OutWiker
    """
    def __init__ (self, mainWindow):
        wx.FileDropTarget.__init__ (self)
        self._mainWindow = mainWindow
        self._mainWindow.SetDropTarget (self)
    
    
    def OnDropFiles (self, x, y, files):
        if (Application.wikiroot != None and
                Application.wikiroot.selectedPage != None):
            cmd.attachFiles (self._mainWindow, 
                        Application.wikiroot.selectedPage, 
                        files)
            return True
