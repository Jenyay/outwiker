#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin
from .controller import Controller
from .exporterfactory import ExporterFactory


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
        return u"Export to HTML"

    
    @property
    def description (self):
        return _(u"Export pages to HTML")


    @property
    def version (self):
        return u"0.1"

    
    def initialize(self):
        self.__controller.initialize ()


    def destroy (self):
        """
        Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    #############################################


    @property
    def exporterFactory (self):
        """
        Возвращает класс Exporter, чтобы его можно было легче тестировать при загрузке плагина в реальном времени
        """
        return ExporterFactory
