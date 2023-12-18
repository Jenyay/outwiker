import wx

from outwiker.core.treetools import testreadonly
from outwiker.core.tagscommands import renameTag, removeTagsFromBranch
from outwiker.gui.dialogs.messagebox import MessageBox


class TagPopupMenu:
    def __init__(self, parent, tag_name, application):
        self.ID_RENAME_TAG = None
        self.ID_DESTROY_TAG = None

        self._parent = parent
        self._tag_name = tag_name
        self._application = application

        self._menu = self._create_popup_menu()

    def _create_popup_menu(self) -> wx.Menu:
        menu = wx.Menu()

        self.ID_RENAME_TAG = menu.Append(wx.ID_ANY, _("Rename tag")).GetId()
        menu.Bind(wx.EVT_MENU, handler=self._onRenameTag, id=self.ID_RENAME_TAG)

        self.ID_DESTROY_TAG = menu.Append(wx.ID_ANY, _("Remove tag from all pages")).GetId()
        menu.Bind(wx.EVT_MENU, handler=self._onDestroyTag, id=self.ID_DESTROY_TAG)

        return menu

    @testreadonly
    def _onRenameTag(self, event):
        tag_name_old = self._tag_name
        with wx.TextEntryDialog(self._parent, _("Enter new tag name"), _("Tag renaming"), value=tag_name_old) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                wikiroot = self._application.wikiroot
                tag_name_new = dlg.GetValue()
                renameTag(wikiroot, tag_name_old, tag_name_new)

    @testreadonly
    def _onDestroyTag(self, event):
        if MessageBox(_("Remove tags from all pages?"), _("Tag removing"), wx.YES_NO, self._application.mainWindow) == wx.YES:
            removeTagsFromBranch(self._application.wikiroot, [self._tag_name])

    @property
    def menu(self) -> wx.Menu:
        return self._menu
