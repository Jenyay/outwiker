# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


if getCurrentVersion() < Version (1, 8, 0, 731, status=StatusSet.DEV):
    print ("ChangeUID plugin. OutWiker version requirement: 1.8.0.731")
else:
    from .i18n import set_
    from .controller import Controller
    from .contentsparser import ContentsParser, Section
    from .tocwikigenerator import TOCWikiGenerator
    from .tocwikimaker import TocWikiMaker

    class PluginTableOfContents (Plugin):
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self.__controller = Controller(self, application)


        @property
        def application (self):
            return self._application


        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name (self):
            return u"TableOfContents"


        @property
        def description (self):
            return _(u'''Plugin add the menu "Wiki - Table of contents" and the wiki command (:toc:) for generation of the table of contents.''')


        @property
        def version (self):
            return u"1.0"


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/ContentsEn")


        def initialize(self):
            self._initlocale(u"tableofcontents")
            self.__controller.initialize()


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print e

            set_(_)


        @property
        def ContentsParser (self):
            return ContentsParser


        @property
        def Section (self):
            return Section


        @property
        def TOCWikiGenerator (self):
            return TOCWikiGenerator


        @property
        def TocWikiMaker (self):
            return TocWikiMaker
