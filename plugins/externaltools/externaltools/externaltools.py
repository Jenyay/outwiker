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

For OutWiker 1.9 and above ExternalTools adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command has the following optional parameters:
<ul>
<li>format. If the parameter equals "button" command will create a button instead of a link.</li>
<li>title. The parameter sets the text for link or button.</li>
</ul>

The (:exec:) command allow to run many applications. Every application must writed on the separated lines.

If line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.

<b>Examples</b>

Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>

Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>

Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\\myfolder\\path to file name"
(:execend:)</pre></code>

Run many applications:
<code><pre>(:exec text="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>
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
