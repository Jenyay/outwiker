# -*- coding: utf-8 -*-

import outwiker
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.dialogs.about import AboutDialog


class AboutAction(BaseAction):
    '''Open the About dialog'''

    stringId = 'About'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('About…')

    @property
    def description(self):
        return _('Open "About" dialog')

    def run(self, params):
        assert self._application.mainWindow is not None

        version = outwiker.getVersionStr()
        with AboutDialog(version, self._application.mainWindow) as dlg:
            dlg.ShowModal()
