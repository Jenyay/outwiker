# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


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
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self._controller.destroy()
