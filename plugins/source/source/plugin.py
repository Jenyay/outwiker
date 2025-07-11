# -*- coding: utf-8 -*-

import os.path
import sys

from outwiker.api.core.plugins import Plugin

from .i18n import set_


class PluginSource(Plugin):
    """
    Плагин, добавляющий обработку команды (:source:) в википарсер
    """

    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)

        self.__correctSysPath()

        from .controller import Controller

        self.__controller = Controller(self, application)

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def __correctSysPath(self):
        plugin_path = os.path.dirname(os.path.abspath(__file__))
        libs_path = os.path.join(plugin_path, "source_plugin_libs")

        if plugin_path not in sys.path:
            sys.path.insert(0, plugin_path)

        if libs_path not in sys.path:
            sys.path.insert(0, libs_path)

        from pygments.lexers._mapping import LEXERS
        LEXERS["OneSLexer"] = ('1S', '1S', ('1s', '1c'), ('*.1s', '*.prm', '*.1cpp'), ('text/x-1s',))

    @property
    def name(self):
        return "Source"

    @property
    def description(self):
        description = _(
            "Add command (:source:) in wiki parser. This command highlight your source code."
        )

        usage = _(
            """<B>Usage:</B>:
(:source params... :)
source code
(:sourceend:)"""
        )

        params = _(
            """<B>Params:</B>
<U>lang</U> - programming language

<U>tabwidth</U> - tab size

<U>file</U> - attached source file

<U>encoding</U> - encoding of the attached source file (default encoding - utf8)

<U>style</U> - style of hightlighting

<U>parentbg</U> - use the page background for the code block

<U>linenum</U> - enable line numbers"""
        )

        example1 = _(
            """<B>Example 1:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>"""
        )

        example2 = _(
            """<B>Example 2:</B>
<PRE>(:source lang="python" style="autumn":)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>"""
        )

        example3 = _(
            """<B>Example 3:</B>
<PRE>(:source lang="python" tabwidth=4 parentbg linenum:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>"""
        )

        example4 = _(
            """<B>Example 4:</B>
<PRE>(:source file="Attach:example.cs" encoding="cp1251":)(:sourceend:)</PRE>"""
        )

        example5 = _(
            """<B>Example 5:</B>
<PRE>(:source file="Attach:example.txt" lang="python":)(:sourceend:)</PRE>"""
        )

        return """{description}

{usage}

{params}

{example1}

{example2}

{example3}

{example4}

{example5}""".format(
            description=description,
            usage=usage,
            params=params,
            example1=example1,
            example2=example2,
            example3=example3,
            example4=example4,
            example5=example5,
        )

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/SourcePluginEn")

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
