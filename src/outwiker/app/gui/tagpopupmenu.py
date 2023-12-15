import wx

from outwiker.core.treetools import testreadonly
from outwiker.core.tagscommands import renameTag


class TagPopupMenu:
    def __init__(self, parent, tag_name, application):
        self.ID_RENAME_TAG = None

        self._parent = parent
        self._tag_name = tag_name
        self._application = application

        self._menu = self._create_popup_menu()

    def _create_popup_menu(self) -> wx.Menu:
        menu = wx.Menu()

        self.ID_RENAME_TAG = menu.Append(wx.ID_ANY, _("Rename tag")).GetId()
        menu.Bind(wx.EVT_MENU, self._onRenameTag, id=self.ID_RENAME_TAG)

        return menu

    @testreadonly
    def _onRenameTag(self, event):
        wikiroot = self._application.wikiroot
        tag_name_old = self._tag_name
        with wx.TextEntryDialog(self._parent, _("Enter new tag name"), _("Tag renaming"), value=tag_name_old) as dlg:
            tag_name_new = dlg.GetValue()

    @property
    def menu(self) -> wx.Menu:
        return self._menu
