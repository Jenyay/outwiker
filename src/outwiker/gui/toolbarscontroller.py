#!/usr/bin/env python
#-*- coding: utf-8 -*-


class ToolBarsController (object):
    """
    Класс для управления панелями инструментов
    """
    def __init__ (self, parent):
        self._parent = parent
        self._toolbars = {}


    def __getitem__ (self, toolbarname):
        return self._toolbars[toolbarname]


    def __setitem__ (self, toolbarname, toolbar):
        self._toolbars[toolbarname] = toolbar


    def destroyToolBar (self, toolbarname):
        """
        Уничтожить панель инструментов. Нужно вызывать до вызова auiManager.UnInit()
        """
        self._parent.auiManager.DetachPane (self._toolbars[toolbarname])

        self._toolbars[toolbarname].Destroy()
        del self._toolbars[toolbarname]
        self._parent.auiManager.Update()


    def destroyAllToolBars (self):
        """
        Уничтожить все панели инструментов.
        Нужно вызывать до вызова auiManager.UnInit()
        """
        for toolbarname in self._toolbars.keys():
            self.destroyToolBar (toolbarname)


    def __contains__ (self, toolbarname):
        return toolbarname in self._toolbars
