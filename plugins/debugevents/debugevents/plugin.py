# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller


class PluginDebugEvents(Plugin):
    def __init__(self, application):
        super(PluginDebugEvents, self).__init__(application)
        self.controller = Controller(application)

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return u"DebugEventsPlugin"

    @property
    def description(self):
        return _(u"Events debug plugin")

    def initialize(self):
        self.controller.initialize()

    def destroy(self):
        self.controller.destroy()
