#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ToolsInfo (object):
    """
    Класс, описываемый инструмент, добавляемый на панель и/или в главное меню
    """
    def __init__ (self, id, alwaysEnabled, menu, panelname):
        """
        id - идентификатор
        alwaysEnabled - кнопка всегда активна?
        menu - меню, куда добавляем новый пункт
        panelname - имя панели, куда добавляется кнопка
        """
        self.id = id
        self.alwaysEnabled = alwaysEnabled
        self.menu = menu
        self.panelname = panelname
