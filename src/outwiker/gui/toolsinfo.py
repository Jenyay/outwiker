# -*- coding: utf-8 -*-


class ToolsInfo (object):
    """
    Класс, описываемый инструмент, добавляемый на панель и/или в главное меню
    """
    def __init__(self, tools_id, alwaysEnabled, menu, panelname):
        """
        tools_id - идентификатор
        alwaysEnabled - кнопка всегда активна?
        menu - меню, куда добавляем новый пункт
        panelname - имя панели, куда добавляется кнопка
        """
        self.id = tools_id
        self.alwaysEnabled = alwaysEnabled
        self.menu = menu
        self.panelname = panelname
