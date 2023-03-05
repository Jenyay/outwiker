# -*- coding: utf-8 -*-

from outwiker.api.services.messages import showError
from outwiker.gui.baseaction import BaseAction
from outwiker.core.system import getOS, getPluginsDirList


class OpenPluginsFolderAction(BaseAction):
    """
    Открыть папку с плагинами
    """
    stringId = "OpenPluginsFolder"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Open Plugins Folder")

    @property
    def description(self):
        return _("Open folder with plugins")

    def run(self, params):
        # 0 - папка рядом с запускаемым файлом,
        # затем идут другие папки, если они есть
        pluginsDir = getPluginsDirList()[-1]
        try:
            getOS().startFile(pluginsDir)
        except OSError:
            text = _("Can't open folder '{}'".format(pluginsDir))
            showError(self._application.mainWindow, text)
