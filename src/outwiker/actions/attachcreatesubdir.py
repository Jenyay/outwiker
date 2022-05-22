# -*- coding=utf-8 -*-

import logging
from pathlib import Path

from outwiker.core.attachment import Attachment
from outwiker.core.commands import showError, testreadonly
from outwiker.core.events import BeginAttachRenamingParams
from outwiker.gui.baseaction import BaseAction


logger = logging.getLogger('outwiker.actions.AttachCreateSubdirAction')


class AttachCreateSubdirAction(BaseAction):
    """
    Create new subdirectory for current attach subdirectory of selected page
    """
    stringId = 'AttachCreateSubdir'

    def __init__(self, application):
        self._application = application
        self.default_subdir_name = _('New folder')

    @property
    def title(self):
        return _('Create a new attached folder')

    @property
    def description(self):
        return _('Create a new folder in the current attached folder')

    @testreadonly
    def run(self, params):
        page = self._application.selectedPage
        if page is not None:
            attach = Attachment(page)
            root = Path(attach.getAttachPath(create=True), page.currentAttachSubdir)

            dirname = self.default_subdir_name
            index = 1

            while (root / dirname).exists():
                dirname = '{name} ({index})'.format(name=self.default_subdir_name, index=index)
                index += 1

            try:
                attach.createSubdir(Path(page.currentAttachSubdir, dirname))
                self._application.onBeginAttachRenaming(page, BeginAttachRenamingParams(str(dirname)))
            except IOError as e:
                message = _("Can't create folder {} for attachments").format(dirname)
                showError(self._application.mainWindow, message)
                logger.error("Can't create attachments subdir %s for the page '%s'. Error: %s", dirname, page.subpath, str(e))


class AttachCreateSubdirActionForAttachPanel(AttachCreateSubdirAction):
    stringId = 'AttachCreateSubdirForAttachPanel'

    @property
    def description(self):
        return _('Create a new folder in the current attached folder. Action for attachments panel')
