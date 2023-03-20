# -*- coding=utf-8 -*-

from outwiker.app.services.attachment import createSubdir
from outwiker.core.treetools import testreadonly
from outwiker.gui.baseaction import BaseAction


class AttachCreateSubdirAction(BaseAction):
    """
    Create new subdirectory for current attach subdirectory of selected page
    """
    stringId = 'AttachCreateSubdir'

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _('Create a new attached folder')

    @property
    def description(self):
        return _('Create a new folder in the current attached folder')

    @testreadonly
    def run(self, params):
        page = self._application.selectedPage
        createSubdir(page, self._application)


class AttachCreateSubdirActionForAttachPanel(AttachCreateSubdirAction):
    stringId = 'AttachCreateSubdirForAttachPanel'

    @property
    def description(self):
        return _('Create a new folder in the current attached folder. Action for attachments panel')
