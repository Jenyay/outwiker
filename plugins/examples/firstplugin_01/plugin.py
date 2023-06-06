# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin


class PluginFirst(Plugin):
    def __init__(self, application):
        super().__init__(application)

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return "FirstPlugin"

    @property
    def description(self):
        return _("My first plugin")

    def initialize(self):
        pass

    def destroy(self):
        pass
