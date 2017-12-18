# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet


__version__ = u"2.0.1"


def _no_translate(text):
    return text


if getCurrentVersion() < Version(2, 1, 0, 833, status=StatusSet.DEV):
    print(u"ChangePageUID plugin. OutWiker version requirement: 2.1.0.833")
else:
    from .controller import Controller

    class PluginChangePageUid(Plugin):
        def __init__(self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__(self, application)
            self.__controller = Controller(self, application)

        @property
        def application(self):
            return self._application

        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name(self):
            return u"ChangePageUID"

        @property
        def description(self):
            return _(u"Plugin for edit a page indentifiers")

        @property
        def version(self):
            return __version__

        @property
        def url(self):
            return _(u"http://jenyay.net/Outwiker/ChangePageUidEn")

        def initialize(self):
            self._initlocale(u"changepageuid")
            self.__controller.initialize()

        def destroy(self):
            self.__controller.destroy()

        #############################################

        def _initlocale(self, domain):
            from .i18n import set_
            langdir = os.path.join(os.path.dirname(__file__), "locale")
            global _

            try:
                _ = self._init_i18n(domain, langdir)
            except BaseException:
                _ = _no_translate

            set_(_)
