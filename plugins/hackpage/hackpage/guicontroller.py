# -*- coding: utf-8 -*-

import wx

from outwiker.api.gui.defines import MENU_TOOLS

from hackpage.i18n import get_
from hackpage.actions.changeuid import ChangeUIDAction
from hackpage.actions.setalias import SetAliasAction
from hackpage.actions.changepagefolder import ChangePageFolderAction
from hackpage.actions.changepagecreationdate import ChangePageCreationDateAction
from hackpage.actions.changepagechangedate import ChangePageChangeDateAction
from hackpage.utils import (
    changeUidWithDialog,
    setAliasWithDialog,
    setPageFolderWithDialog,
    setPageCreationDate,
    setPageChangeDate,
)


class GuiController:
    """
    Создание элементов интерфейса с использованием actions
    """

    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

        # All actions list
        self._actions = [
            ChangeUIDAction,
            SetAliasAction,
            ChangePageFolderAction,
            ChangePageCreationDateAction,
            ChangePageChangeDateAction,
        ]

        global _
        _ = get_()

        self._mainSubmenuItem = None

        # Pointer to clicked page
        self._selectedPage = None

        self._popupSubmenu = None

    def _bind(self):
        self._application.onTreePopupMenu += self.__onTreePopupMenu

    def _unbind(self):
        self._application.onTreePopupMenu -= self.__onTreePopupMenu

    def initialize(self):
        self._bind()

        if self._application.mainWindow is not None:
            list(
                map(
                    lambda action: self._application.actionController.register(
                        action(self._application, self._controller), None
                    ),
                    self._actions,
                )
            )

            self.createTools()

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        menu_tools = mainWindow.menuController[MENU_TOOLS]
        # Menu for action
        menu = wx.Menu()
        self._mainSubmenuItem = menu_tools.AppendSubMenu(menu, "HackPage")

        list(
            map(
                lambda action: self._application.actionController.appendMenuItem(
                    action.stringId, menu
                ),
                self._actions,
            )
        )

    def destroy(self):
        self._unbind()
        actionController = self._application.actionController
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            menu_tools = mainWindow.menuController[MENU_TOOLS]
            [
                *map(
                    lambda action: actionController.removeAction(action.stringId),
                    self._actions,
                )
            ]
            menu_tools.Remove(self._mainSubmenuItem)
            self._mainSubmenuItem = None

    def __onTreePopupMenu(self, menu, page):
        self._selectedPage = page

        self._popupSubmenu = wx.Menu()
        changePageUIDMenuItem = self._popupSubmenu.Append(
            wx.ID_ANY, _("Change page identifier...")
        )

        setPageAliasMenuItem = self._popupSubmenu.Append(
            wx.ID_ANY, _("Set page alias...")
        )

        setPageFolderMenuItem = self._popupSubmenu.Append(
            wx.ID_ANY, _("Change page folder...")
        )

        setPageCreationDateMenuItem = self._popupSubmenu.Append(
            wx.ID_ANY, _("Change page creation date and time...")
        )

        setPageChangeDateMenuItem = self._popupSubmenu.Append(
            wx.ID_ANY, _("Change date and time of change of the page...")
        )

        menu.AppendSubMenu(self._popupSubmenu, "HackPage")

        self._application.mainWindow.Bind(
            wx.EVT_MENU, self.__onChangePageUIDPopupClick, changePageUIDMenuItem
        )

        self._application.mainWindow.Bind(
            wx.EVT_MENU, self.__onSetPageAliasPopupClick, setPageAliasMenuItem
        )

        self._application.mainWindow.Bind(
            wx.EVT_MENU, self.__onSetPageFolderPopupClick, setPageFolderMenuItem
        )

        self._application.mainWindow.Bind(
            wx.EVT_MENU,
            self.__onSetPageCreationDatePopupClick,
            setPageCreationDateMenuItem,
        )

        self._application.mainWindow.Bind(
            wx.EVT_MENU, self.__onSetPageChangeDatePopupClick, setPageChangeDateMenuItem
        )

    def __onChangePageUIDPopupClick(self, event):
        assert self._selectedPage is not None
        changeUidWithDialog(self._selectedPage, self._application)
        self._unbindPopupMenu()
        self._selectedPage = None

    def __onSetPageAliasPopupClick(self, event):
        assert self._selectedPage is not None
        setAliasWithDialog(self._selectedPage, self._application)
        self._unbindPopupMenu()
        self._selectedPage = None

    def __onSetPageFolderPopupClick(self, event):
        assert self._selectedPage is not None
        setPageFolderWithDialog(self._selectedPage, self._application)
        self._unbindPopupMenu()
        self._selectedPage = None

    def __onSetPageCreationDatePopupClick(self, event):
        assert self._selectedPage is not None
        setPageCreationDate(self._selectedPage, self._application)
        self._unbindPopupMenu()
        self._selectedPage = None

    def __onSetPageChangeDatePopupClick(self, event):
        assert self._selectedPage is not None
        setPageChangeDate(self._selectedPage, self._application)
        self._unbindPopupMenu()
        self._selectedPage = None

    def _unbindPopupMenu(self):
        self._application.mainWindow.Unbind(
            wx.EVT_MENU, handler=self.__onSetPageFolderPopupClick
        )

        self._application.mainWindow.Unbind(
            wx.EVT_MENU, handler=self.__onSetPageAliasPopupClick
        )

        self._application.mainWindow.Unbind(
            wx.EVT_MENU, handler=self.__onChangePageUIDPopupClick
        )

        self._application.mainWindow.Unbind(
            wx.EVT_MENU, handler=self.__onSetPageCreationDatePopupClick
        )

        self._application.mainWindow.Unbind(
            wx.EVT_MENU, handler=self.__onSetPageChangeDatePopupClick
        )
