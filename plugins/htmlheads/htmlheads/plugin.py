# -*- coding: utf-8 -*-

from outwiker.api.core.plugins import Plugin

from .i18n import set_
from .controller import Controller


class PluginHtmlHeads(Plugin):
    """
    This is a main class for HtmlHeads plugin
    """

    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__(self, application)
        self.__controller = Controller(self, application)

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "HtmlHeads"

    @property
    def description(self):
        description = _(
            """Plugin adds wiki-commands (:title:), (:description:), (:keywords:) and (:htmlhead:)"""
        )

        usage = _(
            """<b>Usage:</b>
(:title Page title:)

(:description Page description:)

(:keywords keyword_1, keyword_2, other keyword:)

(:htmlhead:)
&lt;meta http-equiv='Content-Type' content='text/html; charset=utf-8' /&gt;

&lt;meta name='robots' content='index,follow' /&gt;
(:htmlheadend:)
"""
        )

        return """{description}

{usage}
""".format(
            description=description, usage=usage
        )

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/HtmlHeadsEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()
