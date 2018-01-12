# -*- coding: utf-8 -*-


class MenuController(object):
    def __init__(self):
        self._menu = {}

    def __getitem__(self, key):
        return self._menu[key]

    def addMenu(self, key, menu):
        assert key not in self._menu
        self._menu[key] = menu

    def removeMenu(self, key):
        del self._menu[key]
