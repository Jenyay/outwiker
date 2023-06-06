# -*- coding: utf-8 -*-

from outwiker.app.gui.pagedialog import editPage
from outwiker.gui.baseaction import BaseAction


class EditPagePropertiesAction(BaseAction):
    """
    Редактировать свойства текущей страницы
    """
    stringId = "EditPageProperties"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Page Properties…")

    @property
    def description(self):
        return _("Edit page properties")

    def run(self, params):
        if self._application.selectedPage is not None:
            editPage(self._application.mainWindow,
                     self._application.selectedPage)
