# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .controller import Controller
from .i18n import set_


class PluginRecentEditedPages(Plugin):
    def __init__(self, application):
        """
        application - Instance of the
            core.application.ApplicationParams class
        """
        super().__init__(application)
        self._controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return "RecentEditedPages"

    @property
    def description(self):
        return _("Marks for recent edited pages")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/RecentEditedPagesEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    def destroy(self):
        """
        Destroy (unload) the plugin.
        The plugin must unbind all events.
        """
        self._controller.destroy()
