# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet


def _no_translate(text):
    return text


if getCurrentVersion() < Version(2, 1, 0, 833, status=StatusSet.DEV):
    print(u"HackPage plugin. OutWiker version requirement: 2.1.0.833")
else:
    class PluginHackPage(Plugin):
        def __init__(self, application):
            super(PluginHackPage, self).__init__(application)

        @property
        def application(self):
            return self._application

        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name(self):
            return u"HackPage"

        @property
        def description(self):
            return _(u"The HackPage plugin allow to edit hidden page properties")

        @property
        def url(self):
            return _(u"http://jenyay.net/Outwiker/HackPageEn")

        def initialize(self):
            from hackpage.guicontroller import GuiController
            self._initlocale(u"hackpage")
            self.__controller = GuiController(self, self._application)
            self.__controller.initialize()

        def destroy(self):
            self.__controller.destroy()

        #############################################

        def _initlocale(self, domain):
            from .i18n import set_
            langdir = str(os.path.join(os.path.dirname(__file__), "locale"))
            global _

            try:
                _ = self._init_i18n(domain, langdir)
            except BaseException:
                _ = _no_translate

            set_(_)
