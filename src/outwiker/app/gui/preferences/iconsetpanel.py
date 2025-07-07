# -*- coding: utf-8 -*-

import os.path
from outwiker.gui.images import readImage

import wx

from outwiker.core.system import getBuiltinImagePath, getIconsDirList
from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.defines import (
    ICONS_WIDTH,
    ICONS_HEIGHT,
    BUTTON_ICON_WIDTH,
    BUTTON_ICON_HEIGHT,
)
from outwiker.gui.dialogs.messagebox import MessageBox
from outwiker.gui.iconlistctrl import IconListCtrl
from outwiker.gui.iconscollection import IconsCollection, DuplicateGroupError
from outwiker.gui.testeddialog import TestedFileDialog
from outwiker.gui.preferences.prefpanel import BasePrefPanel


class IconsetPanel(BasePrefPanel):
    def __init__(self, parent):
        super().__init__(parent)

        self._default_group_cover = getBuiltinImagePath("icons_cover_default.svg")

        self.__createGuiElements()

        self._groups.Bind(wx.EVT_TREE_SEL_CHANGED, handler=self.__onGroupSelect)
        self._groups.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.__onBeginLabelEdit)
        self._groups.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.__onEndLabelEdit)
        self._groups.Bind(wx.EVT_KEY_DOWN, handler=self.__onKeyDown)

        self.__updateGroups()
        self.SetupScrolling()

    def __createGuiElements(self):
        mainSizer = wx.FlexGridSizer(cols=2, rows=1, vgap=0, hgap=0)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(0)

        #
        # Controls for groups
        groupsSizer = wx.FlexGridSizer(cols=1, rows=0, vgap=0, hgap=0)
        groupsSizer.AddGrowableCol(0)
        groupsSizer.AddGrowableRow(0)

        self._groups = wx.TreeCtrl(
            self, style=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.SUNKEN_BORDER
        )
        self._groups.SetMinSize((200, 200))

        self._imagelist = SafeImageList(ICONS_WIDTH, ICONS_HEIGHT)
        self._groups.AssignImageList(self._imagelist)

        # Buttons for groups
        groupButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add a group
        self.addGroupBtn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("add.svg"), BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
            ),
        )
        self.addGroupBtn.SetToolTip(_("Add new group"))
        self.addGroupBtn.Bind(wx.EVT_BUTTON, handler=self.__onAddGroup)

        # Remove a group
        self.removeGroupBtn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("remove.svg"), BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
            ),
        )
        self.removeGroupBtn.SetToolTip(_("Remove group"))
        self.removeGroupBtn.Bind(wx.EVT_BUTTON, handler=self.__onRemoveGroup)

        # Rename a group
        self.renameGroupBtn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("pencil.svg"), BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
            ),
        )
        self.renameGroupBtn.SetToolTip(_("Rename group"))
        self.renameGroupBtn.Bind(wx.EVT_BUTTON, handler=self.__onRenameGroup)

        groupButtonsSizer.Add(self.addGroupBtn, flag=wx.ALL, border=0)
        groupButtonsSizer.Add(self.removeGroupBtn, flag=wx.ALL, border=0)
        groupButtonsSizer.Add(self.renameGroupBtn, flag=wx.ALL, border=0)

        groupsSizer.Add(self._groups, 1, wx.RIGHT | wx.EXPAND, border=2)
        groupsSizer.Add(groupButtonsSizer, 1, wx.RIGHT | wx.EXPAND, border=2)

        #
        # Controls for icons in the group
        iconsSizer = wx.FlexGridSizer(cols=1, rows=0, vgap=0, hgap=0)
        iconsSizer.AddGrowableRow(0)
        iconsSizer.AddGrowableCol(0)

        self._iconsList = IconListCtrl(self, True)
        self._iconsList.SetMinSize((200, 150))

        # Buttons for icons in the group
        iconsButtonsSizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add icons
        self.addIconsBtn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("add.svg"), BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
            ),
        )
        self.addIconsBtn.SetToolTip(_("Add icons"))
        self.addIconsBtn.Bind(wx.EVT_BUTTON, handler=self.__onAddIcons)

        # Remove icons
        self.removeIconsBtn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("remove.svg"), BUTTON_ICON_WIDTH, BUTTON_ICON_HEIGHT
            ),
        )
        self.removeIconsBtn.SetToolTip(_("Remove selected icons"))
        self.removeIconsBtn.Bind(wx.EVT_BUTTON, handler=self.__onRemoveIcons)

        # Set icon as group cover
        self.setCoverBtn = wx.BitmapButton(
            self,
            bitmap=readImage(
                getBuiltinImagePath("folder_picture.svg"),
                BUTTON_ICON_WIDTH,
                BUTTON_ICON_HEIGHT,
            ),
        )
        self.setCoverBtn.SetToolTip(_("Set icon as group cover"))
        self.setCoverBtn.Bind(wx.EVT_BUTTON, handler=self.__onSetCover)

        iconsButtonsSizer.Add(self.addIconsBtn, flag=wx.ALL, border=0)
        iconsButtonsSizer.Add(self.removeIconsBtn, flag=wx.ALL, border=0)
        iconsButtonsSizer.Add(self.setCoverBtn, flag=wx.ALL, border=0)

        iconsSizer.Add(self._iconsList, 1, wx.LEFT | wx.EXPAND, border=2)
        iconsSizer.Add(iconsButtonsSizer, 1, wx.LEFT | wx.EXPAND, border=2)

        # Main sizer
        mainSizer.Add(groupsSizer, 1, wx.ALL | wx.EXPAND, border=0)
        mainSizer.Add(iconsSizer, 1, wx.ALL | wx.EXPAND, border=0)

        self.SetSizer(mainSizer)
        self.Layout()

    def Save(self):
        pass

    def LoadState(self):
        pass

    def __updateGroups(self):
        self._groups.DeleteAllItems()
        self._imagelist.RemoveAll()

        collection = self.__getIconsCollection()

        # Add the root element
        rootimage = collection.getCover(None)
        imageIndex = (
            -1
            if rootimage is None
            else self._imagelist.Add(readImage(rootimage, ICONS_WIDTH, ICONS_HEIGHT))
        )
        rootItem = self._groups.AddRoot(_("Not in groups"), imageIndex, data=None)

        # Add child groups
        for group in collection.getGroups():
            image = collection.getCover(group)
            if image is None:
                image = self._default_group_cover

            imageIndex = self._imagelist.Add(
                readImage(image, ICONS_WIDTH, ICONS_HEIGHT)
            )

            self._groups.AppendItem(rootItem, group, imageIndex, data=group)

        self._groups.Expand(rootItem)
        self._groups.SelectItem(rootItem)
        self.__onGroupSelect(None)

    def __getIconsCollection(self):
        return IconsCollection(getIconsDirList()[-1])

    def __showIcons(self, groupname):
        """
        Show icons from group groupname.
        If groupname is None then icons from root will be showed
        """
        self._iconsList.clear()
        collection = self.__getIconsCollection()
        icons = collection.getIcons(groupname)
        self._iconsList.setIconsList(icons)

    def __onGroupSelect(self, event):
        """
        User select other group
        """
        selItem = self._groups.GetSelection()
        if not selItem.IsOk():
            return

        group = self._groups.GetItemData(selItem)
        self.__showIcons(group)

    def __onAddGroup(self, event):
        collection = self.__getIconsCollection()
        newGroupName = self.__getNewGroupName(collection.getGroups())
        try:
            collection.addGroup(newGroupName)
            self.__updateGroups()
            self.__selectGroupItem(newGroupName)
        except (IOError, SystemError):
            MessageBox(
                _("Can't create directory for icons group"),
                _("Error"),
                wx.OK | wx.ICON_ERROR,
            )

    def __selectGroupItem(self, groupname):
        """
        Select group in _groups tree. If groupname is None then select
        the root element.
        If groupname not exists then method does nothing.
        """
        rootItem = self._groups.GetRootItem()
        assert rootItem.IsOk()

        if groupname is None:
            self._groups.SelectItem(rootItem)

        nextGroupItem, cookie = self._groups.GetFirstChild(rootItem)

        while nextGroupItem.IsOk():
            if self._groups.GetItemData(nextGroupItem) == groupname:
                self._groups.SelectItem(nextGroupItem)
                break

            nextGroupItem, cookie = self._groups.GetNextChild(rootItem, cookie)

    def __getNewGroupName(self, groups):
        """
        Return name for new group
        """
        newGroupTemplate = _("New group{}")
        newGroupName = newGroupTemplate.format("")
        if newGroupName in groups:
            # Generate new group name in format "New group(1)",
            # "New group(2)" etc
            index = 0
            while newGroupName in groups:
                index += 1
                newGroupName = newGroupTemplate.format("({})".format(index))
        return newGroupName

    def __onEndLabelEdit(self, event):
        if event.IsEditCancelled():
            return

        event.Veto()
        oldGroupName = self._groups.GetItemData(event.GetItem())
        newGroupName = event.GetLabel().strip()

        assert oldGroupName is not None

        collection = self.__getIconsCollection()

        try:
            collection.renameGroup(oldGroupName, newGroupName)
        except (IOError, SystemError):
            MessageBox(
                _("Can't rename directory for icons group"),
                _("Error"),
                wx.OK | wx.ICON_ERROR,
            )
            return
        except DuplicateGroupError:
            MessageBox(
                _('Group with name "{}" exists already').format(newGroupName),
                _("Error"),
                wx.OK | wx.ICON_ERROR,
            )
            return
        except ValueError:
            MessageBox(
                _('Invalid group name "{}"').format(newGroupName),
                _("Error"),
                wx.OK | wx.ICON_ERROR,
            )
            return

        self.__updateGroups()
        self.__selectGroupItem(newGroupName)

    def __onBeginLabelEdit(self, event):
        item = event.GetItem()
        group = self._groups.GetItemData(item)
        if group is None:
            # Root element
            event.Veto()

    def __onRenameGroup(self, event):
        selItem = self._groups.GetSelection()
        rootItem = self._groups.GetRootItem()

        if selItem.IsOk() and selItem != rootItem:
            self._groups.EditLabel(selItem)

    def __onRemoveGroup(self, event):
        selItem = self._groups.GetSelection()
        rootItem = self._groups.GetRootItem()

        if not selItem.IsOk() or selItem == rootItem:
            return

        groupname = self._groups.GetItemData(selItem)
        assert groupname is not None

        if (
            MessageBox(
                _('Remove group "{}" and all icons inside it?').format(groupname),
                _("Remove group?"),
                wx.YES_NO | wx.ICON_QUESTION,
            )
            == wx.YES
        ):
            try:
                self.__getIconsCollection().removeGroup(groupname)
            except (IOError, SystemError):
                MessageBox(
                    _("Can't remove group directory"), _("Error"), wx.OK | wx.ICON_ERROR
                )
                return
            self.__updateGroups()

    def __onAddIcons(self, event):
        wildcard = "{images}(*.png; *.jpg; *.jpeg; *.gif; *.bmp; *.svg)|*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.svg|*.png|*.png|*.jpg; *.jpeg|*.jpg;*.jpeg|*.gif|*.gif|*.bmp|*.bmp|*.svg|*.svg|{all}(*.*)|*.*".format(
            images=_("All image files"), all=_("All files")
        )
        style = wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST

        with TestedFileDialog(
            self, _("Select images"), wildcard=wildcard, style=style
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                item = self._groups.GetSelection()
                group = self._groups.GetItemData(item)

                collection = self.__getIconsCollection()
                collection.addIcons(group, dlg.GetPaths())
                self.__updateGroups()
                self.__selectGroupItem(group)

    def __onRemoveIcons(self, event):
        icons = self._iconsList.getSelection()
        if not icons:
            MessageBox(
                _("You have not selected any icons"),
                _("Select icons"),
                wx.OK | wx.ICON_INFORMATION,
            )
            return

        if (
            MessageBox(
                _("Remove selected icons?"),
                _("Remove icons"),
                wx.YES_NO | wx.ICON_QUESTION,
            )
            == wx.YES
        ):
            for fname in icons:
                try:
                    os.remove(fname)
                except (IOError, SystemError):
                    pass

            item = self._groups.GetSelection()
            group = self._groups.GetItemData(item)
            self.__updateGroups()
            self.__selectGroupItem(group)

    def __onSetCover(self, event):
        icons = self._iconsList.getSelection()
        if not icons:
            MessageBox(
                _("You have not selected any icons"),
                _("Select icons"),
                wx.OK | wx.ICON_ERROR,
            )
            return

        item = self._groups.GetSelection()
        group = self._groups.GetItemData(item)

        collection = self.__getIconsCollection()
        collection.setCover(group, icons[0])

        self.__updateGroups()
        self.__selectGroupItem(group)

    def __onKeyDown(self, event):
        if (
            event.GetKeyCode() == wx.WXK_F2
            and not event.AltDown()
            and not event.CmdDown()
            and not event.ControlDown()
            and not event.ShiftDown()
        ):
            self.__onRenameGroup(None)
