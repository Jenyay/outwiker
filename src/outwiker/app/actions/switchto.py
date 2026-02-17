# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction


class SwitchToMainPanelAction(BaseAction):
    """
    Set focus to main panel.
    """

    stringId = "GoToMainPanel"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Main panel")

    @property
    def description(self):
        return _("Set focus to main panel")

    def run(self, params):
        panel = self._application.mainWindow.pagePanel
        if panel.isShown():
            panel.setFocus()


class SwitchToTreeAction(BaseAction):
    """
    Set focus to note tree.
    """

    stringId = "GoToNotesTree"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Note tree")

    @property
    def description(self):
        return _("Set focus to note tree")

    def run(self, params):
        panel = self._application.mainWindow.treePanel
        if panel.isShown():
            panel.setFocus()


class SwitchToAttachmentsAction(BaseAction):
    """
    Set focus to attachments panel.
    """

    stringId = "GoToAttachments"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Attachments")

    @property
    def description(self):
        return _("Set focus to attachments panel")

    def run(self, params):
        panel = self._application.mainWindow.attachPanel
        if panel.isShown():
            panel.setFocus()


class SwitchToTagsCloudAction(BaseAction):
    """
    Set focus to tag cloud panel.
    """

    stringId = "GoToTags"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Tags")

    @property
    def description(self):
        return _("Set focus to tag cloud panel")

    def run(self, params):
        panel = self._application.mainWindow.tagsCloudPanel
        if panel.isShown():
            panel.setFocus()
