# -*- coding: UTF-8 -*-

import os.path
import logging

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


if getCurrentVersion() < Version(2, 0, 0, 806, status=StatusSet.BETA):
    logging.warning("Snippets plugin. OutWiker version requirement: 2.0.0.806")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginSnippets (Plugin):
        def __init__(self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super(PluginSnippets, self).__init__(application)
            self.__controller = Controller(self, application)

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
            return _(u"Plugin to store text templates")

        @property
        def url(self):
            return _(u"http://jenyay.net/Outwiker/Snippets")

        def initialize(self):
            self._initlocale(u'snippets')
            self.__controller.initialize()

        def destroy(self):
            self.__controller.destroy()

        #############################################

        def _initlocale(self, domain):
            langdir = unicode(os.path.join(os.path.dirname(__file__),
                                           "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n(domain, langdir)
            except BaseException, e:
                print e

            set_(_)
