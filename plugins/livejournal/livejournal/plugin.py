# -*- coding: utf-8 -*-

import os.path

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
        self._initlocale("livejournal")
        self._controller.initialize()

    def _initlocale(self, domain):
        """
        Загрузить перевод
        """
        langdir = os.path.join(os.path.dirname(__file__), "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException as e:
            print(e)

        set_(_)

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
