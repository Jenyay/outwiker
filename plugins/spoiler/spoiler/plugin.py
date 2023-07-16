# -*- coding: utf-8 -*-

# Плагин для вставки свернутого текста

from outwiker.api.core.plugins import Plugin

from .controller import Controller
from .i18n import set_


class PluginSpoiler(Plugin):
    """
    Плагин, добавляющий обработку команды spoiler в википарсер
    """

    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self._controller = Controller(self, application)

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    @property
    def name(self):
        return "Spoiler"

    @property
    def description(self):
        return _(
            """Add (:spoiler:) wiki command to parser.

<B>Usage:</B>
<PRE>(:spoiler:)
Text
(:spoilerend:)</PRE>

For nested spoilers use (:spoiler0:), (:spoiler1:)...(:spoiler9:) commands. 

<U>Example:</U>

<PRE>(:spoiler:)
Text
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Nested spoiler
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Params:</B>
<U>inline</U> - Spoiler will be in inline mode.
<U>expandtext</U> - Link text for the collapsed spoiler. Default: "Expand".
<U>collapsetext</U> - Link text for the expanded spoiler. Default: "Collapse".

<U>Example:</U>

<PRE>(:spoiler expandtext="More..." collapsetext="Less" inline :)
Text
(:spoilerend:)</PRE>
"""
        )

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/SpoilerEn")

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий и удалить свои кнопки,
        пункты меню и т.п.
        """
        self._controller.destroy()
