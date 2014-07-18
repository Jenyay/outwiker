# -*- coding: UTF-8 -*-

from .i18n import get_
from .guicreator import GuiCreator


class PluginController (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application

        self._guiCreator = None


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._guiCreator = GuiCreator (self, self._application)
        self._guiCreator.initialize()


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._guiCreator.destroy ()
