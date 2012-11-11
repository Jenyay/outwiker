#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

import wx
import wx.aui

from outwiker.core.tree import WikiDocument, RootWikiPage
import outwiker.core.config
import outwiker.core.commands as cmd
import outwiker.core.system
from outwiker.core.application import Application

import outwiker.pages.search.searchpage
from .guiconfig import MainWindowConfig

from .mainid import MainId
from .mainmenu import MainMenu
from .pagedialog import createSiblingPage, createChildPage, editPage
from .trayicon import OutwikerTrayIcon
from .preferences.prefdialog import PrefDialog
from .mainwndcontroller import MainWndController
from .mainpanescontroller import MainPanesController
from outwiker.gui.mainpanes.tagscloudmainpane import TagsCloudMainPane
from outwiker.gui.mainpanes.attachmainpane import AttachMainPane
from outwiker.gui.mainpanes.treemainpane import TreeMainPane
from outwiker.gui.mainpanes.pagemainpane import PageMainPane
from outwiker.gui.tabscontroller import TabsController
from outwiker.core.system import getImagesDir

from toolbars.generaltoolbar import GeneralToolBar
from toolbars.pluginstoolbar import PluginsToolBar
from toolbars.toolbarscontroller import ToolBarsController


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

        self.__panesController = MainPanesController (self, self.auiManager)

        self.__bindGuiEvents()

        self._dropTarget = DropFilesTarget (self.attachPanel.panel)
        self.controller.enableGui()
        self.controller.updateRecentMenu()
        self.__panesController.updateViewMenu()
        self.Show()

        if self.mainWindowConfig.maximized.value:
            self.Maximize()

        self.taskBarIcon = OutwikerTrayIcon(self)
        self.tabsController = TabsController (self.pagePanel.panel.tabsCtrl, 
                Application)


    @property
    def mainToolbar (self):
        """
        Доступ к основной панели инструментов
        """
        return self.toolbars[self.GENERAL_TOOLBAR_STR]


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
                Application, 
                None)

        self.treePanel = TreeMainPane (
                self, 
                self.auiManager, 
                Application, 
                self.mainMenu.viewNotes)

        self.attachPanel = AttachMainPane (
                self, 
                self.auiManager, 
                Application, 
                self.mainMenu.viewAttaches)

        self.tagsCloudPanel = TagsCloudMainPane (
                self, 
                self.auiManager, 
                Application, 
                self.mainMenu.viewTagsCloud)


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
        self.Bind (wx.EVT_MENU, self.__onNew, id=MainId.ID_NEW)
        self.Bind (wx.EVT_MENU, self.__onOpen, id=MainId.ID_OPEN)
        self.Bind (wx.EVT_MENU, self.__onClose, id=MainId.ID_CLOSE)

        self.Bind (wx.EVT_MENU, 
                self.__onOpenReadOnly, 
                id=MainId.ID_OPEN_READONLY)

        self.Bind (wx.EVT_MENU, self.__onSave, id=MainId.ID_SAVE)
        self.Bind (wx.EVT_MENU, self.__onPrint, id=wx.ID_PRINT)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_UNDO)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_REDO)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_CUT)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_COPY)
        self.Bind (wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_PASTE)
        self.Bind (wx.EVT_MENU, self.__onPreferences, id=MainId.ID_PREFERENCES)
        self.Bind (wx.EVT_MENU, self.__onAddSiblingPage, id=MainId.ID_ADDPAGE)
        self.Bind (wx.EVT_MENU, self.__onAddChildPage, id=MainId.ID_ADDCHILD)
        self.Bind (wx.EVT_MENU, self.__onMovePageUp, id=MainId.ID_MOVE_PAGE_UP)

        self.Bind (wx.EVT_MENU, 
                self.__onMovePageDown, 
                id=MainId.ID_MOVE_PAGE_DOWN)

        self.Bind (wx.EVT_MENU, 
                self.__onSortChildrenAlphabetical, 
                id=MainId.ID_SORT_CHILDREN_ALPHABETICAL)

        self.Bind (wx.EVT_MENU, 
                self.__onSortSiblingAlphabetical, 
                id=MainId.ID_SORT_SIBLINGS_ALPHABETICAL)

        self.Bind (wx.EVT_MENU, self.__onRename, id=MainId.ID_RENAME)

        self.Bind (wx.EVT_MENU, 
                self.__onRemovePage, 
                id=MainId.ID_REMOVE_PAGE)

        self.Bind (wx.EVT_MENU, self.__onEditPage, id=MainId.ID_EDIT)

        self.Bind (wx.EVT_MENU, 
                self.__onGlobalSearch, 
                id=MainId.ID_GLOBAL_SEARCH)

        self.Bind (wx.EVT_MENU, self.__onAttach, id=MainId.ID_ATTACH)
        self.Bind (wx.EVT_MENU, self.__onCopyTitle, id=MainId.ID_COPY_TITLE)
        self.Bind (wx.EVT_MENU, self.__onCopyPath, id=MainId.ID_COPYPATH)

        self.Bind (wx.EVT_MENU, 
                self.__onCopyAttaches, 
                id=MainId.ID_COPY_ATTACH_PATH)

        self.Bind (wx.EVT_MENU, self.__onCopyLink, id=MainId.ID_COPY_LINK)
        self.Bind (wx.EVT_MENU, self.__onReload, id=MainId.ID_RELOAD)

        self.Bind (wx.EVT_MENU, 
                self.__onFullscreen, 
                self.mainMenu.viewFullscreen)

        self.Bind (wx.EVT_MENU, self.__onHelp, id=MainId.ID_HELP)
        self.Bind (wx.EVT_MENU, self.__onAbout, id=MainId.ID_ABOUT)
        self.Bind (wx.EVT_TOOL, self.__onNew, id=MainId.ID_NEW)
        self.Bind (wx.EVT_TOOL, self.__onOpen, id=MainId.ID_OPEN)
        self.Bind (wx.EVT_TOOL, self.__onReload, id=MainId.ID_RELOAD)
        self.Bind (wx.EVT_TOOL, self.__onAttach, id=MainId.ID_ATTACH)

        self.Bind (wx.EVT_TOOL, 
                self.__onGlobalSearch, 
                id=MainId.ID_GLOBAL_SEARCH)

        self.Bind (wx.EVT_TOOL, 
                self.__onAddTagsToBranch, 
                id=MainId.ID_ADD_TAGS_TO_BRANCH)

        self.Bind (wx.EVT_TOOL, 
                self.__onRemoveTagsFromBranch, 
                id=MainId.ID_REMOVE_TAGS_FROM_BRANCH)

        self.Bind (wx.EVT_TOOL, self.__onRenameTag, id=MainId.ID_RENAME_TAG)
        self.Bind (wx.EVT_TOOL, self.__onAddNewTab, id=MainId.ID_ADD_TAB)
        self.Bind (wx.EVT_TOOL, self.__onCloseTab, id=MainId.ID_CLOSE_TAB)
        self.Bind (wx.EVT_TOOL, self.__onNextTab, id=MainId.ID_NEXT_TAB)
        self.Bind (wx.EVT_TOOL, self.__onPrevTab, id=MainId.ID_PREV_TAB)


    def __onNextTab (self, event):
        """
        Обработчик события переключения на следующую вкладку
        """
        cmd.nextTab (Application)


    def __onPrevTab (self, event):
        """
        Обработчик события переключения на предыдущую вкладку
        """
        cmd.previousTab (Application)


    def __onAddNewTab (self, event):
        """
        Обработчик события добавления новой вкладки
        """
        cmd.addNewTab (Application)


    def __onCloseTab (self, event):
        """
        Обработчик события закрытия вкладки
        """
        cmd.closeCurrentTab (Application)


    def __onClose (self, event):
        """
        Обработчик события закрытия программы
        """
        cmd.closeWiki (Application)

    
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
        icon.CopyFromBitmap(wx.Bitmap(os.path.join (outwiker.core.system.getImagesDir(), 
            "outwiker.ico"), 
            wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)


    def Destroy(self):
        """
        Убрать за собой
        """
        self.__saveParams()

        self.tabsController.destroy()
        self.toolbars.destroyAllToolBars()

        self.auiManager.UnInit()

        self.pagePanel.close()
        self.__panesController.closePanes()

        self.statusbar.Close()
        self.taskBarIcon.Destroy()
        self.controller.destroy()

        super (MainWindow, self).Destroy()
    

    def __onNew(self, event):
        """
        Обработчик события создания новой вики
        """
        cmd.createNewWiki(self)


    def __onOpen(self, event):
        """
        Обработчик события открытия вики
        """
        cmd.openWikiWithDialog (self)
    

    def __onSave(self, event):
        """
        Обработчик события принудительного сохранения вики
        """
        Application.onForceSave()


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


    def __onAddSiblingPage(self, event):
        """
        Создание страницы на уровне текущей страницы
        """
        createSiblingPage (self)

    
    def __onAddChildPage(self, event):
        """
        Создание дочерней страницы
        """
        createChildPage (self)


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
    

    def __onEditPage(self, event):
        """
        Обработчик события изменения настроек страницы
        """
        if Application.selectedPage != None:
            editPage (self, Application.selectedPage)


    def __onRemovePage(self, event):
        """
        Обработчик события удаления текущей страницы
        """
        if Application.selectedPage != None:
            cmd.removePage (Application.wikiroot.selectedPage)


    @cmd.testreadonly
    def __onGlobalSearch(self, event):
        """
        Обработчик события создания или показа страницы глобального поиска
        """
        if Application.wikiroot != None:
            try:
                outwiker.pages.search.searchpage.GlobalSearch.create (Application.wikiroot)
            except IOError:
                cmd.MessageBox (_(u"Can't create page"), 
                        _(u"Error"), 
                        wx.ICON_ERROR | wx.OK)


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


    def __onRename(self, event):
        """
        Обработчик события переименования текущей страницы
        """
        self.treePanel.beginRename()


    def __onHelp(self, event):
        """
        Обработчик события вызова справки
        """
        cmd.openHelp()


    def __onOpenReadOnly(self, event):
        """
        Обработчик события открытия вики в режиме "только для чтения"
        """
        cmd.openWikiWithDialog (self, readonly=True)


    def __onPreferences(self, event):
        """
        Обработчик события вызова диалога настроек программы
        """
        dlg = PrefDialog (self)
        dlg.ShowModal()
        dlg.Destroy()
    

    def __onFullscreen(self, event):
        """
        Обработчик события переключения в полноэкранный режим
        """
        self.setFullscreen(not self.IsFullScreen())


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

    
    def __onMovePageUp(self, event):
        """
        Обработчик события перемещения страницы вверх
        """
        cmd.moveCurrentPageUp()


    def __onMovePageDown(self, event):
        """
        Обработчик события перемещения страницы вниз
        """
        cmd.moveCurrentPageDown()
        

    def __onSortChildrenAlphabetical(self, event):
        """
        Обработчик события сортировки дочерних страниц по алфавиту
        """
        cmd.sortChildrenAlphabeticalGUI()


    def __onSortSiblingAlphabetical(self, event):
        """
        Обработчик события сортировки братских страниц по алфавиту
        """
        cmd.sortSiblingsAlphabeticalGUI()


    def __onPrint(self, event):
        """
        Печать текущей страницы
        """
        self.pagePanel.panel.Print()


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
