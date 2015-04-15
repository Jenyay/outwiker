# -*- coding: UTF-8 -*-

"""
Плагин для открытия файлов заметок с помощью внешних программ,
а также для создания ссылок на викистраницах, при клике на которые запускаются
внешние программы.
"""

import os.path

from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version
from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS

__version__ = u"1.3"


if getCurrentVersion() < Version (1, 8, 0):
    print ("ExternalTools plugin. OutWiker version requirement: 1.8.0")
else:
    from controller import Controller
    from i18n import set_

    class PluginExternalTools (Plugin):
        def __init__ (self, application):
            """
            application - instance of core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.__controller = Controller (self)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"ExternalTools"


        @property
        def description (self):
            return _(u"""Open notes files with external editor.
Added (:exec:) command for creation link for execute external tools from wiki page.

<b>Examples</b>
(:exec text="Open gvim in diff mode":)
gvim -d "file name 1.txt" "file name 2.txt"
(:execend:)
""")


        @property
        def version (self):
            return __version__


        def initialize(self):
            self.__initlocale()
            self.__controller.initialize ()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/ExternalToolsEn")

        #############################################

        def __initlocale (self):
            domain = u"externaltools"

            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)

            try:
                global _
                _ = self._init_i18n (domain, langdir)

                set_(_)
            except BaseException:
                pass
