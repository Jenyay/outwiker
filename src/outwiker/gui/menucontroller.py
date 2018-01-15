# -*- coding: utf-8 -*-

import wx

ROOT_MENU_ID = '__root__'


class MenuInfo(object):
    def __init__(self, menu_id, menu, parent=None, menuitem=None):
        '''
        menu_id -- unique menu identifier.
        menu -- wx.Menu instance
        parent -- MenuInfo instance or None
        menuitem -- instance of the wx.MenuItem
        '''
        self.menu_id = menu_id
        self.menu = menu
        self.parent = parent
        self.menuitem = menuitem
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

        self._menu[menu_id] = MenuInfo(menu_id, menu)

    def getRootMenu(self):
        return self._menu[ROOT_MENU_ID].menu

    def removeMenu(self, menu_id):
        if menu_id is ROOT_MENU_ID:
            raise KeyError()

        menu_info = self._menu[menu_id]
        if menu_info.menuitem is not None:
            self._destroyMenu(menu_info)

        # Find menu IDs and all children
        items_to_remove = [menu_info]
        self._add_children_to_list(items_to_remove, menu_info)

        for menu in items_to_remove:
            del self._menu[menu.menu_id]

    def _add_children_to_list(self, menu_id_list, menu_info):
        menu_id_list.extend(menu_info.children)
        for submenu in menu_info.children:
            self._add_children_to_list(menu_id_list, submenu)

    def createSubMenu(self, menu_id, title, parent_id=ROOT_MENU_ID):
        if menu_id in self._menu:
            raise KeyError()

        menu = wx.Menu()
        parent = self._menu[parent_id]
        if isinstance(parent.menu, wx.MenuBar):
            menuitem = parent.menu.Append(menu, title)
        else:
            menuitem = parent.menu.AppendSubMenu(menu, title)

        new_menu_info = MenuInfo(menu_id, menu, parent, menuitem)
        self._menu[menu_id] = new_menu_info
        parent.children.append(new_menu_info)
        return menu

    def _destroyMenu(self, menu_info):
        if isinstance(menu_info.parent.menu, wx.MenuBar):
            self._destroyMenuFromMenuBar(menu_info)
        else:
            assert isinstance(menu_info.parent.menu, wx.Menu)
            menu_info.parent.menu.Remove(menu_info.menuitem)

    def _destroyMenuFromMenuBar(self, menu_info):
        parent_menu = menu_info.parent.menu
        assert isinstance(parent_menu, wx.MenuBar)
        menus = parent_menu.GetMenus()
        for n, (menu, label) in enumerate(menus):
            if menu == menu_info.menu:
                parent_menu.Remove(n)
                break
