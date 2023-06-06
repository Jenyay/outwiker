# -*- coding: utf-8 -*-

from outwiker.api.gui.dialogs import BaseLinkDialogController

from .linkcreator import LinkCreator


class LinkDialogController(BaseLinkDialogController):
    def __init__(self, application, page, dialog, selectedString):
        super().__init__(page, dialog, selectedString)
        self._application = application

    @property
    def linkResult(self):
        """
        Return link notation.
        """
        creator = LinkCreator()
        return creator.create(self.link, self.comment, self._dlg.title)

    def createFileLink(self, fname):
        """
        Return link to attached file
        """
        return "__attach/{}".format(fname)
