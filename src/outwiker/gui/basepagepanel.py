# -*- coding: utf-8 -*-

import logging
import os.path

import wx

from outwiker.core.event import Event

logger = logging.getLogger('outwiker.gui.pasepagepanel')


class BasePagePanel(wx.Panel):
    """
    Базовый класс для панелей представления страниц
    """
    def __init__(self, parent, application):
        super().__init__(parent, style=wx.TAB_TRAVERSAL)

        self._currentpage = None
        self._application = application
        self.mainWindow = self._application.mainWindow

        # Событие, срабатывающее, когда устанавливается новая страница
        # Параметр: новая страница
        self._onSetPage = Event()

        # Словарь, хранящий информацию о созданных инструментах
        # Ключ - строка, описывающая инструмент
        # Значение - экземпляр класса ToolsInfo
        self._tools = {}

    @property
    def allTools(self):
        """
        Возвращает список ToolsInfo.
        """
        return list(self._tools.values())

    def _removeAllTools(self):
        self.mainWindow.Freeze()

        for toolKey in self._tools:
            self.removeTool(toolKey, fullUpdate=False)

        self.mainWindow.UpdateAuiManager()
        self.mainWindow.Thaw()

    def removeTool(self, idstring, fullUpdate=True):
        if idstring not in self._tools:
            logger.error('BasePagePanel.removeTool. Invalid idstring: {}'.format(idstring))
            return

        tool = self._tools[idstring]

        if (tool.panelname in self.mainWindow.toolbars and
                self.mainWindow.toolbars[tool.panelname].FindById(tool.id) is not None):
            self.mainWindow.toolbars[tool.panelname].DeleteTool(tool.id, fullUpdate=fullUpdate)

        tool.menu.Remove(tool.id)

        self.mainWindow.Unbind(wx.EVT_MENU, id=tool.id)

        del self._tools[idstring]

    def enableTool(self, tool, enabled):
        """
        Активировать или дезактивировать один инструмент(пункт меню и кнопку)
        tool - экземпляр класса ToolsInfo
        """
        tool.menu.Enable(tool.id, enabled)

        if self.mainWindow.toolbars[tool.panelname].FindById(tool.id) is not None:
            toolbar = self.mainWindow.toolbars[tool.panelname]
            toolbar.Freeze()
            toolbar.EnableTool(tool.id, enabled)
            toolbar.Realize()
            toolbar.Thaw()

    ###############################################
    # Методы, которые обязательно надо перегрузить
    ###############################################

    def Print(self):
        """
        Вызов печати страницы
        """
        pass

    def UpdateView(self, page):
        """
        Обновление страницы
        """
        pass

    def Save(self):
        """
        Сохранить страницу
        """
        pass

    def Clear(self):
        """
        Убрать за собой.
        Удалить добавленные элементы интерфейса и отписаться от событий
        """
        pass

    @property
    def page(self):
        return self._currentpage

    @page.setter
    def page(self, page):
        self.Save()
        self._currentpage = page

        if not os.path.exists(page.path):
            return

        self._onSetPage(page)
        self.UpdateView(page)

    def Close(self):
        """
        Закрытие панели.
        Вызывать вручную!!!
        """
        self.Save()
        self.CloseWithoutSave()

    def CloseWithoutSave(self):
        """
        Закрытие панели без сохранения.
        """
        self.Clear()
        super(BasePagePanel, self).Close()
        self.Destroy()
