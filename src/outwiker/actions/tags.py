# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import testreadonly
from outwiker.core.tagscommands import tagBranch, removeTagsFromBranch, renameTag
from outwiker.gui.tagsdialog import TagsDialog
from outwiker.gui.renametagdialog import RenameTagDialog
from outwiker.core.tagslist import TagsList


class AddTagsToBranchAction (BaseAction):
    """
    Добавить теги к ветке
    """
    stringId = u"AddTagsToBranch"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Add Tags to Branch…")


    @property
    def description (self):
        return _(u"Add tags to branch")


    def run (self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is None:
            self.addTagsToBranchGui (self._application.wikiroot,
                                     self._application.mainWindow)
        else:
            self.addTagsToBranchGui (self._application.selectedPage,
                                     self._application.mainWindow)


    @testreadonly
    def addTagsToBranchGui (self, page, parent):
        """
        Добавить теги к ветке, начинающейся со страницы page.
        Теги к самой странице page тоже добавляются
        """
        dlg = TagsDialog (parent, self._application)
        dlg.SetTitle (_(u"Add Tags to Branch"))

        if dlg.ShowModal() == wx.ID_OK:
            self._application.onStartTreeUpdate(page.root)

            try:
                tagBranch (page, dlg.tags)
            finally:
                self._application.onEndTreeUpdate(page.root)

        dlg.Destroy()


class RemoveTagsFromBranchAction (BaseAction):
    """
    Удалить теги из ветки
    """
    stringId = u"RemoveTagsFromBranch"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Remove Tags from Branch…")


    @property
    def description (self):
        return _(u"Remove tags from branch")


    def run (self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is None:
            return

        if self._application.selectedPage is None:
            self.removeTagsFromBranchGui (
                self._application.wikiroot,
                self._application.mainWindow)
        else:
            self.removeTagsFromBranchGui (
                self._application.selectedPage,
                self._application.mainWindow)


    @testreadonly
    def removeTagsFromBranchGui (self, page, parent):
        """
        Удалить теги из ветки, начинающейся со страницы page
        """
        dlg = TagsDialog (parent, self._application)
        dlg.SetTitle (_(u"Remove Tags from Branch"))

        if dlg.ShowModal() == wx.ID_OK:
            self._application.onStartTreeUpdate(page.root)

            try:
                removeTagsFromBranch (page, dlg.tags)
            finally:
                self._application.onEndTreeUpdate(page.root)

        dlg.Destroy()


class RenameTagAction (BaseAction):
    """
    Переименовать тег
    """
    stringId = u"RenameTag"

    def __init__ (self, application):
        self._application = application


    @property
    def title (self):
        return _(u"Rename Tag…")


    @property
    def description (self):
        return _(u"Rename tag")


    def run (self, params):
        assert self._application.mainWindow is not None

        if self._application.wikiroot is not None:
            self.renameTagGui (
                self._application.wikiroot,
                self._application.mainWindow)


    @testreadonly
    def renameTagGui (self, wikiroot, parent):
        tagslist = TagsList (wikiroot)

        dlg = RenameTagDialog (parent, tagslist)
        if dlg.ShowModal() == wx.ID_OK:
            self._application.onStartTreeUpdate(wikiroot)

            try:
                renameTag (wikiroot, dlg.oldTagName, dlg.newTagName)
            finally:
                self._application.onEndTreeUpdate(wikiroot)

        dlg.Destroy()
