# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .guicontroller import GUIController


def _no_translate(text):
    return text


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
        self._GUIController = GUIController(application)

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
        self._initlocale(u"style")
        self._controller.initialize()
        self._GUIController.initialize()

    def _initlocale(self, domain):
        from .i18n import set_
        langdir = os.path.join(os.path.dirname(__file__), "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException as e:
            print(e)
            _ = _no_translate

        set_(_)

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/StylePluginEn")

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._controller.destroy()
        self._GUIController.destroy()
