#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os

import wx

import outwiker.core.system
from outwiker.core.commands import MessageBox, openWiki, pageExists
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application

from outwiker.gui.buttonsdialog import ButtonsDialog
from outwiker.gui.toolsinfo import ToolsInfo

from .basepagepanel import BasePagePanel


class BaseTextPanel (BasePagePanel):
    """
    Базовый класс для представления текстовых страниц и им подобных (где есть текстовый редактор)
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def GetContentFromGui(self):
        """
        Получить из интерфейса контент, который будет сохранен в файл __page.text
        """
        pass


    @abstractmethod
    def GetSearchPanel (self):
        """
        Вернуть панель поиска
        """
        pass

    
    def __init__ (self, parent, *args, **kwds):
        BasePagePanel.__init__ (self, parent, *args, **kwds)

        self.mainWindow = Application.mainWindow
        self.searchMenu = None

        # Предыдущее сохраненное состояние. 
        # Используется для выявления изменения страницы внешними средствами
        self._oldContent = None

        # Диалог, который показывается, если страница изменена сторонними программами.
        # Используется для проверки того, что диалог уже показан и еще раз его показывать не надо
        self.externalEditDialog = None

        # Словарь, хранящий информацию о созданных инструментах 
        # Ключ - строка, описыывающая инструмент
        # Значение - экземпляр класса ToolsInfo
        self._tools = {}

        self.searchMenuIndex = 2
        self.imagesDir = outwiker.core.system.getImagesDir()

        self._addSearchTools ()

        Application.onAttachmentPaste += self.onAttachmentPaste
        Application.onPreferencesDialogClose += self.onPreferencesDialogClose

        self._onSetPage += self.__onSetPage


    @property
    def allTools (self):
        return self._tools.values()


    def __onSetPage (self, page):
        self.__updateOldContent()


    def __updateOldContent (self):
        self._oldContent = self.page.content


    def onPreferencesDialogClose (self, prefDialog):
        pass
    

    def Save (self):
        """
        Сохранить страницу
        """
        if self.page == None:
            return

        if not pageExists (self.page):
            return

        if not self.page.isRemoved:
            self.checkForExternalEditAndSave()


    def checkForExternalEditAndSave (self):
        """
        Проверить, что страница не изменена внешними средствами
        """
        if self._oldContent != None and self._oldContent != self.page.content:
            # Старое содержимое не совпадает с содержимым страницы.
            # Значит содержимое страницы кто-то изменил
            self.__externalEdit()
        else:
            self._savePageContent(self.page)
            self.__updateOldContent()


    def __externalEdit (self):
        """
        Спросить у пользователя, что делать, если страница изменилась внешними средствами
        """
        if self.externalEditDialog == None:
            result = self.__showExternalEditDialog()

            if result == 0:
                # Перезаписать
                self._savePageContent(self.page)
                self.__updateOldContent()
            elif result == 1:
                # Перезагрузить
                self.__updateOldContent()
                self.UpdateView(self.page)

    
    def __showExternalEditDialog (self):
        """
        Показать диалог о том, что страница изменена сторонними программами и вернуть результат диалога:
        0 - перезаписать
        1 - перезагрузить
        2 - ничего не делать
        """
        buttons = [_(u"Overwrite"), _("Load"), _("Cancel")]

        message = _(u'Page "%s" is changed by the external program') % self.page.title
        self.externalEditDialog = ButtonsDialog (self, 
                message,
                _(u"Owerwrite?"),
                buttons,
                default = 0,
                cancel = 2)
        
        result = self.externalEditDialog.ShowModal()
        self.externalEditDialog.Destroy()
        self.externalEditDialog = None

        return result


    def __stringsAreEqual (self, str1, str2):
        """
        Сравнение двух строк
        """
        return str1.replace ("\r\n", "\n") == str2.replace ("\r\n", "\n")


    def _savePageContent (self, page):
        """
        Сохранение содержимого страницы
        """
        if (page != None and 
                not page.isRemoved and 
                not page.readonly and
                not self.__stringsAreEqual (page.content, self.GetContentFromGui() ) ):

            try:
                page.content = self.GetContentFromGui()
            except IOError as e:
                # TODO: Проверить под Windows
                MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
    

    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += Attachment.attachDir + "/" + fnames[n]
            if n != count -1:
                text += "\n"

        return text

    
    def Clear (self):
        """
        Убрать за собой
        """
        Application.onAttachmentPaste -= self.onAttachmentPaste
        Application.onPreferencesDialogClose -= self.onPreferencesDialogClose
        self._onSetPage -= self.__onSetPage

        self.removeGui()


    def removeGui (self):
        """
        Убрать за собой элементы управления
        """
        assert self.mainWindow != None
        assert self.mainWindow.mainMenu.GetMenuCount() >= 3
        assert self.searchMenu != None

        self._removeAllTools()
        self.mainWindow.mainMenu.Remove (self.searchMenuIndex)
        self.searchMenu = None


    def _removeAllTools (self):
        self.mainWindow.Freeze()

        for toolKey in self._tools.keys():
            self.removeTool (toolKey, fullUpdate=False)

        self.mainWindow.UpdateAuiManager()
        self.mainWindow.Thaw()


    def removeTool (self, idstring, fullUpdate=True):
        tool = self._tools[idstring]

        if self.mainWindow.generalToolbar.FindById (tool.id) != None:
            self.mainWindow.generalToolbar.DeleteTool (tool.id, fullUpdate=fullUpdate)

        tool.menu.Remove (tool.id)
        
        self.mainWindow.Unbind(wx.EVT_MENU, id=tool.id)

        del self._tools[idstring]

    
    def _addSearchTools (self):
        assert self.mainWindow != None
        self.searchMenu = wx.Menu()
        self.mainWindow.mainMenu.Insert (self.searchMenuIndex, self.searchMenu, _("&Search") )

        self.addTool (self.searchMenu,
                u"ID_BASE_SEARCH",
                self.onSearch,
                _(u"Search…\tCtrl+F"),
                _(u"Search"),
                os.path.join (self.imagesDir, "local_search.png"),
                False,
                fullUpdate=False)


        self.addTool (self.searchMenu,
                u"ID_BASE_SEARCH_PREV",
                self.onSearchPrev,
                _(u"Find previous\tShift+F3"),
                "",
                None,
                fullUpdate=False)

        self.addTool (self.searchMenu,
                u"ID_BASE_SEARCH_NEXT",
                self.onSearchNext,
                _(u"Find next\tF3"),
                "",
                None,
                fullUpdate=False)


    def _showSearchPanel (self, panel):
        if not panel.IsShown():
            panel.Show()
            panel.GetParent().Layout()


    def onSearch (self, event):
        panel = self.GetSearchPanel()
        if panel != None:
            self._showSearchPanel (panel)
            panel.startSearch()


    def onSearchNext (self, event):
        panel = self.GetSearchPanel()
        if panel != None:
            self._showSearchPanel (panel)
            panel.nextSearch()


    def onSearchPrev (self, event):
        panel = self.GetSearchPanel()
        if panel != None:
            self._showSearchPanel (panel)
            panel.prevSearch()


    def addTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled=False,
            fullUpdate=True):
        """
        Добавить пункт меню и кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        """
        assert idstring not in self._tools

        id = wx.NewId()
        tool = ToolsInfo (id, alwaysEnabled, menu)
        self._tools[idstring] = tool

        menu.Append (id, menuText, "", wx.ITEM_NORMAL)
        self.mainWindow.Bind(wx.EVT_MENU, func, id = id)

        if image != None and len (image) != 0:
            self.mainWindow.generalToolbar.AddTool(id, 
                    buttonText, 
                    wx.Bitmap(image, wx.BITMAP_TYPE_ANY), 
                    buttonText,
                    fullUpdate=fullUpdate)

            self.mainWindow.generalToolbar.UpdateToolBar()


    def enableTool (self, tool, enabled):
        """
        Активировать или дезактивировать один инструмент (пункт меню и кнопку)
        tool - экземпляр класса ToolsInfo
        """
        tool.menu.Enable (tool.id, enabled)

        if self.mainWindow.generalToolbar.FindById (tool.id) != None:
            self.mainWindow.generalToolbar.EnableTool (tool.id, enabled)
            self.mainWindow.generalToolbar.Realize()


    def addCheckTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled = False,
            fullUpdate=True):
        """
        Добавить пункт меню с галкой и залипающую кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        """
        assert idstring not in self._tools

        id = wx.NewId()
        tool = ToolsInfo (id, alwaysEnabled, menu)
        self._tools[idstring] = tool

        menu.AppendCheckItem (id, menuText, "")
        self.mainWindow.Bind(wx.EVT_MENU, func, id = id)

        if image != None and len (image) != 0:
            self.mainWindow.generalToolbar.AddTool(id, 
                    buttonText,
                    wx.Bitmap(image, wx.BITMAP_TYPE_ANY), 
                    buttonText,
                    wx.ITEM_CHECK,
                    fullUpdate=fullUpdate)

            # self.mainWindow.generalToolbar.Realize()


    def checkTools (self, idstring, checked):
        """
        Активировать/деактивировать залипающие элементы управления
        idstring - строка, описывающая элементы управления
        checked - устанавливаемое состояние
        """
        assert idstring in self._tools
        assert self.mainWindow != None

        tools = self._tools[idstring]

        if tools.menu != None:
            tools.menu.Check (tools.id, checked)

        self.mainWindow.generalToolbar.ToggleTool (tools.id, checked)
