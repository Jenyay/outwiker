# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


class PluginLivejournal(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__(self, application)
        self._controller = Controller(self, application)

    def initialize(self):
        """
        Инициализация плагина
        """
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    @property
    def name(self):
        return u"Livejournal"

    @property
    def description(self):
        return _(u"""Add commands (:ljuser:) and (:ljcomm:) in wiki parser.

                 <B>Usage:</B>
                 (:ljuser username:)
                 (:ljcomm communityname:)
                 """)

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/LivejournalPluginEn")

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._controller.destroy()
