# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

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
        return u"HtmlHeads"

    @property
    def description(self):
        description = _(u'''Plugin adds wiki-commands (:title:), (:description:), (:keywords:) and (:htmlhead:)''')

        usage = _(u'''<b>Usage:</b>
(:title Page title:)

(:description Page description:)

(:keywords keyword_1, keyword_2, other keyword:)

(:htmlhead:)
&lt;meta http-equiv='Content-Type' content='text/html; charset=utf-8' /&gt;

&lt;meta name='robots' content='index,follow' /&gt;
(:htmlheadend:)
''')

        return u"""{description}

{usage}
""".format(description=description, usage=usage)

    @property
    def url(self):
        return _(u"https://jenyay.net/Outwiker/HtmlHeadsEn")

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
