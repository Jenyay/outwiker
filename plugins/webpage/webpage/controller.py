# -*- coding: UTF-8 -*-

from outwiker.core.factoryselector import FactorySelector

from .webnotepage import WebPageFactory


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        FactorySelector.addFactory (WebPageFactory())


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        FactorySelector.removeFactory (WebPageFactory().getTypeString())
