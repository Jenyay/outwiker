# -*- coding: utf-8 -*-

from typing import Union
import wx

from outwiker.app.gui.dialogs.renametagdialog import RenameTagDialog
from outwiker.core.tagscommands import tagBranch, removeTagsFromBranch, renameTag
from outwiker.core.tagslist import TagsList
from outwiker.core.treetools import testreadonly
from outwiker.gui.baseaction import BaseAction
from outwiker.gui.guiconfig import TagsConfig
from outwiker.gui.tagsdialog import TagsDialog


def _set_tags_cloud_font_size(application, dlg: Union[RenameTagDialog, TagsDialog]):
    config = TagsConfig(application.config)
    minFontSize = config.minFontSize.value
    maxFontSize = config.maxFontSize.value
    mode = config.tagsCloudMode.value
    dlg.setTagsCloudFontSize(minFontSize, maxFontSize)
    dlg.setTagsCloudMode(mode)


class AddTagsToBranchAction(BaseAction):
    """
    Добавить теги к ветке
    """

    stringId = "AddTagsToBranch"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Add Tags to Branch…")

    @property
    def description(self):
        return _("Add tags to branch")

    def run(self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is None:
            self.addTagsToBranchGui(
                self._application.wikiroot, self._application.mainWindow
            )
        else:
            self.addTagsToBranchGui(
                self._application.selectedPage, self._application.mainWindow
            )

    @testreadonly
    def addTagsToBranchGui(self, page, parent):
        """
        Добавить теги к ветке, начинающейся со страницы page.
        Теги к самой странице page тоже добавляются
        """
        with TagsDialog(parent, self._application) as dlg:
            _set_tags_cloud_font_size(self._application, dlg)

            dlg.SetTitle(_("Add Tags to Branch"))

            if dlg.ShowModal() == wx.ID_OK:
                self._application.onStartTreeUpdate(page.root)

                try:
                    tagBranch(page, dlg.tags)
                finally:
                    self._application.onEndTreeUpdate(page.root)


class RemoveTagsFromBranchAction(BaseAction):
    """
    Удалить теги из ветки
    """

    stringId = "RemoveTagsFromBranch"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Remove Tags from Branch…")

    @property
    def description(self):
        return _("Remove tags from branch")

    def run(self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is None:
            self.removeTagsFromBranchGui(
                self._application.wikiroot, self._application.mainWindow
            )
        else:
            self.removeTagsFromBranchGui(
                self._application.selectedPage, self._application.mainWindow
            )

    @testreadonly
    def removeTagsFromBranchGui(self, page, parent):
        """
        Удалить теги из ветки, начинающейся со страницы page
        """
        with TagsDialog(parent, self._application) as dlg:
            dlg.SetTitle(_("Remove Tags from Branch"))
            _set_tags_cloud_font_size(self._application, dlg)

            if dlg.ShowModal() == wx.ID_OK:
                self._application.onStartTreeUpdate(page.root)

                try:
                    removeTagsFromBranch(page, dlg.tags)
                finally:
                    self._application.onEndTreeUpdate(page.root)


class RenameTagAction(BaseAction):
    """
    Переименовать тег
    """

    stringId = "RenameTag"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Rename Tag…")

    @property
    def description(self):
        return _("Rename tag")

    def run(self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is not None:
            self.renameTagGui(self._application.wikiroot, self._application.mainWindow)

    @testreadonly
    def renameTagGui(self, wikiroot, parent):
        tagslist = TagsList(wikiroot)

        with RenameTagDialog(parent, tagslist) as dlg:
            _set_tags_cloud_font_size(self._application, dlg)
            if dlg.ShowModal() == wx.ID_OK:
                self._application.onStartTreeUpdate(wikiroot)

                try:
                    renameTag(wikiroot, dlg.oldTagName, dlg.newTagName)
                finally:
                    self._application.onEndTreeUpdate(wikiroot)
