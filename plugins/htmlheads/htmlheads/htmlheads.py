# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS

from .i18n import set_
from .controller import Controller


if getCurrentVersion() < Version (1, 8, 0, 729, status=StatusSet.DEV):
    print ("HrmlHeads plugin. OutWiker version requirement: 1.8.0.729")
else:
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
            description = _(u'''Plugin adds wiki-commands (:title:), (:description:) and (:keywords:)''')

            usage = _(u'''<b>Usage:</b>
''')

            return u"""{description}

{usage}
""".format (description=description, usage=usage)


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/HtmlHeadsEn")


        @property
        def version (self):
            return u"1.0"


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
