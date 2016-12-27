# -*- coding: UTF-8 -*-

import os.path
import logging

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet
from outwiker.core.system import getOS


def _no_translate(text):
    return text


if getCurrentVersion() < Version(2, 0, 0, 807, status=StatusSet.DEV):
    logging.warning("HackPage plugin. OutWiker version requirement: 2.0.0.807")
else:
    # from .controller import Controller

    class PluginName(Plugin):
        def __init__(self, application):
            """
            application - Instance of the
                core.application.ApplicationParams class
            """
            super(PluginName, self).__init__(application)
            # self.__controller = Controller(self, application)

        @property
        def application(self):
            return self._application

        #########################################
        # Properties and methods to overloading #
        #########################################

        @property
        def name(self):
            return u"HackPage"

        @property
        def description(self):
            return _(u"Plugin description")

        @property
        def url(self):
            return _(u"http://jenyay.net")

        def initialize(self):
            self._initlocale(u"hackpage")
            # self.__controller.initialize()

        def destroy(self):
            """
            Destroy (unload) the plugin.
            The plugin must unbind all events.
            """
            # self.__controller.destroy()
            pass

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
