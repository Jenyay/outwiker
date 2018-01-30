# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


class PluginName(Plugin):
    def __init__(self, application):
        """
        application - Instance of the
            core.application.ApplicationParams class
        """
        super(PluginName, self).__init__(application)
        self.__controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return u"PluginName"

    @property
    def description(self):
        return _(u"Plugin description")

    @property
    def url(self):
        return _(u"http://jenyay.net")

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
