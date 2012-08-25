#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Плагин для открытия файлов заметок с помощью внешних программ
"""

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS

from .controller import Controller
from .i18n import set_


class PluginExternalTools (Plugin):
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)
        self.__controller = Controller (self)


    @property
    def application (self):
        return self._application


    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name (self):
        return u"ExternalTools"

    
    @property
    def description (self):
        return _(u"Open notes files with external editor")


    @property
    def version (self):
        return u"1.2"


    def initialize(self):
        self.__initlocale()
        self.__controller.initialize ()


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    #############################################

    def __initlocale (self):
        domain = u"externaltools"

        langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)

        try:
            global _
            _ = self._init_i18n (domain, langdir)

            set_(_)
        except BaseException as e:
            pass
