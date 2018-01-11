# -*- coding: utf-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .guicontroller import GUIController


class PluginLightbox(Plugin):
    """
    Плагин, добавляющий обработку команды (:lightbox:) в википарсер
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
        return u"Lightbox"

    @property
    def description(self):
        return _("""This plugin adds a command (:lightbox:), after adding a images from thumbnails will open in a preview window, rather than in an external program.
                
<B>Usage</B>

(:lightbox:)

bla-bla-bla %thumb%Attach:image_1.jpg%%
bla-bla-bla...
%thumb%Attach:image_2.png%%
""")

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/LightboxEn")

    def initialize(self):
        self._initlocale(u"lightbox")
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

        set_(_)

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._controller.destroy()
        self._GUIController.destroy()
