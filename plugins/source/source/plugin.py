# -*- coding: utf-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin

from .i18n import set_


class PluginSource(Plugin):
    """
    Плагин, добавляющий обработку команды (:source:) в википарсер
    """

    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__(self, application)

        self.__correctSysPath()

        from .controller import Controller
        self.__controller = Controller(self, application)

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def __correctSysPath(self):
        cmd_folder = os.path.dirname(os.path.abspath(__file__))

        if cmd_folder not in sys.path:
            sys.path.insert(0, cmd_folder)

    @property
    def name(self):
        return u"Source"

    @property
    def description(self):
        description = _(
            u"Add command (:source:) in wiki parser. This command highlight your source code.")

        usage = _(u"""<B>Usage:</B>:
(:source params... :)
source code
(:sourceend:)""")

        params = _(u"""<B>Params:</B>
<U>lang</U> - programming language

<U>tabwidth</U> - tab size

<U>file</U> - attached source file

<U>encoding</U> - encoding of the attached source file (default encoding - utf8)

<U>style</U> - style of hightlighting

<U>parentbg</U> - use the page background for the code block

<U>linenum</U> - enable line numbers""")

        example1 = _(u"""<B>Example 1:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>""")

        example2 = _(u"""<B>Example 2:</B>
<PRE>(:source lang="python" style="autumn":)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>""")

        example3 = _(u"""<B>Example 3:</B>
<PRE>(:source lang="python" tabwidth=4 parentbg linenum:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>""")

        example4 = _(u"""<B>Example 4:</B>
<PRE>(:source file="Attach:example.cs" encoding="cp1251":)(:sourceend:)</PRE>""")

        example5 = _(u"""<B>Example 5:</B>
<PRE>(:source file="Attach:example.txt" lang="python":)(:sourceend:)</PRE>""")

        return u"""{description}

{usage}

{params}

{example1}

{example2}

{example3}

{example4}

{example5}""".format(description=description,
                     usage=usage,
                     params=params,
                     example1=example1,
                     example2=example2,
                     example3=example3,
                     example4=example4,
                     example5=example5)

    @property
    def url(self):
        return _(u"https://jenyay.net/Outwiker/SourcePluginEn")

    def destroy(self):
        """
        Уничтожение (выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    @property
    def config(self):
        from .sourceconfig import SourceConfig
        return SourceConfig(self._application.config)
