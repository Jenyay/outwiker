# -*- coding: utf-8 -*-


class ToolBarInfo (object):
    def __init__ (self, toolbar, menuitem):
        """
        toolbar - экземпляр класса панели инструментов (производный от basetoolbar)
        menuitem - экземпляр класса wx.MenuItem, представляющий элемент меню, соответствующий данной панели инструментов
        """
        self.toolbar = toolbar
        self.menuitem = menuitem
