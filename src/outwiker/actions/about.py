# -*- coding: utf-8 -*-

import outwiker
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.dialogs.about import AboutDialog


class AboutAction (BaseAction):
    """
    Открыть диалог "О программе"
    """
    stringId = u"About"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"About…")

    @property
    def description(self):
        return _(u'Open "About" dialog')

    def run(self, params):
        assert self._application.mainWindow is not None

        version = outwiker.__version__
        dlg = AboutDialog(version, self._application.mainWindow)
        dlg.ShowModal()
        dlg.Destroy()
