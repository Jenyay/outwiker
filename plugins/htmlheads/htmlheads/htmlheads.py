# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


if getCurrentVersion() < Version (1, 8, 0, 729, status=StatusSet.DEV):
    print ("HtmlHeads plugin. OutWiker version requirement: 1.8.0.729")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginTestWikiCommand (Plugin):
        """
        Плагин, добавляющий обработку команды TestCommand в википарсер
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
            return u"HtmlHeads"


        @property
        def description (self):
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
""".format (description=description, usage=usage)


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/HtmlHeadsEn")


        @property
        def version (self):
            return u"1.0.1"


        def initialize(self):
            if self._application.mainWindow is not None:
                self._initlocale(u"htmlheads")

            self.__controller.initialize()


        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e

            set_(_)


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################
