#!/usr/bin/python
# -*- coding: UTF-8 -*-

from baseaction import BaseAction


class PolyAction (BaseAction):
    """
    Класс для полиморфного действия, поведение которого можно менять во время работы
    """
    def __init__ (self, 
            application,
            strid,
            title,
            description):
        self._application = application
        self._strid = strid
        self._title = title
        self._description = description

        # Функция, которая будет вызываться из метода run(), если _func != None
        self._func = None


    @property
    def title (self):
        return self._title


    @property
    def description (self):
        return self._description

    @property
    def strid (self):
        return self._strid


    def run (self, params):
        if self._func != None:
            self._func (params)


    def setFunc (self, func):
        self._func = func
