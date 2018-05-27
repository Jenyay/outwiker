# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.preferences.prefdialog import PrefDialog


class PreferencesAction(BaseAction):
    """
    Вызов диалога настроек
    """
    stringId = u"Preferences"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Preferences…")

    @property
    def description(self):
        return _(u"Open the preferences dialog")

    def run(self, params):
        dlg = PrefDialog(self._application.mainWindow, self._application)
        dlg.ShowModal()
        dlg.Destroy()
