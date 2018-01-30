# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin

from .i18n import set_


from .controller import Controller


class PluginWebPage (Plugin):
    def __init__(self, application):
        """
        application - instance of the core.application.ApplicationParams
        class
        """
        super(PluginWebPage, self).__init__(application)
        self.__controller = Controller(self, self._application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################
    @property
    def name(self):
        return u"WebPage"

    @property
    def description(self):
        return _(u"Plug-in for downloading HTML pages from web")

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/WebPageEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от
        всех событий
        """
        self.__controller.destroy()

    #############################################

    def _initlocale(self, domain):
        langdir = os.path.join(os.path.dirname(__file__), "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException as e:
            print(e)

        set_(_)
