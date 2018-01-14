# -*- coding: utf-8 -*-

ROOT_MENU_ID = '__root__'


class MenuInfo(object):
    def __init__(self, menu_id, menu, parent=None):
        '''
        menu_id -- unique menu identifier.
        menu -- wx.Menu instance
        parent -- MenuInfo instance or None
        '''
        self.menu_id = menu_id
        self.menu = menu
        self.parent = parent
        # Submenus
        self.children = []


class MenuController(object):
    def __init__(self, root):
        '''
        root -- instance of the wx.MenuBar or wx.Menu
        '''
        self._menu = {}
        self.addMenu(ROOT_MENU_ID, root)

    def __getitem__(self, menu_id):
        return self._menu[menu_id].menu

    def __contains__(self, menu_id):
        return menu_id in self._menu

    def addMenu(self, menu_id, menu):
        '''
        Add existing menu
        '''
        assert menu is not None
        if menu_id in self._menu:
            raise KeyError()

        self._menu[menu_id] = MenuInfo(menu_id, menu, None)

    def removeMenu(self, key):
        if key is ROOT_MENU_ID:
            raise KeyError()

        keys_to_remove = [key]
        for current_key in keys_to_remove:
            del self._menu[current_key]
