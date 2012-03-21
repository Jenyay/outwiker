#!/usr/bin/python
# -*- coding: UTF-8 -*-

class ToolsInfo (object):
    """
    Класс, описываемый инструмент, добавляемый на панель и/или в главное меню
    """
    def __init__ (self, id, alwaysEnabled, menu):
        """
        id - идентификатор
        alwaysEnabled - кнопка всегда активна?
        menu - меню, куда добавляем новый пункт
        """
        self.id = id
        self.alwaysEnabled = alwaysEnabled
        self.menu = menu
