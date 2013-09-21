#!/usr/bin/python
# -*- coding: UTF-8 -*-


from outwiker.gui.baseaction import BaseAction

class DebugAction (BaseAction):
    """
    Класс действия, предназначенный для отладки действий с помощью плагина TestDebug
    """
    def __init__ (self, application):
        super (DebugAction, self).__init__()
        self._application = application

    @property
    def title (self):
        return u"DebugAction"


    @property
    def description (self):
        return u"DebugAction"
    

    @property
    def strid (self):
        return u"plugin_debug_action"


    def run (self, params):
        self._application.mainWindow.updateViewMenu()
        print u"DebugAction.run({0})".format (params)
