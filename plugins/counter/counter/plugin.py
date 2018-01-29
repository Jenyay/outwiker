# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .i18n import set_
from .controller import Controller


class PluginCounter (Plugin):
    """
    Плагин, добавляющий обработку команды (:counter:) в википарсер
    """
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self.__controller = Controller(self, application)

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return u"Counter"

    @property
    def description(self):
        description = _(u'''Plugin adds wiki-command (:counter:), allowing the automatic numbering anything on the page.''')

        usage = _(u'''<b>Usage:</b>:
(:counter parameters... :)''')

        params = _(u'''<b>Parameters:</b>
All parameters are optional.
<ul>
<li><b>name</b> - sets the name of the counter. Counters with different names have independent current values.</li>
<li><b>start</b> - value, with which to start a new count. With this option, you can "reset" the counter to the required value.</li>
<li><b>step</b> - increment for the counter.</li>
<li><b>parent</b> - name of the parent counter to create a numbering like 1.1, 1.2.3, etc.</li>
<li><b>separator</b> - separator between a given counter and the parent counter (the default value - dot).</li>
<li><b>hide</b> - parameter indicates that the counter need to hide, but to increase its value.</li>
</ul>''')

        return u"""{description}

{usage}

{params}
""".format(description=description, usage=usage, params=params)

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/CounterEn")

    def initialize(self):
        set_(self.gettext)
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    #############################################
