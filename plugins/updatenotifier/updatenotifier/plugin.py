# -*- coding: utf-8 -*-

import logging
import os.path
import sys

from outwiker.core.pluginbase import Plugin

from .controller import Controller
from .i18n import set_


logger = logging.getLogger('updatenotifier')


class PluginUpdateNotifier(Plugin):
    def __init__(self, application):
        super(PluginUpdateNotifier, self).__init__(application)
        self._correctSysPath()
        self._controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    @property
    def name(self):
        return u"UpdateNotifier"

    @property
    def description(self):
        return _(u'''Check for update OutWiker and plug-ins for it.

Append menu item "Help -> Check for Updates..."''')

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/UpdateNotifierEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._controller.initialize()

    def destroy(self):
        self._controller.destroy()

    @property
    def pluginPath(self):
        return self._pluginPath

    def _correctSysPath(self):
        libspath = os.path.join(self._pluginPath, u'libs')
        if libspath not in sys.path:
            sys.path.insert(0, libspath)
