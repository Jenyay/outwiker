# -*- coding: UTF-8 -*-

import os
import sys

from outwiker.core.pluginbase import Plugin

from .i18n import set_


class PluginMarkdown(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        Plugin.__init__(self, application)
        self._correctSysPath()

        from .controller import Controller
        self.__controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return u"Markdown"

    @property
    def description(self):
        return _(u"The Markdown plug-in add a new page type with Markdown notation")

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/MarkdownEn")

    def initialize(self):
        self._initlocale(u'markdown')
        self.__controller.initialize()

    def destroy(self):
        self.__controller.clear()

    #############################################

    def _correctSysPath(self):
        libs_path = os.path.join(self._pluginPath, u'markdown_plugin_libs')

        if self._pluginPath not in sys.path:
            sys.path.insert(0, self._pluginPath)

        if libs_path not in sys.path:
            sys.path.insert(0, libs_path)

    def _initlocale(self, domain):
        langdir = os.path.join(self._pluginPath, "locale")
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException:
            pass

        set_(_)
