#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin


class PluginTestInvalid3 (Plugin):
    """
    Плагин с ошибкой - нет свойства version
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
        return u"TestInvalid3"


    def initialize(self):
        pass

    
    @property
    def description (self):
        return _(u"This plugin is empty")


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        pass

    #############################################
