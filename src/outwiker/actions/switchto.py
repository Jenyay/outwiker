# -*- coding: UTF-8 -*-

from outwiker.gui.baseaction import BaseAction


class SwitchToMainPanelAction(BaseAction):
    """
    Set focus to main panel.
    """
    stringId = u"GoToMainPanel"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Main panel")

    @property
    def description(self):
        return _(u"Set focus to main panel")

    def run(self, params):
        panel = self._application.mainWindow.pagePanel
        if panel.isShown():
            panel.setFocus()


class SwitchToTreeAction(BaseAction):
    """
    Set focus to notes tree.
    """
    stringId = u"GoToNotesTree"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Notes tree")

    @property
    def description(self):
        return _(u"Set focus to notes tree")

    def run(self, params):
        panel = self._application.mainWindow.treePanel
        if panel.isShown():
            panel.setFocus()


class SwitchToAttachmentsAction(BaseAction):
    """
    Set focus to attachments panel.
    """
    stringId = u"GoToAttachments"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Attachments")

    @property
    def description(self):
        return _(u"Set focus to attachments panel")

    def run(self, params):
        panel = self._application.mainWindow.attachPanel
        if panel.isShown():
            panel.setFocus()


class SwitchToTagsCloudAction(BaseAction):
    """
    Set focus to tags cloud panel.
    """
    stringId = u"GoToTags"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Tags")

    @property
    def description(self):
        return _(u"Set focus to tags cloud panel")

    def run(self, params):
        panel = self._application.mainWindow.tagsCloudPanel
        if panel.isShown():
            panel.setFocus()
