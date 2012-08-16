#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os.path

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.event import Event
from outwiker.gui.toolsinfo import ToolsInfo
from outwiker.core.application import Application


class BasePagePanel (wx.Panel):
    """
    Базовый класс для панелей представления страниц
    """
    __metaclass__ = ABCMeta

    def __init__ (self, parent, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, parent, *args, **kwds)

        self._currentpage = None
        self.mainWindow = Application.mainWindow

        # Событие, срабатывающее, когда устанавливается новая страница
        # Параметр: новая страница
        self._onSetPage = Event ()

        # Словарь, хранящий информацию о созданных инструментах 
        # Ключ - строка, описывающая инструмент
        # Значение - экземпляр класса ToolsInfo
        self._tools = {}


    @property
    def allTools (self):
        return self._tools.values()


    def _removeAllTools (self):
        self.mainWindow.Freeze()

        for toolKey in self._tools.keys():
            self.removeTool (toolKey, fullUpdate=False)

        self.mainWindow.UpdateAuiManager()
        self.mainWindow.Thaw()


    def removeTool (self, idstring, fullUpdate=True):
        tool = self._tools[idstring]

        if (tool.panelname in self.mainWindow.toolbars and
            self.mainWindow.toolbars[tool.panelname].FindById (tool.id) != None):
                self.mainWindow.toolbars[tool.panelname].DeleteTool (tool.id, fullUpdate=fullUpdate)

        tool.menu.Remove (tool.id)
        
        self.mainWindow.Unbind(wx.EVT_MENU, id=tool.id)

        del self._tools[idstring]


    def addTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled=False,
            fullUpdate=True,
            panelname="plugins"):
        """
        Добавить пункт меню и кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        fullUpdate - нужно ли полностью обновлять окно после добавления кнопки
        panelname - имя панели, куда добавляется кнопка
        """
        assert idstring not in self._tools

        id = wx.NewId()
        tool = ToolsInfo (id, alwaysEnabled, menu, panelname)
        self._tools[idstring] = tool

        menu.Append (id, menuText, "", wx.ITEM_NORMAL)
        self.mainWindow.Bind(wx.EVT_MENU, func, id = id)

        if image != None and len (image) != 0:
            self.mainWindow.toolbars[tool.panelname].AddTool(id, 
                    buttonText, 
                    wx.Bitmap(image, wx.BITMAP_TYPE_ANY), 
                    buttonText,
                    fullUpdate=fullUpdate)

            self.mainWindow.toolbars[tool.panelname].UpdateToolBar()


    def enableTool (self, tool, enabled):
        """
        Активировать или дезактивировать один инструмент (пункт меню и кнопку)
        tool - экземпляр класса ToolsInfo
        """
        tool.menu.Enable (tool.id, enabled)

        if self.mainWindow.toolbars[tool.panelname].FindById (tool.id) != None:
            self.mainWindow.toolbars[tool.panelname].EnableTool (tool.id, enabled)
            self.mainWindow.toolbars[tool.panelname].Realize()


    def addCheckTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled = False,
            fullUpdate=True,
            panelname="plugins"):
        """
        Добавить пункт меню с галкой и залипающую кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        fullUpdate - нужно ли полностью обновлять окно после добавления кнопки
        panelname - имя панели, куда добавляется кнопка
        """
        assert idstring not in self._tools

        id = wx.NewId()
        tool = ToolsInfo (id, alwaysEnabled, menu, panelname)
        self._tools[idstring] = tool

        menu.AppendCheckItem (id, menuText, "")
        self.mainWindow.Bind(wx.EVT_MENU, func, id = id)

        if image != None and len (image) != 0:
            self.mainWindow.toolbars[tool.panelname].AddTool(id, 
                    buttonText,
                    wx.Bitmap(image, wx.BITMAP_TYPE_ANY), 
                    buttonText,
                    wx.ITEM_CHECK,
                    fullUpdate=fullUpdate)


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

        self.mainWindow.toolbars[tools.panelname].ToggleTool (tools.id, checked)


    ###############################################
    # Методы, которые обязательно надо перегрузить
    ###############################################

    @abstractmethod
    def Print (self):
        """
        Вызов печати страницы
        """
        pass


    @abstractmethod
    def UpdateView (self, page):
        """
        Обновление страницы
        """
        pass


    @abstractmethod
    def Save (self):
        """
        Сохранить страницу
        """
        pass


    @abstractmethod
    def Clear (self):
        """
        Убрать за собой. Удалить добавленные элементы интерфейса и отписаться от событий
        """
        pass


    #############################################################################################
    # Методы, которые в базовом классе ничего не делают, но которые может понадобиться перегрузить
    #############################################################################################

    def onAttachmentPaste (self, fnames):
        """
        Пользователь хочет вставить ссылки на приаттаченные файлы
        """
        pass


    def removeGui (self):
        """
        Убрать за собой элементы управления
        """
        pass

    ###################################################

    @property
    def page (self):
        return self._currentpage


    @page.setter
    def page (self, page):
        self.Save()
        self._currentpage = page

        if not os.path.exists (page.path):
            return

        self._onSetPage (page)
        self.UpdateView (page)


    def Close (self):
        """
        Закрытие панели. 
        Вызывать вручную!!!
        """
        self.mainWindow.toolbars.updatePanesInfo()
        self.Save()
        self.CloseWithoutSave()
    

    def CloseWithoutSave (self):
        """
        Закрытие панели без сохранения. 
        """
        self.Clear()
        wx.Panel.Close (self)
        self.Destroy()
