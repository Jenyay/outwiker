# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import showError
from outwiker.core.system import getOS, getPluginsDirList


class OpenPluginsFolderAction (BaseAction):
    """
    Открыть папку с плагинами
    """
    stringId = u"OpenPluginsFolder"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Open Plugins Folder")

    @property
    def description(self):
        return _(u"Open folder with plugins")

    def run(self, params):
        # 0 - папка рядом с запускаемым файлом,
        # затем идут другие папки, если они есть
        pluginsDir = getPluginsDirList()[-1]
        try:
            getOS().startFile(pluginsDir)
        except OSError:
            text = _(u"Can't open folder '{}'".format(pluginsDir))
            showError(self._application.mainWindow, text)
