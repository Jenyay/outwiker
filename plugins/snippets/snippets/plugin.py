# -*- coding: utf-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin

from .i18n import set_


class PluginSnippets (Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self._correctSysPath()

        self.__controller = None

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return u"Snippets"

    @property
    def description(self):
        return _(u"Plugin to store text snippets")

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/SnippetsEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        from .controller import Controller

        self.__controller = Controller(self, self._application)
        self.__controller.initialize()

    def destroy(self):
        self.__controller.destroy()

    #############################################

    def _correctSysPath(self):
        libspath = os.path.join(self._pluginPath, u'libs')
        if libspath not in sys.path:
            sys.path.insert(0, libspath)
