# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from .i18n import get_


class TexEquationAction (BaseAction):
    def __init__ (self, application):
        self._application = application

        global _
        _ = get_()

    stringId = u"TexEquation_Action"


    @property
    def title (self):
        return _(u"Equation")


    @property
    def description (self):
        return _(u"Insert equation")


    def run (self, params):
        print "Run!"
