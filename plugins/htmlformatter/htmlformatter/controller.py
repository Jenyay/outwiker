# -*- coding: utf-8 -*-

from .i18n import get_

from .paragraphimprover import ParagraphHtmlImprover


class Controller:
    """
    Класс отвечает за основную работу интерфейса плагина
    """

    def __init__(self, plugin, application):
        """ """
        self._plugin = plugin
        self._application = application

    def initialize(self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()

        self._application.onPrepareHtmlImprovers += self._onAddHtmlImprover

    def destroy(self):
        """
        Вызывается при отключении плагина
        """
        self._application.onPrepareHtmlImprovers -= self._onAddHtmlImprover

    def _onAddHtmlImprover(self, factory):
        factory.add("pimprover", ParagraphHtmlImprover(), _("Paragraphs (<p>...</p>)"))
