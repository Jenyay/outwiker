#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction


class FullScreenAction (BaseAction):
    """
    Переход в полноэкранный режим и обратно
    """
    stringId = u"Fullscreen"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Fullscreen")


    @property
    def description (self):
        return _(u"Fullscreen mode on/off")
    

    def run (self, params):
        self._application.mainWindow.setFullscreen (params)
