# -*- coding: UTF-8 -*-


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
        pass


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        pass
