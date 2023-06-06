# -*- coding: utf-8 -*-

import os
import sys

from outwiker.api.core.plugins import Plugin

from .i18n import set_


class PluginMarkdown(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
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
        return "Markdown"

    @property
    def description(self):
        return _("The Markdown plug-in add a new page type with Markdown notation")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/MarkdownEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        self.__controller.clear()

    #############################################

    def _correctSysPath(self):
        libs_path = os.path.join(self._pluginPath, "markdown_plugin_libs")

        if self._pluginPath not in sys.path:
            sys.path.insert(0, self._pluginPath)

        if libs_path not in sys.path:
            sys.path.insert(0, libs_path)
