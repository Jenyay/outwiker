# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction

from hackpage.utils import setPageFolderWithDialog
from hackpage.i18n import get_


class ChangePageFolderAction(BaseAction):
    """
    Change the current page folder (title)
    """
    def __init__(self, application, controller):
        self._application = application
        self._controller = controller

        global _
        _ = get_()

    stringId = u"HackPage_ChangePageFolder"

    @property
    def title(self):
        return _(u"Change page folder...")

    @property
    def description(self):
        return _(u"HackPage plugin. Set current page folder")

    def run(self, params):
        setPageFolderWithDialog(self._application.selectedPage,
                                self._application)
