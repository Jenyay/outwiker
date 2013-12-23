#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiEquationAction (BaseAction):
    """
    Вставка формулы
    """
    stringId = u"WikiEquation"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Equation")


    @property
    def description (self):
        return _(u"Equation")
    

    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (u'{$', u'$}')
