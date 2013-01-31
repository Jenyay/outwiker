#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .sourceconfig import SourceConfig
from .controller import Controller
from .i18n import set_
from .insertdialogcontroller import InsertDialogController


# Для работы этого плагина требуется OutWiker 1.7
if getCurrentVersion() < Version (1, 7, 0, 680, status=StatusSet.DEV):
    print ("Source plugin. OutWiker version requirement: 1.7.0.680")
else:
    class PluginSource (Plugin):
        """
        Плагин, добавляющий обработку команды (:source:) в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.__version = u"1.9"
            self.__controler = Controller(self, application)


        def initialize(self):
            self._initlocale(u"source")

            self.__correctSysPath()

            self.__controler.initialize()


        def __correctSysPath (self):
            cmd_folder = unicode (os.path.dirname(os.path.abspath(__file__)), getOS().filesEncoding )

            syspath = [unicode (item, getOS().filesEncoding) 
                    if type (item) != type(u"") 
                    else item for item in sys.path]

            if cmd_folder not in syspath:
                sys.path.insert(0, cmd_folder)


        @property
        def config (self):
            return SourceConfig (self._application.config)


        @property
        def name (self):
            return u"Source"


        @property
        def description (self):
            return _(u"""Add command (:source:) in wiki parser. This command highlight your source code.

<B>Usage:</B>:
(:source params... :)
source code
(:sourceend:)

<B>Params:</B>
<I>lang</I> - programming language
<I>tabwidth</I> - tab size
<I>file</I> - attached source file
<I>encoding</I> - encoding of the attached source file (default encoding - utf8)

<B>Example 1:</B>
<PRE>(:source lang="python" tabwidth=4:)
import os

if __name__ == "__main__":
    print "Hello World!"
(:sourceend:)
</PRE>

<B>Example 2:</B>
<PRE>(:source file="Attach:example.cs" encoding="cp1251":)(:sourceend:)</PRE>

<B>Example 3:</B>
<PRE>(:source file="Attach:example.txt" lang="python":)(:sourceend:)</PRE>
""")


        @property
        def version (self):
            return self.__version

        
        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/SourcePluginEn")


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
            self.__controler.destroy()


        @property
        def insertDialogControllerClass (self):
            """
            Возвращает класс (не экземпляр класса) InsertDialogController.
            Используется для тестирования
            """
            return InsertDialogController
