#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class TitleAction (BaseAction):
    """
    Вставить команду (:title:)
    """
    stringId = u"HtmlHeads_InsertTitle"

    def __init__ (self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()


    @property
    def title (self):
        return _(u"Title (:title ...:)")


    @property
    def description (self):
        return _(u"HtmlHeads plugin. Insert (:title... :) command")


    def run (self, params):
        self._getPageView().codeEditor.turnText (u"(:title ", u":)")


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView
