#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

import wx
import wx.aui

from outwiker.core.tree import WikiDocument, RootWikiPage
import outwiker.core.config
import outwiker.core.commands
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

        self.mainMenu = None
        self.__createMenu()

        self.__createStatusBar()

        self.controller = MainWndController (self)
        self.controller.loadMainWindowParams()

        self.auiManager = wx.aui.AuiManager(self)
        self.__createAuiPanes ()

        self.GENERAL_TOOLBAR_STR = "general"
        self.PLUGINS_TOOLBAR_STR = "plugins"
        self.toolbars = ToolBarsController (self)
        self.toolbars[self.GENERAL_TOOLBAR_STR] = GeneralToolBar (self, self.auiManager)
        self.toolbars[self.PLUGINS_TOOLBAR_STR] = PluginsToolBar (self, self.auiManager)
        self.toolbars[self.PLUGINS_TOOLBAR_STR].UpdateToolBar()

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


    @property
    def generalToolBar (self):
        return self.toolbars[self.GENERAL_TOOLBAR_STR]


    def UpdateAuiManager (self):
        self.auiManager.Update()


    def __createAuiPanes(self):
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
        self.statusbar = wx.StatusBar(self, -1)
        self.statusbar.SetFieldsCount(1)
        self.SetStatusBar (self.statusbar)


    def __createMenu (self):
        self.mainMenu = MainMenu()
        self.SetMenuBar(self.mainMenu)


    def __bindGuiEvents (self):
        """
        Подписаться на события меню, кнопок и т.п.
        """
        self.Bind (wx.EVT_MENU, self.__onNew, id=MainId.ID_NEW)
        self.Bind (wx.EVT_MENU, self.__onOpen, id=MainId.ID_OPEN)
        self.Bind (wx.EVT_MENU, self.__onOpenReadOnly, id=MainId.ID_OPEN_READONLY)
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
        self.Bind (wx.EVT_MENU, self.__onMovePageDown, id=MainId.ID_MOVE_PAGE_DOWN)
        self.Bind (wx.EVT_MENU, self.__onSortChildrenAlphabetical, id=MainId.ID_SORT_CHILDREN_ALPHABETICAL)
        self.Bind (wx.EVT_MENU, self.__onSortSiblingAlphabetical, id=MainId.ID_SORT_SIBLINGS_ALPHABETICAL)
        self.Bind (wx.EVT_MENU, self.__onRename, id=MainId.ID_RENAME)
        self.Bind (wx.EVT_MENU, self.__onRemovePage, id=MainId.ID_REMOVE_PAGE)
        self.Bind (wx.EVT_MENU, self.__onEditPage, id=MainId.ID_EDIT)
        self.Bind (wx.EVT_MENU, self.__onGlobalSearch, id=MainId.ID_GLOBAL_SEARCH)
        self.Bind (wx.EVT_MENU, self.__onAttach, id=MainId.ID_ATTACH)
        self.Bind (wx.EVT_MENU, self.__onCopyTitle, id=MainId.ID_COPY_TITLE)
        self.Bind (wx.EVT_MENU, self.__onCopyPath, id=MainId.ID_COPYPATH)
        self.Bind (wx.EVT_MENU, self.__onCopyAttaches, id=MainId.ID_COPY_ATTACH_PATH)
        self.Bind (wx.EVT_MENU, self.__onCopyLink, id=MainId.ID_COPY_LINK)
        self.Bind (wx.EVT_MENU, self.__onReload, id=MainId.ID_RELOAD)
        self.Bind (wx.EVT_MENU, self.__onFullscreen, self.mainMenu.viewFullscreen)
        self.Bind (wx.EVT_MENU, self.__onHelp, id=MainId.ID_HELP)
        self.Bind (wx.EVT_MENU, self.__onAbout, id=MainId.ID_ABOUT)
        self.Bind (wx.EVT_TOOL, self.__onNew, id=MainId.ID_NEW)
        self.Bind (wx.EVT_TOOL, self.__onOpen, id=MainId.ID_OPEN)
        self.Bind (wx.EVT_TOOL, self.__onReload, id=MainId.ID_RELOAD)
        self.Bind (wx.EVT_TOOL, self.__onAttach, id=MainId.ID_ATTACH)
        self.Bind (wx.EVT_TOOL, self.__onGlobalSearch, id=MainId.ID_GLOBAL_SEARCH)
        self.Bind (wx.EVT_TOOL, self.__onAddTagsToBranch, id=MainId.ID_ADD_TAGS_TO_BRANCH)
        self.Bind (wx.EVT_TOOL, self.__onRemoveTagsFromBranch, id=MainId.ID_REMOVE_TAGS_FROM_BRANCH)
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
            outwiker.core.commands.MessageBox (_(u"Can't save config\n%s") % (unicode (e)),
                    _(u"Error"), wx.ICON_ERROR | wx.OK)
    

    def __setIcon (self):
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(os.path.join (outwiker.core.system.getImagesDir(), "outwiker.ico"), 
            wx.BITMAP_TYPE_ANY))

        self.SetIcon(icon)


    def Destroy(self):
        """
        Убрать за собой
        """
        self.__saveParams()

        self.toolbars.destroyAllToolBars()

        self.auiManager.UnInit()

        self.pagePanel.close()
        self.__panesController.closePanes()

        self.statusbar.Close()
        self.taskBarIcon.Destroy()
        self.controller.destroy()

        super (MainWindow, self).Destroy()
    

    def __onNew(self, event): 
        outwiker.core.commands.createNewWiki(self)


    def __onOpen(self, event):
        outwiker.core.commands.openWikiWithDialog (self)
    

    def __onSave(self, event):
        Application.onForceSave()


    def __onReload(self, event):
        outwiker.core.commands.reloadWiki (self)
    

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
        if Application.selectedPage != None:
            outwiker.core.commands.attachFilesWithDialog (self, Application.wikiroot.selectedPage)

    def __onAbout(self, event):
        outwiker.core.commands.showAboutDialog (self)


    def __onCopyPath(self, event):
        if Application.selectedPage != None:
            outwiker.core.commands.copyPathToClipboard (Application.wikiroot.selectedPage)


    def __onCopyAttaches(self, event):
        if Application.selectedPage != None:
            outwiker.core.commands.copyAttachPathToClipboard (Application.wikiroot.selectedPage)

    
    def __onCopyLink(self, event):
        if Application.selectedPage != None:
            outwiker.core.commands.copyLinkToClipboard (Application.wikiroot.selectedPage)

    
    def __onCopyTitle(self, event):
        if Application.selectedPage != None:
            outwiker.core.commands.copyTitleToClipboard (Application.wikiroot.selectedPage)
    

    def __onEditPage(self, event):
        if Application.selectedPage != None:
            editPage (self, Application.selectedPage)


    def __onRemovePage(self, event):
        if Application.selectedPage != None:
            outwiker.core.commands.removePage (Application.wikiroot.selectedPage)


    @outwiker.core.commands.testreadonly
    def __onGlobalSearch(self, event):
        if Application.wikiroot != None:
            try:
                outwiker.pages.search.searchpage.GlobalSearch.create (Application.wikiroot)
            except IOError:
                outwiker.core.commands.MessageBox (_(u"Can't create page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


    def __onStdEvent(self, event):
        if not self.__stdEventLoop:
            self.__stdEventLoop = True
            target = wx.Window.FindFocus()

            if target != None:
                target.ProcessEvent (event)
        self.__stdEventLoop = False


    def __onRename(self, event):
        self.treePanel.beginRename()


    def __onHelp(self, event):
        outwiker.core.commands.openHelp()


    def __onOpenReadOnly(self, event):
        outwiker.core.commands.openWikiWithDialog (self, readonly=True)


    def __onPreferences(self, event):
        dlg = PrefDialog (self)
        dlg.ShowModal()
        dlg.Destroy()
    

    def __onFullscreen(self, event):
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
        self.__panesController.savePanesParams()
        self.ShowFullScreen(True, wx.FULLSCREEN_NOTOOLBAR | wx.FULLSCREEN_NOBORDER | wx.FULLSCREEN_NOCAPTION)

        self.__panesController.hidePanes()
        self.__panesController.updateViewMenu()


    def __fromFullscreen (self):
        self.controller.loadMainWindowParams()
        self.ShowFullScreen(False)

        self.__panesController.showPanes()
        self.__panesController.loadPanesSize ()
        self.__panesController.updateViewMenu()

    
    def __onMovePageUp(self, event):
        outwiker.core.commands.moveCurrentPageUp()


    def __onMovePageDown(self, event):
        outwiker.core.commands.moveCurrentPageDown()
        

    def __onSortChildrenAlphabetical(self, event):
        outwiker.core.commands.sortChildrenAlphabeticalGUI()


    def __onSortSiblingAlphabetical(self, event):
        outwiker.core.commands.sortSiblingsAlphabeticalGUI()


    def __onPrint(self, event):
        self.pagePanel.panel.Print()


    def __onAddTagsToBranch (self, event):
        if Application.wikiroot == None:
            return

        if Application.selectedPage == None:
            outwiker.core.commands.addTagsToBranchGui (Application.wikiroot, self)
        else:
            outwiker.core.commands.addTagsToBranchGui (Application.selectedPage, self)


    def __onRemoveTagsFromBranch (self, event):
        if Application.wikiroot == None:
            return

        if Application.selectedPage == None:
            outwiker.core.commands.removeTagsFromBranchGui (Application.wikiroot, self)
        else:
            outwiker.core.commands.removeTagsFromBranchGui (Application.selectedPage, self)


    def __onRenameTag (self, event):
        if Application.wikiroot != None:
            outwiker.core.commands.renameTagGui (Application.wikiroot, self)
            


# end of class MainWindow


class DropFilesTarget (wx.FileDropTarget):
    def __init__ (self, mainWindow):
        wx.FileDropTarget.__init__ (self)
        self._mainWindow = mainWindow
        self._mainWindow.SetDropTarget (self)
    
    
    def OnDropFiles (self, x, y, files):
        if (Application.wikiroot != None and
                Application.wikiroot.selectedPage != None):
            outwiker.core.commands.attachFiles (self._mainWindow, 
                        Application.wikiroot.selectedPage, 
                        files)
            return True
