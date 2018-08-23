# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


class PluginReadingMode(Plugin):
    """
    ReadingMode Plugin
    """
    def __init__(self, application):
        super().__init__(application)
        self._controller = Controller(application)

    @property
    def name(self):
        return u"ReadingMode"

    @property
    def description(self):
        return _(u'''Plugin disables the panel "Tree", "Tag", "Attach Files" without changing the geometry of the main window.''')

    @property
    def url(self):
        return _(u"https://jenyay.net/Outwiker/ReadingModeEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    def destroy(self):
        self._controller.destroy()
