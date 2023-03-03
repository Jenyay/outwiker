# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.app.gui.pagedialog import createSiblingPage


class AddSiblingPageAction (BaseAction):
    """Добавить страницу того же уровня, что и выбранная"""

    stringId = 'AddSiblingPage'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('Add Sibling Page…')

    @property
    def description(self):
        return _('Add sibling page')

    def run(self, params):
        createSiblingPage(self._application.mainWindow,
                          self._application.selectedPage)
