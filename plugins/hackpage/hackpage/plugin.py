# -*- coding: utf-8 -*-


from outwiker.api.core.plugins import Plugin

from .guicontroller import GuiController
from .i18n import set_


class PluginHackPage(Plugin):
    def __init__(self, application):
        super().__init__(application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "HackPage"

    @property
    def description(self):
        return _("The HackPage plugin allow to edit hidden page properties")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/HackPageEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller = GuiController(self, self._application)
        self.__controller.initialize()

    def destroy(self):
        self.__controller.destroy()
