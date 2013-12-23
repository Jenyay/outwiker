#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class WikiAttachListAction (BaseAction):
    """
    Вставка команды для показа списка прикрепленных файлов
    """
    stringId = u"WikiAttachList"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Attachment (:attachlist:)")


    @property
    def description (self):
        return _(u"Insert (:attachlist:) command")
    

    def run (self, params):
        assert self._application.mainWindow != None
        assert self._application.mainWindow.pagePanel != None

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.replaceText (u"(:attachlist:)")
