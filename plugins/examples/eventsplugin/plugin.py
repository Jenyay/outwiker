# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller


class PluginExampleEvents(Plugin):
    def __init__(self, application):
        super(PluginExampleEvents, self).__init__(application)
        self.controller = Controller(application)

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return u"ExampleEventsPlugin"

    @property
    def description(self):
        return _(u"Example plugin")

    def initialize(self):
        self.controller.initialize()

    def destroy(self):
        self.controller.destroy()
