# -*- coding: UTF-8 -*-

import os.path
import logging

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

logger = logging.getLogger('texequation')


if getCurrentVersion() < Version(2, 1, 0, 835, status=StatusSet.DEV):
    logger.warning("TexEquation plugin. OutWiker version requirement: 2.1.0.835")
else:
    from .i18n import set_
    from .controller import Controller

    class PluginTexEquation(Plugin):
        def __init__(self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            super(PluginTexEquation, self).__init__(application)
            self.__controller = Controller(self, application)

        @property
        def application(self):
            return self._application

        ###################################################
        # Свойства и методы, которые необходимо определить
        ###################################################

        @property
        def name(self):
            return u"TeXEquation"

        @property
        def description(self):
            return _(u"TeXEquation plug-in allow to insert equations in the TeX format.")

        @property
        def url(self):
            return _(u"http://jenyay.net/Outwiker/TexEquationEn")

        def initialize(self):
            self._initlocale(u"texequation")
            self.__controller.initialize()

        def destroy(self):
            """
            Уничтожение(выгрузка) плагина.
            Здесь плагин должен отписаться от всех событий
            """
            self.__controller.destroy()

        #############################################

        def _initlocale(self, domain):
            langdir = os.path.join(os.path.dirname(__file__), "locale")
            global _

            try:
                _ = self._init_i18n(domain, langdir)
            except BaseException as e:
                logger(e)

            set_(_)
