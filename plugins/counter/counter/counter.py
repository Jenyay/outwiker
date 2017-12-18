# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

__version__ = u"2.0.1"


if getCurrentVersion() < Version(2, 1, 0, 833, status=StatusSet.DEV):
    print ("Counter plugin. OutWiker version requirement: 2.1.0.833")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginCounter (Plugin):
        """
        Плагин, добавляющий обработку команды (:counter:) в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.__controller = Controller(self, application)


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"Counter"


        @property
        def description (self):
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
""".format (description=description, usage=usage, params=params)


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/CounterEn")


        @property
        def version (self):
            return __version__


        def initialize(self):
            if self._application.mainWindow is not None:
                self._initlocale(u"counter")

            self.__controller.initialize()


        def _initlocale (self, domain):
            langdir = os.path.join (os.path.dirname (__file__), "locale")
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print (e)

            set_(_)


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################
