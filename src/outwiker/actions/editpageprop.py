# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.pagedialog import editPage


class EditPagePropertiesAction (BaseAction):
    """
    Добавить страницу того же уровня, что и выбранная
    """
    stringId = u"EditPageProperties"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Page Properties…")


    @property
    def description (self):
        return _(u"Edit page properties")


    def run (self, params):
        if self._application.selectedPage is not None:
            editPage (self._application.mainWindow,
                      self._application.selectedPage)
