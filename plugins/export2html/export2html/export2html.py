# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_

__version__ = u"2.0.1"


class PluginExport2Html (Plugin):
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)
        self.__controller = Controller (self, application)


    @property
    def application (self):
        return self._application


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name (self):
        return u"Export2Html"


    @property
    def description (self):
        return _(u"Export pages to HTML")


    @property
    def version (self):
        return __version__

    def initialize(self):
        self.__initlocale()
        self.__controller.initialize ()


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    #############################################


    @property
    def url (self):
        return _(u"http://jenyay.net/Outwiker/Export2HtmlPluginEn")


    def __initlocale (self):
        domain = u"export2html"

        langdir = str(os.path.join (os.path.dirname (__file__), "locale"))

        try:
            global _
            _ = self._init_i18n (domain, langdir)
            set_(_)
        except BaseException as e:
            print (e)
