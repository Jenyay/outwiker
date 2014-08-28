# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiNonParsedAction (BaseAction):
    """
    Текст, который не должен парситься википарсером
    """
    stringId = u"WikiNonParsed"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Non-parsed [=…=]")


    @property
    def description (self):
        return _(u"Non parsed text")


    def run (self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u"[=", u"=]")
