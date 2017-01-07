# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


__version__ = u"1.0"


def _no_translate(text):
    return text


if getCurrentVersion() < Version(2, 0, 0, 807, status=StatusSet.DEV):
    print(u"HackPage plugin. OutWiker version requirement: 2.0.0.807")
else:
    from hackpage.controller import Controller

    class PluginHackPage(Plugin):
        def __init__(self, application):
            super(PluginHackPage, self).__init__(application)
            self.__controller = Controller(self, application)

        @property
        def application(self):
            return self._application

        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name(self):
            return u"HackPage"

        @property
        def description(self):
            return _(u"Plugin for edit low-level page parameters")

        @property
        def version(self):
            return __version__

        @property
        def url(self):
            return _(u"http://jenyay.net/Outwiker/HackPageEn")

        def initialize(self):
            self._initlocale(u"hackpage")
            self.__controller.initialize()

        def destroy(self):
            self.__controller.destroy()

        #############################################

        def _initlocale(self, domain):
            from .i18n import set_
            langdir = unicode(os.path.join(os.path.dirname(__file__),
                                           "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n(domain, langdir)
            except BaseException:
                _ = _no_translate

            set_(_)
