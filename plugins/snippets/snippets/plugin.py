# -*- coding: UTF-8 -*-

import os.path
import logging
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


def _no_translate(text):
    return text


if getCurrentVersion() < Version(2, 0, 0, 806, status=StatusSet.BETA):
    logging.warning("Snippets plugin. OutWiker version requirement: 2.0.0.806")
else:
    class PluginSnippets (Plugin):
        def __init__(self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super(PluginSnippets, self).__init__(application)
            self._correctSysPath()

            self.__controller = None

        @property
        def application(self):
            return self._application

        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name(self):
            return u"Snippets"

        @property
        def description(self):
            return _(u"Plugin to store text snippets")

        @property
        def url(self):
            return _(u"http://jenyay.net/Outwiker/SnippetsEn")

        def initialize(self):
            self._initlocale(u'snippets')
            from .controller import Controller

            self.__controller = Controller(self, self._application)
            self.__controller.initialize()

        def destroy(self):
            self.__controller.destroy()

        #############################################

        def _initlocale(self, domain):
            from snippets.i18n import set_
            langdir = unicode(os.path.join(os.path.dirname(__file__),
                                           "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n(domain, langdir)
            except BaseException:
                _ = _no_translate

            set_(_)

        def _correctSysPath(self):
            syspath = [unicode(item, getOS().filesEncoding)
                       if not isinstance(item, unicode)
                       else item for item in sys.path]

            libspath = os.path.join(self._pluginPath, u'libs')
            if libspath not in syspath:
                sys.path.insert(0, libspath)
