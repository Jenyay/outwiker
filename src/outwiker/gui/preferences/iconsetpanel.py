# -*- coding: UTF-8 -*-

import os.path

import wx

from outwiker.core.system import getImagesDir, getIconsDirList
from outwiker.gui.iconlistctrl import IconListCtrl
from outwiker.core.iconscollection import IconsCollection, DuplicateGroupError
from outwiker.core.commands import MessageBox
from outwiker.gui.testeddialog import TestedFileDialog
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT


class IconsetPanel (wx.Panel):
    def __init__ (self, *args, **kwds):
        kwds["style"] = wx.TAB_TRAVERSAL
        super (IconsetPanel, self).__init__ (*args, **kwds)

        self.ADD_GROUP = wx.NewId()
        self.REMOVE_GROUP = wx.NewId()
        self.RENAME_GROUP = wx.NewId()

        self.ADD_ICONS = wx.NewId()
        self.REMOVE_ICONS = wx.NewId()
        self.SET_COVER = wx.NewId()

        self.__createGuiElements()

        self._groups.Bind (wx.EVT_TREE_SEL_CHANGED, handler=self.__onGroupSelect)
        self._groups.Bind (wx.EVT_TREE_BEGIN_LABEL_EDIT, self.__onBeginLabelEdit)
        self._groups.Bind (wx.EVT_TREE_END_LABEL_EDIT, self.__onEndLabelEdit)

        self.Bind(wx.EVT_MENU, handler=self.__onAddGroup, id=self.ADD_GROUP)
        self.Bind(wx.EVT_MENU, handler=self.__onRenameGroup, id=self.RENAME_GROUP)
        self.Bind(wx.EVT_MENU, handler=self.__onRemoveGroup, id=self.REMOVE_GROUP)

        self.Bind(wx.EVT_MENU, handler=self.__onAddIcons, id=self.ADD_ICONS)
        self.Bind(wx.EVT_MENU, handler=self.__onRemoveIcons, id=self.REMOVE_ICONS)
        self.Bind(wx.EVT_MENU, handler=self.__onSetCover, id=self.SET_COVER)

        self._groups.Bind (wx.EVT_KEY_DOWN, handler=self.__onKeyDown)

        self.__updateGroups()


    def __fillGroupsToolbar (self):
        imagesDir = getImagesDir()

        self._groupsToolbar.AddLabelTool(
            self.ADD_GROUP,
            _(u"Add new group"),
            wx.Bitmap(os.path.join (imagesDir, "add.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Add new group"),
            "")

        self._groupsToolbar.AddLabelTool(
            self.REMOVE_GROUP,
            _(u"Remove group"),
            wx.Bitmap(os.path.join (imagesDir, "remove.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Remove group"),
            "")

        self._groupsToolbar.AddLabelTool(
            self.RENAME_GROUP,
            _(u"Rename group"),
            wx.Bitmap(os.path.join (imagesDir, "pencil.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Rename group"),
            "")


    def __fillIconsToolbar (self):
        imagesDir = getImagesDir()

        self._iconsToolbar.AddLabelTool(
            self.ADD_ICONS,
            _(u"Add icons"),
            wx.Bitmap(os.path.join (imagesDir, "add.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Add icons"),
            "")

        self._iconsToolbar.AddLabelTool(
            self.REMOVE_ICONS,
            _(u"Remove selected icons"),
            wx.Bitmap(os.path.join (imagesDir, "remove.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Remove selected icons"),
            "")

        self._iconsToolbar.AddLabelTool(
            self.SET_COVER,
            _(u"Set icon as group cover"),
            wx.Bitmap(os.path.join (imagesDir, "picture.png"), wx.BITMAP_TYPE_ANY),
            wx.NullBitmap,
            wx.ITEM_NORMAL,
            _(u"Set icon as group cover"),
            "")


    def __createGuiElements (self):
        mainSizer = wx.FlexGridSizer (cols=2, rows=1)
        mainSizer.AddGrowableCol (1)
        mainSizer.AddGrowableRow (0)

        #
        # Controls for groups
        groupsSizer = wx.FlexGridSizer (cols=1)
        groupsSizer.AddGrowableCol (0)
        groupsSizer.AddGrowableRow (0)

        self._groups = wx.TreeCtrl (
            self,
            style = wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.SUNKEN_BORDER)
        self._groups.SetMinSize ((200, -1))

        self._imagelist = wx.ImageList(ICON_WIDTH, ICON_HEIGHT)
        self._groups.AssignImageList (self._imagelist)

        # Toolbar for groups
        self._groupsToolbar = wx.ToolBar (
            self,
            -1,
            style = wx.TB_HORIZONTAL | wx.TB_FLAT)

        self.__fillGroupsToolbar()

        groupsSizer.Add (self._groups, 1, wx.RIGHT | wx.EXPAND, border = 2)
        groupsSizer.Add (self._groupsToolbar, 1, wx.RIGHT | wx.EXPAND, border = 2)

        #
        # Controls for icons in the group
        iconsSizer = wx.FlexGridSizer (cols=1)
        iconsSizer.AddGrowableRow (0)
        iconsSizer.AddGrowableCol (0)

        self._iconsList = IconListCtrl (self, True)

        # Toolbar for icons in the group
        self._iconsToolbar = wx.ToolBar (
            self,
            -1,
            style = wx.TB_HORIZONTAL | wx.TB_FLAT)

        self.__fillIconsToolbar()
        iconsSizer.Add (self._iconsList, 1, wx.LEFT | wx.EXPAND, border = 2)
        iconsSizer.Add (self._iconsToolbar, 1, wx.LEFT | wx.EXPAND, border = 2)

        # Main sizer
        mainSizer.Add (groupsSizer, 1, wx.ALL | wx.EXPAND, border = 0)
        mainSizer.Add (iconsSizer, 1, wx.ALL | wx.EXPAND, border = 0)

        self.SetSizer (mainSizer)
        self.Layout()


    def Save (self):
        pass


    def LoadState (self):
        pass


    def __updateGroups (self):
        self._groups.DeleteAllItems()
        self._imagelist.RemoveAll()

        collection = self.__getIconsCollection()

        # Add the root element
        rootimage = collection.getCover (None)
        imageIndex = -1 if rootimage is None else self._imagelist.Add (wx.Bitmap (rootimage))
        rootItem = self._groups.AddRoot (_(u"Not in groups"), imageIndex)

        # Add child groups
        for group in collection.getGroups():
            image = collection.getCover (group)
            imageIndex = -1 if image is None else self._imagelist.Add (wx.Bitmap (image))

            self._groups.AppendItem (rootItem, group, imageIndex, data = wx.TreeItemData(group))

        self._groups.Expand (rootItem)
        self._groups.SelectItem (rootItem)
        self.__onGroupSelect (None)


    def __getIconsCollection (self):
        return IconsCollection (getIconsDirList()[-1])


    def __showIcons (self, groupname):
        """
        Show icons from group groupname.
        If groupname is None then icons from root will be showned
        """
        self._iconsList.clear()
        collection = self.__getIconsCollection()
        icons = collection.getIcons(groupname)
        self._iconsList.setIconsList (icons)


    def __onGroupSelect (self, event):
        """
        User select other group
        """
        selItem = self._groups.GetSelection()
        if not selItem.IsOk():
            return

        group = self._groups.GetItemData (selItem).GetData()
        self.__showIcons (group)


    def __onAddGroup (self, event):
        collection = self.__getIconsCollection()
        newGroupName = self.__getNewGroupName (collection.getGroups())
        try:
            collection.addGroup (newGroupName)
            self.__updateGroups()
            self.__selectGroupItem (newGroupName)
        except (IOError, SystemError):
            MessageBox (
                _(u"Can't create directory for icons group"),
                _(u"Error"),
                wx.OK | wx.ICON_ERROR)


    def __selectGroupItem (self, groupname):
        """
        Select group in _groups tree. If groupname is None then select root element.
        If groupname not exists then method does nothing.
        """
        rootItem = self._groups.GetRootItem()
        assert rootItem.IsOk()

        if groupname is None:
            self._groups.SelectItem (rootItem)

        nextGroupItem, cookie = self._groups.GetFirstChild (rootItem)

        while nextGroupItem.IsOk():
            if self._groups.GetItemData(nextGroupItem).GetData() == groupname:
                self._groups.SelectItem (nextGroupItem)
                break

            nextGroupItem, cookie = self._groups.GetNextChild (rootItem, cookie)


    def __getNewGroupName (self, groups):
        """
        Return name for new group
        """
        newGroupTemplate = _(u"New group{}")
        newGroupName = newGroupTemplate.format (u"")
        if newGroupName in groups:
            # Generate new group name in format "New group (1)", "New group (2)" etc
            index = 0
            while newGroupName in groups:
                index += 1
                newGroupName = newGroupTemplate.format (u" ({})".format (index))
        return newGroupName


    def __onEndLabelEdit (self, event):
        if event.IsEditCancelled():
            return

        event.Veto()
        oldGroupName = self._groups.GetItemData (event.GetItem()).GetData()
        newGroupName = event.GetLabel().strip()

        assert oldGroupName is not None

        collection = self.__getIconsCollection()

        try:
            collection.renameGroup (oldGroupName, newGroupName)
        except (IOError, SystemError):
            MessageBox (
                _(u"Can't rename directory for icons group"),
                _(u"Error"),
                wx.OK | wx.ICON_ERROR)
            return
        except DuplicateGroupError:
            MessageBox (
                _(u'Group with name "{}" exists already').format (newGroupName),
                _(u"Error"),
                wx.OK | wx.ICON_ERROR)
            return
        except ValueError:
            MessageBox (
                _(u'Invalid group name "{}"').format (newGroupName),
                _(u"Error"),
                wx.OK | wx.ICON_ERROR)
            return

        self.__updateGroups()
        self.__selectGroupItem (newGroupName)


    def __onBeginLabelEdit (self, event):
        item = event.GetItem()
        group = self._groups.GetItemData (item).GetData()
        if group is None:
            # Root element
            event.Veto()


    def __onRenameGroup (self, event):
        selItem = self._groups.GetSelection()
        rootItem = self._groups.GetRootItem()

        if selItem.IsOk() and selItem != rootItem:
            self._groups.EditLabel (selItem)


    def __onRemoveGroup (self, event):
        selItem = self._groups.GetSelection()
        rootItem = self._groups.GetRootItem()

        if not selItem.IsOk() or selItem == rootItem:
            return

        groupname = self._groups.GetItemData(selItem).GetData()
        assert groupname is not None

        if MessageBox (
                _(u'Remove group "{}" and all icons inside it?').format (groupname),
                _(u"Remove group?"),
                wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            try:
                self.__getIconsCollection ().removeGroup (groupname)
            except (IOError, SystemError):
                MessageBox (
                    _(u"Can't remove group directory"),
                    _(u"Error"),
                    wx.OK | wx.ICON_ERROR)
                return
            self.__updateGroups()


    def __onAddIcons (self, event):
        wildcard = u"{images} (*.png; *.jpg; *.jpeg; *.gif; *.bmp)|*.png; *.jpg; *.jpeg; *.gif; *.bmp|*.png|*.png|*.jpg; *.jpeg|*.jpg;*.jpeg|*.gif|*.gif|*.bmp|*.bmp|{all} (*.*)|*.*".format (
            images = _(u"All image files"),
            all = _(u"All files"))
        style = wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST

        with TestedFileDialog (
                self,
                _(u"Select images"),
                wildcard = wildcard,
                style = style) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                item = self._groups.GetSelection ()
                group = self._groups.GetItemData (item).GetData()

                collection = self.__getIconsCollection()
                collection.addIcons (group, dlg.GetPaths())
                self.__updateGroups()
                self.__selectGroupItem (group)


    def __onRemoveIcons (self, event):
        icons = self._iconsList.getSelection()
        if not icons:
            MessageBox (
                _(u"You have not selected any icons"),
                _(u"Select icons"),
                wx.OK | wx.ICON_INFORMATION)
            return

        if MessageBox (
                _(u"Remove selected icons?"),
                _(u"Remove icons"),
                wx.YES_NO | wx.ICON_QUESTION) == wx.YES:
            for fname in icons:
                try:
                    os.remove (fname)
                except (IOError, SystemError):
                    pass

            item = self._groups.GetSelection ()
            group = self._groups.GetItemData (item).GetData()
            self.__updateGroups()
            self.__selectGroupItem (group)


    def __onSetCover (self, event):
        icons = self._iconsList.getSelection()
        if not icons:
            MessageBox (
                _(u"You have not selected any icons"),
                _(u"Select icons"),
                wx.OK | wx.ICON_ERROR)
            return

        item = self._groups.GetSelection ()
        group = self._groups.GetItemData (item).GetData()

        collection = self.__getIconsCollection()
        collection.setCover (group, icons[0])

        self.__updateGroups()
        self.__selectGroupItem (group)


    def __onKeyDown (self, event):
        if (event.GetKeyCode() == wx.WXK_F2 and
                not event.AltDown() and
                not event.CmdDown() and
                not event.ControlDown() and
                not event.ShiftDown()):
            self.__onRenameGroup (None)
