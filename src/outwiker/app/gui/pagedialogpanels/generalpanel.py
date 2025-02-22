# -*- coding: utf-8 -*-

import logging
import os
import os.path
from datetime import datetime
from typing import List, Callable

import wx

import outwiker.core.factory as ocf

from outwiker.app.gui.pagedialogpanels.iconslistpopup import IconsListPopup

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import BasePage
from outwiker.core.events import (
    PageDialogPageTypeChangedParams,
    PageDialogPageTitleChangedParams,
    PageDialogPageTagsChangedParams,
    PageDialogPageFactoriesNeededParams,
    PageDialogNewPageOrderChangedParams,
)
from outwiker.core.system import getIconsDirList, getBuiltinImagePath
from outwiker.core.recenticonslist import RecentIconsList
from outwiker.core.defines import ICON_DEFAULT
from outwiker.core.events import (
    PageDialogPageIconChangedParams,
    IconsGroupsListInitParams,
)
from outwiker.gui.defines import ICONS_HEIGHT, ICONS_WIDTH
from outwiker.gui.iconscollection import IconsCollection
from outwiker.gui.images import readImage
from outwiker.gui.tagsselector import TagsSelector, EVT_TAGS_LIST_CHANGED
from outwiker.gui.guiconfig import PageDialogConfig, GeneralGuiConfig, TagsConfig
from outwiker.gui.pagedialogpanels.basecontroller import BasePageDialogController
from outwiker.gui.controls.switchthemed import EVT_SWITCH
from outwiker.gui.iconlistctrl import EVT_ICON_SELECTED, EVT_ICON_DOUBLE_CLICK
from outwiker.gui.dialogs.messagebox import MessageBox
from outwiker.gui.theme import Theme


class IconsGroupInfo:
    # Icons group types
    TYPE_BUILTIN = 0
    TYPE_CUSTOM = 1
    TYPE_OTHER = 2

    def __init__(self, iconslist, title, cover, group_type, sort_key=None):
        self.iconslist = iconslist
        self.title = title
        self.cover = cover
        self.group_type = group_type
        self.sort_key = sort_key


class GeneralPanel(wx.Panel):
    """
    Класс панели, расположенной на вкладке "Общее"
    """

    def __init__(self, parent, theme: Theme):
        super().__init__(parent)
        self._theme = theme
        self._POPUP_WIDTH = 500
        self._POPUP_HEIGHT = 350

        self.__createGeneralControls()
        self.__layout()

    def __layout(self):
        # Page title
        titleSizer = wx.FlexGridSizer(cols=3)
        titleSizer.AddGrowableCol(1)
        titleSizer.Add(
            self.titleLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4
        )
        titleSizer.Add(self.titleTextCtrl, flag=wx.ALL | wx.EXPAND, border=4)
        titleSizer.Add(self.iconBtn, flag=wx.ALL | wx.ALIGN_RIGHT, border=4)

        # Page type
        typeSizer = wx.FlexGridSizer(cols=2)
        typeSizer.AddGrowableCol(1)
        typeSizer.Add(self.typeLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4)
        typeSizer.Add(self.typeCombo, flag=wx.ALL | wx.EXPAND, border=4)

        # Page order
        self.orderSizer = wx.FlexGridSizer(cols=2)
        self.orderSizer.AddGrowableCol(1)
        self.orderSizer.Add(
            self.orderLabel, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=4
        )
        self.orderSizer.Add(self.orderCombo, flag=wx.ALL | wx.EXPAND, border=4)

        generalSizer = wx.FlexGridSizer(cols=1)
        generalSizer.AddGrowableRow(3)
        generalSizer.AddGrowableCol(0)
        generalSizer.Add(titleSizer, flag=wx.EXPAND)
        generalSizer.Add(typeSizer, flag=wx.EXPAND)
        generalSizer.Add(self.orderSizer, flag=wx.EXPAND)
        generalSizer.Add(self.tagsSelector, flag=wx.EXPAND)

        self.SetSizer(generalSizer)
        self.Layout()

    def __createGeneralControls(self):
        # Page title
        self.titleLabel = wx.StaticText(self, label=_("Title"))
        self.titleTextCtrl = wx.TextCtrl(self, value="")
        self.titleTextCtrl.SetMinSize((350, -1))

        # Page icon
        self.iconBtn = wx.BitmapButton(self)
        self.iconBtn.SetMinSize((40, -1))
        self.iconBtn.SetToolTip(_("Page icon"))
        self.iconsPopup = IconsListPopup(self, self._theme)
        self.iconsPopup.SetSize((self._POPUP_WIDTH, self._POPUP_HEIGHT))

        # Page type
        self.typeLabel = wx.StaticText(self, label=_("Page type"))
        self.typeCombo = wx.ComboBox(
            self, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY
        )

        # Page order
        self.orderLabel = wx.StaticText(self, label=_("New page position"))
        self.orderCombo = wx.ComboBox(
            self, choices=[], style=wx.CB_DROPDOWN | wx.CB_READONLY
        )

        # Tags
        self.tagsSelector = TagsSelector(self)

    def popupIconsList(self):
        self.iconsPopup.Popup(self)

    def closeIconsList(self):
        self.iconsPopup.Hide()

    @property
    def pageTitle(self):
        return self.titleTextCtrl.GetValue()

    @pageTitle.setter
    def pageTitle(self, value):
        self.titleTextCtrl.SetValue(value)

    def setPageIcon(self, iconFileName):
        bitmap = readImage(iconFileName, ICONS_WIDTH, ICONS_HEIGHT)
        self.iconBtn.SetBitmapLabel(bitmap)


class GeneralController(BasePageDialogController):
    def __init__(self, generalPanel, application, dialog):
        super().__init__(application)
        self._dialog = dialog
        self._generalPanel = generalPanel
        self._config = PageDialogConfig(self._application.config)
        self._tagsConfig = TagsConfig(self._application.config)
        self._iconsController = IconsController(
            self._generalPanel.iconsPopup.iconsPanel,
            self._generalPanel,
            application,
            self._dialog,
        )

        self._orderCalculators = [
            (ocf.orderCalculatorTop, _("Top of the list")),
            (ocf.orderCalculatorBottom, _("End of the list")),
            (ocf.orderCalculatorAlphabetically, _("Alphabetically")),
        ]

        self._setTagsList()

        self._generalPanel.typeCombo.Bind(
            wx.EVT_COMBOBOX, handler=self.__onPageTypeChanged
        )

        self._generalPanel.titleTextCtrl.Bind(
            wx.EVT_TEXT, handler=self.__onPageTitleChanged
        )

        self._generalPanel.orderCombo.Bind(
            wx.EVT_COMBOBOX, handler=self.__onPageOrderChanged
        )

        self._generalPanel.tagsSelector.Bind(
            EVT_TAGS_LIST_CHANGED, handler=self.__onTagsListChanged
        )

        self._generalPanel.iconBtn.Bind(wx.EVT_BUTTON, handler=self.__onIconButtonClick)

    def __onIconButtonClick(self, event):
        self._generalPanel.popupIconsList()

    @property
    def pageTitle(self) -> str:
        return self._generalPanel.titleTextCtrl.GetValue().strip()

    @pageTitle.setter
    def pageTitle(self, value: str):
        self._generalPanel.titleTextCtrl.SetValue(value)

    @property
    def selectedFactory(self):
        index = self._generalPanel.typeCombo.GetSelection()
        return self._generalPanel.typeCombo.GetClientData(index)

    @property
    def tags(self) -> List[str]:
        return self._generalPanel.tagsSelector.tags

    @tags.setter
    def tags(self, value: List[str]):
        self._generalPanel.tagsSelector.tags = value

    @property
    def orderCalculator(self) -> Callable[[BasePage, str, List[str]], int]:
        index = self._generalPanel.orderCombo.GetSelection()
        return self._orderCalculators[index][0]

    def setPageProperties(self, page):
        """
        Return True if success and False otherwise
        """
        page.tags = self.tags
        return self._iconsController.setPageProperties(page)

    def saveParams(self):
        self._config.recentCreatedPageType.value = self.selectedFactory.getPageTypeString()
        self._config.newPageOrderCalculator.value = (
            self._generalPanel.orderCombo.GetSelection()
        )

    def initBeforeCreation(self, parentPage):
        """
        Initialize the panel before new page creation
        parentPage - the parent page for new page
        """
        self._iconsController.initBeforeCreation(parentPage)
        self._fillComboType(None)
        self._fillComboOrderCalculators()

        if parentPage.parent is not None:
            self.tags = parentPage.tags

        # Опция для хранения типа страницы, которая была создана последней
        lastCreatedPageType = self._config.recentCreatedPageType.value
        self._setComboPageType(lastCreatedPageType)

        title = self._getDefaultTitle()
        self._generalPanel.titleTextCtrl.SetValue(title)
        self._generalPanel.titleTextCtrl.SelectAll()
        self._generalPanel.orderSizer.ShowItems(True)
        self._generalPanel.Layout()

        self.__onPageTypeChanged(None)

    def _getDefaultTitle(self):
        config = GeneralGuiConfig(self._application.config)
        template = config.pageTitleTemplate.value
        title = datetime.now().strftime(template)
        return title

    def initBeforeEditing(self, currentPage):
        """
        Initialize the panel before new page editing.
        page - page for editing
        """
        self._iconsController.initBeforeEditing(currentPage)
        self._fillComboType(currentPage)
        self._generalPanel.titleTextCtrl.SetSelection(-1, -1)

        self.tags = currentPage.tags

        self._generalPanel.titleTextCtrl.SetValue(currentPage.display_title)

        # Установить тип страницы
        self._setComboPageType(currentPage.getTypeString())
        self._generalPanel.typeCombo.Disable()
        self._generalPanel.orderSizer.ShowItems(False)
        self._generalPanel.Layout()
        self.__onPageTypeChanged(None)

    def validateBeforeCreation(self, _parentPage):
        return True

    def validateBeforeEditing(self, _page):
        return True

    def clear(self):
        self._generalPanel.typeCombo.Unbind(
            wx.EVT_COMBOBOX, handler=self.__onPageTypeChanged
        )

        self._generalPanel.titleTextCtrl.Unbind(
            wx.EVT_TEXT, handler=self.__onPageTitleChanged
        )

        self._generalPanel.orderCombo.Unbind(
            wx.EVT_COMBOBOX, handler=self.__onPageOrderChanged
        )

        self._generalPanel.tagsSelector.Unbind(
            EVT_TAGS_LIST_CHANGED, handler=self.__onTagsListChanged
        )
        self._dialog = None

    def _fillComboType(self, currentPage):
        """
        currentPage - page for edit or None if dialog opened
            for creation a page
        """
        eventParams = PageDialogPageFactoriesNeededParams(self._dialog, currentPage)
        self._application.onPageDialogPageFactoriesNeeded(
            self._application.selectedPage, eventParams
        )

        self._generalPanel.typeCombo.Clear()
        for factory in eventParams.pageFactories:
            self._generalPanel.typeCombo.Append(factory.title, factory)

        if not self._generalPanel.typeCombo.IsEmpty():
            self._generalPanel.typeCombo.SetSelection(0)

    def _fillComboOrderCalculators(self):
        orderTitles = [item[1] for item in self._orderCalculators]
        self._generalPanel.orderCombo.SetItems(orderTitles)
        order = self._config.newPageOrderCalculator.value

        if order >= 0 and order < len(self._orderCalculators):
            self._generalPanel.orderCombo.SetSelection(order)
        else:
            self._generalPanel.orderCombo.SetSelection(1)

    def _setTagsList(self):
        assert self._application.wikiroot is not None

        tagslist = TagsList(self._application.wikiroot)
        self._generalPanel.tagsSelector.setFontSize(
            self._tagsConfig.minFontSize.value, self._tagsConfig.maxFontSize.value
        )
        self._generalPanel.tagsSelector.setMode(self._tagsConfig.tagsCloudMode.value)
        self._generalPanel.tagsSelector.enableTooltips(
            self._tagsConfig.enableTooltips.value
        )
        self._generalPanel.tagsSelector.setTagsList(tagslist)

    def _setComboPageType(self, pageTypeString):
        """
        Установить тип страницы в диалоге по строке, описывающей тип страницы
        """
        typeCombo = self._generalPanel.typeCombo
        for n in range(typeCombo.GetCount()):
            if typeCombo.GetClientData(n).getPageTypeString() == pageTypeString:
                typeCombo.SetSelection(n)

    def __onPageTypeChanged(self, event):
        eventParams = PageDialogPageTypeChangedParams(
            self._dialog, self.selectedFactory.getPageTypeString()
        )

        self._application.onPageDialogPageTypeChanged(
            self._application.selectedPage, eventParams
        )

    def __onPageTitleChanged(self, event):
        eventParams = PageDialogPageTitleChangedParams(self._dialog, self.pageTitle)

        self._application.onPageDialogPageTitleChanged(
            self._application.selectedPage, eventParams
        )

    def __onPageOrderChanged(self, event):
        eventParams = PageDialogNewPageOrderChangedParams(
            self._dialog, self.orderCalculator
        )

        self._application.onPageDialogNewPageOrderChanged(
            self._application.selectedPage, eventParams
        )

    def __onTagsListChanged(self, event):
        eventParams = PageDialogPageTagsChangedParams(self._dialog, self.tags)

        self._application.onPageDialogPageTagsChanged(
            self._application.selectedPage, eventParams
        )


class IconsController(BasePageDialogController):
    def __init__(self, iconsPanel, generalPanel, application, dialog):
        super().__init__(application)
        self._dialog = dialog
        self._iconsPanel = iconsPanel
        self._generalPanel = generalPanel
        self._groupsMaxWidth = 200
        self._page = None
        self._default_group_cover = getBuiltinImagePath("icons_cover_default.svg")
        self._default_icon_filename = os.path.abspath(
            os.path.join(getIconsDirList()[0], ICON_DEFAULT)
        )

        guiconfig = GeneralGuiConfig(application.config)

        self._recentIconsList = RecentIconsList(
            guiconfig.iconsHistoryLength.value, application.config, getIconsDirList()[0]
        )

        self._recentIconsList.load()

        self._iconsPanel.iconsList.Bind(EVT_ICON_SELECTED, handler=self._onIconSelected)
        self._iconsPanel.iconsList.Bind(
            EVT_ICON_DOUBLE_CLICK, handler=self._onIconDoubleClick
        )
        self._iconsPanel.groupCtrl.Bind(EVT_SWITCH, handler=self._onGroupSelect)

        self._selectedIcon = self._default_icon_filename
        self._groupsInfo = self._getGroupsInfo()

        self._appendGroups()
        group_index = 0 if len(self._recentIconsList) else 1
        self._iconsPanel.groupCtrl.SetSelection(group_index)

    def _getGroupsInfo(self):
        result = []

        for n, path in enumerate(getIconsDirList()):
            # First None is root directory
            collection = IconsCollection(path)
            for groupname in [None] + sorted(
                collection.getGroups(), key=self._localize
            ):
                # Get group name
                if groupname is None:
                    title = _("Not in groups")
                else:
                    title = self._localize(groupname)

                iconslist = collection.getIcons(groupname)
                cover = collection.getCover(groupname)
                if cover is None:
                    cover = self._default_group_cover

                group_type = (
                    IconsGroupInfo.TYPE_BUILTIN
                    if n == 0
                    else IconsGroupInfo.TYPE_CUSTOM
                )

                result.append(
                    IconsGroupInfo(
                        iconslist,
                        title,
                        cover,
                        group_type=group_type,
                        sort_key=os.path.basename,
                    )
                )

        self._addRecentIconsGroup(result)
        eventParam = IconsGroupsListInitParams(result)
        self._application.onIconsGroupsListInit(self._page, eventParam)

        return eventParam.groupsList

    def _addRecentIconsGroup(self, group_info_list):
        recent_title = _("Recent")
        recent_cover = getBuiltinImagePath("recent.png")
        recent_icons = self._recentIconsList.getRecentIcons()
        group_info_list.insert(
            0,
            IconsGroupInfo(
                recent_icons,
                recent_title,
                recent_cover,
                group_type=IconsGroupInfo.TYPE_OTHER,
                sort_key=None,
            ),
        )

    @property
    def icon(self):
        return (
            self._selectedIcon
            if self._selectedIcon != self._default_icon_filename
            else None
        )

    def setPageProperties(self, page):
        """
        Return True if success and False otherwise
        """
        icon_filename = os.path.abspath(self.icon) if self.icon is not None else None

        if (page.icon is not None and icon_filename == os.path.abspath(page.icon)) or (
            page.icon is None and icon_filename is None
        ):
            # Icon was not changed
            return True

        if icon_filename is not None:
            self._recentIconsList.add(icon_filename)

        # If icon_filename not exists, page may be renamed. Don't will to change icon
        if icon_filename is None or os.path.exists(icon_filename):
            try:
                page.icon = icon_filename
            except EnvironmentError as e:
                MessageBox(
                    _("Can't set page icon\n") + str(e),
                    _("Error"),
                    wx.ICON_ERROR | wx.OK,
                )
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
            for n, group_info in enumerate(self._groupsInfo[1:]):
                if self._selectedIcon in group_info.iconslist:
                    self._iconsPanel.groupCtrl.SetSelection(n + 1)
                    break

    def _addCurrentIcon(self):
        self._iconsPanel.iconsList.setCurrentIcon(self._selectedIcon)

    def clear(self):
        self._iconsPanel.iconsList.Unbind(
            EVT_ICON_SELECTED, handler=self._onIconSelected
        )
        self._iconsPanel.iconsList.Unbind(
            EVT_ICON_DOUBLE_CLICK, handler=self._onIconDoubleClick
        )
        self._dialog = None
        self._iconsPanel = None

    def _onIconSelected(self, event):
        assert len(event.icons) == 1

        self._selectedIcon = event.icons[0]
        self._generalPanel.setPageIcon(self._selectedIcon)

        eventParams = PageDialogPageIconChangedParams(self._dialog, self._selectedIcon)

        self._application.onPageDialogPageIconChanged(
            self._application.selectedPage, eventParams
        )

    def _onIconDoubleClick(self, event):
        self._onIconSelected(event)
        self._generalPanel.closeIconsList()

    def _localize(self, groupname):
        name = _(groupname)
        return name.capitalize()

    def _appendGroups(self):
        for index, groupInfo in enumerate(self._groupsInfo):
            bitmap = self._getCoverBitmap(groupInfo.cover)
            if (
                index != 0
                and groupInfo.group_type != self._groupsInfo[index - 1].group_type
            ):
                self._iconsPanel.groupCtrl.AppendSeparator()
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

        neww = ICONS_WIDTH
        newh = ICONS_HEIGHT

        wx.Log.EnableLogging(False)
        image = readImage(fname, ICONS_WIDTH, ICONS_HEIGHT).ConvertToImage()
        wx.Log.EnableLogging(True)

        if not image.IsOk():
            logging.error("Invalid icon file: %s", fname)
            return None

        posx = (neww - image.Width) // 2
        posy = (newh - image.Height) // 2
        image.Resize((neww, newh), (posx, posy), 255, 255, 255)

        return wx.Bitmap(image)

    def _getCurrentIcons(self):
        index = self._iconsPanel.groupCtrl.GetSelection()
        groupInfo = self._groupsInfo[index]

        icons = groupInfo.iconslist
        if groupInfo.sort_key is not None:
            icons.sort(key=groupInfo.sort_key)

        return icons

    def _onGroupSelect(self, event):
        self._updateCurrentGroup()

    def _updateCurrentGroup(self):
        icons = self._getCurrentIcons()
        self._iconsPanel.iconsList.setIconsList(icons)
        self._addCurrentIcon()
