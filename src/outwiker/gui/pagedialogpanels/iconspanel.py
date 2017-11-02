# -*- coding: utf-8 -*-

import logging
import os
import os.path

import wx
import wx.combo

from outwiker.core.system import getIconsDirList, getImagesDir
from outwiker.core.iconscollection import IconsCollection
from outwiker.core.recenticonslist import RecentIconsList
from outwiker.core.defines import (ICON_WIDTH,
                                   ICON_HEIGHT,
                                   RECENT_ICONS_COUNT)
from outwiker.core.commands import MessageBox
from outwiker.core.events import (PageDialogPageIconChangedParams,
                                  IconsGroupsListInitParams)
from outwiker.gui.iconlistctrl import IconListCtrl, EVT_ICON_SELECTED
from outwiker.gui.pagedialogpanels.basecontroller import BasePageDialogController
from outwiker.gui.controls.switchthemed import SwitchThemed, EVT_SWITCH
from outwiker.gui.theme import Theme


class IconsGroupInfo(object):
    # Icons group types
    TYPE_BUILTIN = 0
    TYPE_CUSTOM = 1
    TYPE_OTHER = 2

    def __init__(self,
                 iconslist,
                 title,
                 cover,
                 group_type,
                 sort_key=None):
        self.iconslist = iconslist
        self.title = title
        self.cover = cover
        self.group_type = group_type
        self.sort_key = sort_key


class IconsPanel(wx.Panel):
    """
    Class of the panel in the "Icon" tab.
    """
    def __init__(self, parent):
        super(IconsPanel, self).__init__(parent)
        self._groupsButtonHeight = 32
        self._theme = Theme()
        self._createGui()

    def _createGui(self):
        self.iconsList = IconListCtrl(self, theme=self._theme)
        self.iconsList.SetMinSize((200, 150))

        # Control for selection icons group
        self.groupCtrl = SwitchThemed(self, self._theme)
        self.groupCtrl.SetButtonsHeight(self._groupsButtonHeight)

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


class IconsController(BasePageDialogController):
    def __init__(self, iconsPanel, application, dialog):
        super(IconsController, self).__init__(application)
        self._dialog = dialog
        self._iconsPanel = iconsPanel
        self._groupsMaxWidth = 200
        self._page = None

        self._recentIconsList = RecentIconsList(RECENT_ICONS_COUNT,
                                                application.config,
                                                getIconsDirList()[0])
        self._recentIconsList.load()

        self._iconsPanel.iconsList.Bind(EVT_ICON_SELECTED,
                                        handler=self._onIconSelected)
        self._iconsPanel.groupCtrl.Bind(EVT_SWITCH,
                                        handler=self._onGroupSelect)

        self._selectedIcon = None
        self._groupsInfo = self._getGroupsInfo()

        self._appendGroups()
        self._iconsPanel.groupCtrl.SetSelection(0)
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

                iconslist = collection.getIcons(groupname)
                cover = collection.getCover(groupname)
                group_type = (IconsGroupInfo.TYPE_BUILTIN if n == 0
                              else IconsGroupInfo.TYPE_CUSTOM)

                result.append(IconsGroupInfo(iconslist,
                                             title,
                                             cover,
                                             group_type=group_type,
                                             sort_key=os.path.basename))

        self._addRecentIconsGroup(result)
        eventParam = IconsGroupsListInitParams(result)
        self._application.onIconsGroupsListInit(self._page, eventParam)

        return eventParam.groupsList

    def _addRecentIconsGroup(self, group_info_list):
        recent_title = _(u'Recent')
        recent_cover = os.path.join(getImagesDir(), u'recent.png')
        recent_icons = self._recentIconsList.getRecentIcons()
        group_info_list.insert(0, IconsGroupInfo(
            recent_icons,
            recent_title,
            recent_cover,
            group_type=IconsGroupInfo.TYPE_OTHER,
            sort_key=None)
        )

    @property
    def icon(self):
        return self._selectedIcon

    def setPageProperties(self, page):
        """
        Return True if success and False otherwise
        """
        if self.icon is None:
            return True

        icon = os.path.abspath(self.icon)
        self._recentIconsList.add(icon)

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
        self._page = currentPage

        if currentPage.icon is not None:
            self._selectedIcon = os.path.abspath(currentPage.icon)

    def _addCurrentIcon(self):
        if self._selectedIcon is not None:
            self._iconsPanel.iconsList.setCurrentIcon(self._selectedIcon)

    def clear(self):
        self._iconsPanel.iconsList.Unbind(EVT_ICON_SELECTED,
                                          handler=self._onIconSelected)
        self._dialog = None
        self._iconsPanel = None

    def _onIconSelected(self, event):
        assert len(event.icons) == 1

        self._selectedIcon = event.icons[0]

        eventParams = PageDialogPageIconChangedParams(
            self._dialog,
            self._selectedIcon)

        self._application.onPageDialogPageIconChanged(
            self._application.selectedPage,
            eventParams)

    def _localize(self, groupname):
        name = _(groupname)
        return name.capitalize()

    def _appendGroups(self):
        for groupInfo in self._groupsInfo:
            bitmap = self._getCoverBitmap(groupInfo.cover)
            self._iconsPanel.groupCtrl.Append(groupInfo.title, bitmap)

        minw, minh = self._iconsPanel.groupCtrl.GetMinSize()
        if minw > self._groupsMaxWidth:
            minw = self._groupsMaxWidth

        self._iconsPanel.groupCtrl.SetMinSize((minw, minh))

    def _getCoverBitmap(self, fname):
        """
        Return bitmap for combobox item
        """
        if fname is None:
            return None

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

    def _getCurrentIcons(self):
        index = self._iconsPanel.groupCtrl.GetSelection()
        groupInfo = self._groupsInfo[index]

        icons = groupInfo.iconslist
        if groupInfo.sort_key is not None:
            icons.sort(key=groupInfo.sort_key)

        return icons

    def _onGroupSelect(self, event):
        self._switchToCurrentGroup()

    def _switchToCurrentGroup(self):
        icons = self._getCurrentIcons()
        self._iconsPanel.iconsList.setIconsList(icons)
        self._addCurrentIcon()
