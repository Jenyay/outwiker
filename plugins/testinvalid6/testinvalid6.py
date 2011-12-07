#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin


class PluginTestInvalid6 (Plugin):
    """
    Плагин с ошибкой - нет метода destroy
    """
    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__ (self, application)


    #############################################
    # Свойства, которые необходимо определить
    #############################################

    @property
    def name (self):
        return u"TestEmpty1"


    def initialize(self):
        pass

    
    @property
    def description (self):
        return _(u"This plugin is empty")


    @property
    def version (self):
        return u"0.1"

    #############################################
