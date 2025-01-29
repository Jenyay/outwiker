# -*- coding: utf-8 -*-

from outwiker.app.gui.pagedialog import createChildPage
from outwiker.gui.baseaction import BaseAction


class AddChildPageAction(BaseAction):
    """Добавить дочернюю страницу по отношению к текущей"""

    stringId = 'AddChildPage'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('Add Child Page…')

    @property
    def description(self):
        return _('Add child page')

    def run(self, params):
        createChildPage(self._application.mainWindow,
                        self._application.selectedPage,
                        self._application)
