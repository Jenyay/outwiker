# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.system import getOS
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .controller import Controller


__version__ = u"1.1.4"


# Для работы этого плагина требуется OutWiker 1.6.0.632
if getCurrentVersion() < Version (1, 6, 0, 632, status=StatusSet.DEV):
    print ("Thumblist plugin. OutWiker version requirement: 1.6.0.632")
else:
    class PluginThumbGallery (Plugin):
        """
        Плагин, добавляющий обработку команды (:thumblist:) и (:thumbgallery:) в википарсер
        """
        def __init__ (self, application):
            """
            application - экземпляр класса core.application.ApplicationParams
            """
            Plugin.__init__ (self, application)
            self._controller = Controller (application)


        @property
        def name (self):
            return u"ThumbGallery"


        @property
        def description (self):
            return self._loadDescription()


        @property
        def version (self):
            return __version__


        def initialize(self):
            self._initlocale(u"thumbgallery")
            self._controller.initialize(_)


        def _initlocale (self, domain):
            langdir = unicode (os.path.join (os.path.dirname (__file__), "locale"), getOS().filesEncoding)
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException:
                pass


        def destroy (self):
            """
            Уничтожение (выгрузка) плагина. Здесь плагин должен отписаться от всех событий
            """
            self._controller.destroy()


        @property
        def url (self):
            return _(u"http://jenyay.net/Outwiker/ThumbGalleryEn")


        def _loadDescription (self):
            """
            Загрузить описание плагина из файла
            """
            path = _(u"locale/description.html")
            currentDir = unicode (os.path.dirname (__file__), getOS().filesEncoding)
            fullpath = os.path.join (currentDir, path)

            try:
                with open (fullpath) as fp:
                    return unicode (fp.read (), "utf8")
            except IOError:
                return _(u"Can't load description")
