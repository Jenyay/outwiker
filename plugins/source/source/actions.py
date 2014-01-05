#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class InsertSourceAction (BaseAction):
    """
    Вызвать диалог для вставки команды (:source:)
    """
    stringId = u"Source_InsertSource"

    def __init__ (self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()


    @property
    def title (self):
        return _(u"Source Code (:source ...:)")


    @property
    def description (self):
        return _(u"Source plugin. Insert (: source... :) command for source code highlighting")
    

    def run (self, params):
        self._controller.insertCommand()
