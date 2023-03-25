# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .controller import Controller


class PluginDebugEvents(Plugin):
    def __init__(self, application):
        super().__init__(application)
        self.controller = Controller(application)

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return "DebugEventsPlugin"

    @property
    def description(self):
        return _("Events debug plugin")

    def initialize(self):
        self.controller.initialize()

    def destroy(self):
        self.controller.destroy()
