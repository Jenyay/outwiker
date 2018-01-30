# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


class PluginStyle(Plugin):
    """
    Плагин, добавляющий обработку команды (:style:) в википарсер
    """
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self._controller = Controller(application)

    @property
    def name(self):
        return u"Style"

    @property
    def description(self):
        return _(u"""Add command (:style:) to wiki parser. This command allow the setting of a user CSS style for a page.

<B>Usage</B>:
(:style:)
styles
(:styleend:)

<B>Example:</B>
(:style:)
body {background-color: #EEE;}
(:styleend:)
""")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/StylePluginEn")

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._controller.destroy()
