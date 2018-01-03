# -*- coding: utf-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin


def _no_translate(text):
    return text


class PluginSnippets (Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super(PluginSnippets, self).__init__(application)
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
        self._initlocale(u'snippets')
        from .controller import Controller

        self.__controller = Controller(self, self._application)
        self.__controller.initialize()

    def destroy(self):
        self.__controller.destroy()

    #############################################

    def _initlocale(self, domain):
        from .i18n import set_
        langdir = os.path.join(os.path.dirname(__file__), "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException:
            _ = _no_translate

        set_(_)

    def _correctSysPath(self):
        libspath = os.path.join(self._pluginPath, u'libs')
        if libspath not in sys.path:
            sys.path.insert(0, libspath)
