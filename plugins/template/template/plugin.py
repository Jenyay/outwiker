# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .controller import Controller
from .i18n import set_


class PluginName(Plugin):
    def __init__(self, application):
        """
        application - Instance of the
            core.application.ApplicationParams class
        """
        super().__init__(application)
        self.__controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return "PluginName"

    @property
    def description(self):
        return _("Plugin description")

    @property
    def url(self):
        return _("https://jenyay.net")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Destroy (unload) the plugin.
        The plugin must unbind all events.
        """
        self.__controller.destroy()
