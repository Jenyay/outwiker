# -*- coding: UTF-8 -*-

import logging
import os
import os.path

import wx
import wx.combo

from outwiker.core.system import getIconsDirList
from outwiker.core.iconscollection import IconsCollection
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT
from outwiker.core.commands import MessageBox
from outwiker.core.events import PageDialogPageIconChangedParams
from outwiker.gui.iconlistctrl import IconListCtrl, EVT_ICON_SELECTED
from outwiker.gui.pagedialogpanels.basecontroller import BasePageDialogController
from outwiker.gui.controls.switchthemed import SwitchThemed, EVT_SWITCH
from outwiker.gui.theme import Theme


class GroupInfo(object):
    def __init__(self, iconscollection, groupname, title):
        self.iconscollection = iconscollection
        self.groupname = groupname
        self.title = title


class IconsPanel(wx.Panel):
    """
    Class of the panel in the "Icon" tab.
    """
    def __init__(self, parent):
        super(IconsPanel, self).__init__(parent)
        self._groupsButtonHeight = 32
        self._groupsMaxWidth = 200
        self._groupsInfo = self._getGroupsInfo()
        self._theme = Theme()
        self._createGui()

        self._appendGroups()
        self.groupCtrl.SetSelection(0)
        self._switchToCurrentGroup()

    def _getGroupsInfo(self):
        result = []

        for n, path in enumerate(getIconsDirList()):
            # First None is root directory
            collection = IconsCollection(path)
            for groupname in [None] + sorted(collection.getGroups(), key=self._localize):
                # Get group name
                if groupname is None:
                    title = _(u'Not in groups')
                else:
                    title = self._localize(groupname)

                if n != 0:
                    title += u' *'

                result.append(GroupInfo(collection, groupname, title))
        
        return result

    def _createGui(self):
        self.iconsList = IconListCtrl(self, theme=self._theme)
        self.iconsList.SetMinSize((200, 150))

        # Control for selection icons group
        self.groupCtrl = SwitchThemed(self, self._theme)
        self.groupCtrl.SetButtonsHeight(self._groupsButtonHeight)
        self.groupCtrl.Bind(EVT_SWITCH, handler=self._onGroupSelect)

        self._layout()

    def _layout(self):
        iconSizer = wx.FlexGridSizer(cols=2)
        iconSizer.AddGrowableRow(0)
        iconSizer.AddGrowableCol(0, 1)
        iconSizer.AddGrowableCol(1, 3)
        iconSizer.Add(self.groupCtrl, 1, wx.ALL | wx.EXPAND, 2)
        iconSizer.Add(self.iconsList, 1, wx.ALL | wx.EXPAND, 2)

        self.SetSizer(iconSizer)
        self.Layout()

    def _appendGroups(self):
        for groupInfo in self._groupsInfo:
            bitmap = self._getCover(groupInfo.iconscollection,
                                    groupInfo.groupname)
            self.groupCtrl.Append(groupInfo.title, bitmap)

        minw, minh = self.groupCtrl.GetMinSize()
        if minw > self._groupsMaxWidth:
            minw = self._groupsMaxWidth

        self.groupCtrl.SetMinSize((minw, minh))

    def _getImageForGroup(self, fname):
        neww = ICON_WIDTH
        newh = ICON_HEIGHT

        wx.Log_EnableLogging(False)
        image = wx.Image(fname)
        wx.Log_EnableLogging(True)

        if not image.IsOk():
            logging.error(_(u'Invalid icon file: {}').format(fname))
            return None

        posx = (neww - image.Width) / 2
        posy = (newh - image.Height) / 2
        image.Resize((neww, newh), (posx, posy), 255, 255, 255)

        return wx.BitmapFromImage(image)

    def _getCover(self, collection, groupname):
        """
        Return bitmap for combobox item
        """
        fname = collection.getCover(groupname)
        if fname is not None:
            return self._getImageForGroup(fname)

        return None

    def _onGroupSelect(self, event):
        self._switchToCurrentGroup()

    def _getCurrentIcons(self):
        index = self.groupCtrl.GetSelection()
        groupInfo = self._groupsInfo[index]

        icons = groupInfo.iconscollection.getIcons(groupInfo.groupname)
        icons.sort()

        return icons

    def _switchToCurrentGroup(self):
        icons = self._getCurrentIcons()
        icons.sort(key=os.path.basename)
        self.iconsList.setIconsList(icons)

    def _localize(self, groupname):
        name = _(groupname)
        return name.capitalize()


class IconsController(BasePageDialogController):
    def __init__(self, iconsPanel, application, dialog):
        super(IconsController, self).__init__(application)
        self._dialog = dialog
        self._iconsPanel = iconsPanel

        self._iconsPanel.iconsList.Bind(EVT_ICON_SELECTED,
                                        handler=self.__onIconSelected)

    @property
    def icon(self):
        selection = self._iconsPanel.iconsList.getSelection()

        assert len(selection) != 0
        icon = selection[0]
        return icon

    def setPageProperties(self, page):
        """
        Return True if success and False otherwise
        """
        icon = self.icon

        # If icon not exists, page may be renamed. Don't will to change icon
        if os.path.exists(icon):
            try:
                page.icon = icon
            except EnvironmentError as e:
                MessageBox(_(u"Can't set page icon\n") + unicode(e),
                           _(u"Error"),
                           wx.ICON_ERROR | wx.OK)
                return False

        return True

    def initBeforeEditing(self, currentPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        icon = currentPage.icon
        if icon is not None:
            self._iconsPanel.iconsList.setCurrentIcon(icon)

    def clear(self):
        self._iconsPanel.iconsList.Unbind(EVT_ICON_SELECTED,
                                          handler=self.__onIconSelected)
        self._dialog = None
        self._iconsPanel = None

    def __onIconSelected(self, event):
        assert len(event.icons) == 1

        eventParams = PageDialogPageIconChangedParams(
            self._dialog,
            event.icons[0])

        self._application.onPageDialogPageIconChanged(
            self._application.selectedPage,
            eventParams)
