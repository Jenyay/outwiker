# -*- coding: utf-8 -*-

import os.path
import sys

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS

from .controller import Controller
from .i18n import set_


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
        self._initlocale(u"updatenotifier")
        self._controller.initialize()

    def destroy(self):
        self._controller.destroy()

    @property
    def pluginPath(self):
        return self._pluginPath

    def _initlocale(self, domain):
        langdir = unicode(os.path.join(os.path.dirname(__file__), "locale"),
                          getOS().filesEncoding)
        global _

        try:
            _ = self._init_i18n(domain, langdir)
        except BaseException, e:
            print e

        set_(_)

    def _correctSysPath(self):
        syspath = [unicode(item, getOS().filesEncoding)
                   if not isinstance(item, unicode)
                   else item for item in sys.path]

        libspath = os.path.join(self._pluginPath, u'libs')
        if libspath not in syspath:
            sys.path.insert(0, libspath)
