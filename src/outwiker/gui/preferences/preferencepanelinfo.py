# -*- coding: UTF-8 -*-
"""
Модуль с классом, описывающим панели с настройками
"""


class PreferencePanelInfo (object):
    def __init__ (self, panel, name):
        self.__panel = panel
        self.__name = name


    @property
    def panel (self):
        return self.__panel


    @property
    def name (self):
        return self.__name
