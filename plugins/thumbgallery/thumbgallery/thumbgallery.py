# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.pluginbase import Plugin
from outwiker.core.commands import getCurrentVersion
from outwiker.core.version import Version, StatusSet

from .controller import Controller


__version__ = u"2.0.1"


if getCurrentVersion() < Version(2, 1, 0, 833, status=StatusSet.DEV):
    print ("Thumblist plugin. OutWiker version requirement: 2.1.0.833")
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
            langdir = os.path.join(os.path.dirname (__file__), "locale")
            global _

            try:
                _ = self._init_i18n (domain, langdir)
            except BaseException as e:
                print (e)


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
            currentDir = os.path.dirname (__file__)
            fullpath = os.path.join (currentDir, path)

            try:
                with open (fullpath) as fp:
                    return fp.read()
            except IOError:
                return _(u"Can't load description")
