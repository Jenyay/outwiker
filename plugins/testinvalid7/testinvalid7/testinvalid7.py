#!/usr/bin/env python
# -*- coding: UTF-8 -*-


class PluginInvalid7 (object):
    """
    Плагин с ошибкой, потому что не производный от Plugin
    """

    def __init__ (self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """


    @property
    def application (self):
        return self._application


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


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        pass

    #############################################
