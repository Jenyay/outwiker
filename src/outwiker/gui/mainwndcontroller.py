#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import datetime

import wx

from outwiker.core.application import Application
from outwiker.core.commands import setStatusText, getMainWindowTitle
from .bookmarkscontroller import BookmarksController
from .autosavetimer import AutosaveTimer
from .mainid import MainId
from .guiconfig import GeneralGuiConfig, TrayConfig
import outwiker.core.commands

from outwiker.actions.save import SaveAction
from outwiker.actions.close import CloseAction
from outwiker.actions.printaction import PrintAction


class MainWndController (object):
    """
    Контроллер для управления главным окном
    """

    def __init__ (self, parent):
        """
        parent - окно, которым управляет контроллер
        """
        self._mainWindow = parent

        # Идентификаторы пунктов меню и кнопок, которые надо задизаблить, если не открыта вики
        self.disabledTools = [MainId.ID_RELOAD, 
                MainId.ID_ADDPAGE, MainId.ID_ADDCHILD, MainId.ID_ATTACH, 
                MainId.ID_COPYPATH, MainId.ID_COPY_ATTACH_PATH, MainId.ID_COPY_LINK,
                MainId.ID_COPY_TITLE, MainId.ID_BOOKMARKS, MainId.ID_ADDBOOKMARK,
                MainId.ID_EDIT, MainId.ID_REMOVE_PAGE, MainId.ID_GLOBAL_SEARCH,
                MainId.ID_UNDO, MainId.ID_REDO, MainId.ID_CUT, MainId.ID_COPY, MainId.ID_PASTE,
                MainId.ID_SORT_SIBLINGS_ALPHABETICAL, MainId.ID_SORT_CHILDREN_ALPHABETICAL,
                MainId.ID_MOVE_PAGE_UP, MainId.ID_MOVE_PAGE_DOWN, MainId.ID_RENAME]


        # Действия, котоыре надо дизаблить, если не открыто вики
        self._disabledActions = [
                SaveAction,
                CloseAction,
                PrintAction,
                ]

        # Идентификаторы для пунктов меню последних открытых вики
        # Ключ - id, значение - путь до вики
        self._recentId = {}

        self.bookmarks = BookmarksController (self)
        self.__autosaveTimer = AutosaveTimer (Application)

        self.init()
        self.__createAcceleratorTable()


    def __createAcceleratorTable (self):
        """
        Создать горячие клавиши, которые не попали в меню
        """
        aTable = wx.AcceleratorTable([
            (wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
            (wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
            (wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
        self._mainWindow.SetAcceleratorTable(aTable)


    def init (self):
        """
        Начальные установки для главного окна
        """
        self.__bindAppEvents()
        self.mainWindow.Bind (wx.EVT_CLOSE, self.__onClose)


    def __onClose (self, event):
        if TrayConfig (Application.config).minimizeOnClose.value:
            self._mainWindow.Iconize(True)
            event.Veto()
            return

        if (self.__allowExit()):
            self._mainWindow.Destroy()
        else:
            event.Veto()


    def __allowExit (self):
        """
        Возвращает True, если можно закрывать окно
        """
        generalConfig = GeneralGuiConfig (Application.config)
        askBeforeExit = generalConfig.askBeforeExit.value

        return (not askBeforeExit or 
                outwiker.core.commands.MessageBox (_(u"Really exit?"), 
                    _(u"Exit"), 
                    wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES )


    def destroy (self):
        self.__unbindAppEvents()
        self.mainWindow.Unbind (wx.EVT_CLOSE, handler=self.__onClose)


    @property
    def mainWindow (self):
        return self._mainWindow


    @property
    def mainMenu (self):
        return self.mainWindow.mainMenu


    def updatePageDateTime (self):
        statusbar_item = 1
        config = GeneralGuiConfig (Application.config)

        dateFormat = config.dateTimeFormat.value
        text = u""

        if (Application.selectedPage != None and 
            Application.selectedPage.datetime != None):
                text = datetime.datetime.strftime (Application.selectedPage.datetime, dateFormat)

        setStatusText (text, statusbar_item)


    def removeMenuItemsById (self, menu, keys):
        """
        Удалить все элементы меню по идентификаторам
        """
        for key in keys:
            menu.Delete (key)
            self.mainWindow.Unbind (wx.EVT_MENU, id = key)



    def __bindAppEvents (self):
        Application.onPageSelect += self.__onPageSelect
        Application.onPreferencesDialogClose += self.__onPreferencesDialogClose
        Application.onBookmarksChanged += self.__onBookmarksChanged
        Application.onTreeUpdate += self.__onTreeUpdate
        Application.onWikiOpen += self.__onWikiOpen
        Application.onPageUpdate += self.__onPageUpdate


    def __unbindAppEvents (self):
        Application.onPageSelect -= self.__onPageSelect
        Application.onPreferencesDialogClose -= self.__onPreferencesDialogClose
        Application.onBookmarksChanged -= self.__onBookmarksChanged
        Application.onTreeUpdate -= self.__onTreeUpdate
        Application.onWikiOpen -= self.__onWikiOpen
        Application.onPageUpdate -= self.__onPageUpdate


    def __onBookmarksChanged (self, event):
        self.bookmarks.updateBookmarks()


    def __onTreeUpdate (self, sender):
        """
        Событие при обновлении дерева
        """
        self.updateBookmarks()
        self.updateTitle()
        self.updatePageDateTime()


    def __onPageUpdate (self, page):
        self.updatePageDateTime()


    def __onWikiOpen (self, wikiroot):
        """
        Обновить окно после того как загрузили вики
        """
        if wikiroot != None and not wikiroot.readonly:
            try:
                Application.recentWiki.add (wikiroot.path)
                self.updateRecentMenu()
            except IOError as e:
                outwiker.core.commands.MessageBox (
                        _(u"Can't add wiki to recent list.\nCan't save config.\n%s") % (unicode (e)),
                        _(u"Error"), wx.ICON_ERROR | wx.OK)

        self.enableGui()
        self.updateBookmarks()
        self.updateTitle()
        self.updatePageDateTime()


    def updateBookmarks (self):
        self.bookmarks.updateBookmarks()
    

    ###################################################
    # Обработка событий
    #
    def __onPageSelect (self, newpage):
        """
        Обработчик события выбора страницы в дереве
        """
        self.updateTitle()
        self.updatePageDateTime()


    def __onPreferencesDialogClose (self, prefDialog):
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
    def enableGui (self):
        """
        Проверить открыта ли вики и включить или выключить кнопки на панели
        """
        enabled = Application.wikiroot != None

        self.__enableTools (enabled)
        self.mainWindow.pagePanel.panel.Enable(enabled)
        self.mainWindow.treePanel.panel.Enable(enabled)
        self.mainWindow.attachPanel.panel.Enable(enabled)


    def __enableTools (self, enabled):
        for toolId in self.disabledTools:
            if self.mainWindow.mainToolbar.FindById (toolId) != None:
                self.mainWindow.mainToolbar.EnableTool (toolId, enabled)

            if self.mainMenu.FindItemById (toolId) != None:
                self.mainMenu.Enable (toolId, enabled)

        map (lambda action: Application.actionController.enableTools (action.stringId, enabled),
                self._disabledActions)

    #
    ###################################################


    def updateTitle (self):
        """
        Обновить заголовок главного окна в зависимости от шаблона и текущей страницы
        """
        self.mainWindow.SetTitle (getMainWindowTitle (Application))


    def loadMainWindowParams(self):
        """
        Загрузить параметры из конфига
        """
        self.mainWindow.Freeze()

        width = self.mainWindow.mainWindowConfig.width.value
        height = self.mainWindow.mainWindowConfig.height.value

        xpos = self.mainWindow.mainWindowConfig.xPos.value
        ypos = self.mainWindow.mainWindowConfig.yPos.value
        
        self.mainWindow.SetDimensions (xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

        self.mainWindow.Layout()
        self.mainWindow.Thaw()


    ###################################################
    # Список последних открытых вики
    #
    def updateRecentMenu (self):
        """
        Обновление меню со списком последних открытых вики
        """
        self.removeMenuItemsById (self.mainMenu.fileMenu, self._recentId.keys())
        self._recentId = {}

        for n in range (len (Application.recentWiki)):
            id = wx.NewId()
            path = Application.recentWiki[n]
            self._recentId[id] = path

            title = path if n + 1 > 9 else u"&{n}. {path}".format (n=n+1, path=path)

            self.mainMenu.fileMenu.Append (id, title, "", wx.ITEM_NORMAL)
            
            self.mainWindow.Bind(wx.EVT_MENU, self.__onRecent, id=id)
    

    def __onRecent (self, event):
        """
        Выбор пункта меню с недавно открытыми файлами
        """
        outwiker.core.commands.openWiki (self._recentId[event.Id])

    #
    ###################################################
