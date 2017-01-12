# -*- coding: UTF-8 -*-
import wx

from hackpage.i18n import get_
from hackpage.actions.changeuid import ChangeUIDAction
from hackpage.actions.setalias import SetAliasAction
from hackpage.utils import changeUidWithDialog, setAliasWithDialog


class GuiController(object):
    """
    Создание элементов интерфейса с использованием actions
    """
    def __init__(self, controller, application):
        self._controller = controller
        self._application = application

        # All actions list
        self._actions = [ChangeUIDAction, SetAliasAction]

        global _
        _ = get_()

        self._mainSubmenuItem = None

        # Pointer to clicked page
        self._selectedPage = None

        self.CHANGE_PAGE_UID = wx.NewId()
        self.SET_PAGE_ALIAS_UID = wx.NewId()
        self._popupSubmenu = None

    def _bind(self):
        self._application.onTreePopupMenu += self.__onTreePopupMenu

    def _unbind(self):
        self._application.onTreePopupMenu -= self.__onTreePopupMenu

    def initialize(self):
        self._bind()

        if self._application.mainWindow is not None:
            map(lambda action: self._application.actionController.register(
                action(self._application, self._controller), None),
                self._actions)

            self.createTools()

    def createTools(self):
        mainWindow = self._application.mainWindow

        if mainWindow is None:
            return

        # Menu for actions
        menu = wx.Menu()
        self._mainSubmenuItem = mainWindow.mainMenu.toolsMenu.AppendSubMenu(
            menu,
            u'HackPage')

        map(lambda action: self._application.actionController.appendMenuItem(
            action.stringId, menu), self._actions)

    def destroy(self):
        self._unbind()
        actionController = self._application.actionController
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            map(lambda action: actionController.removeAction(action.stringId),
                self._actions)
            mainWindow.mainMenu.toolsMenu.RemoveItem(self._mainSubmenuItem)
            self._mainSubmenuItem = None

    def __onTreePopupMenu(self, menu, page):
        self._selectedPage = page

        self._popupSubmenu = wx.Menu()
        self._popupSubmenu.Append(self.CHANGE_PAGE_UID,
                                  _(u"Change page identifier..."))
        self._popupSubmenu.Append(self.SET_PAGE_ALIAS_UID,
                                  _(u"Set page alias..."))

        menu.AppendSubMenu(self._popupSubmenu, u"HackPage")

        self._application.mainWindow.Bind(
            wx.EVT_MENU,
            id=self.CHANGE_PAGE_UID,
            handler=self.__onChangePageUIDPopupClick
        )

        self._application.mainWindow.Bind(
            wx.EVT_MENU,
            id=self.SET_PAGE_ALIAS_UID,
            handler=self.__onSetPageAliasPopupClick
        )

    def __onChangePageUIDPopupClick(self, event):
        assert self._selectedPage is not None

        changeUidWithDialog(self._selectedPage, self._application)
        self._application.mainWindow.Unbind(wx.EVT_MENU,
                                            id=self.CHANGE_PAGE_UID)

        self._selectedPage = None

    def __onSetPageAliasPopupClick(self, event):
        assert self._selectedPage is not None

        setAliasWithDialog(self._selectedPage, self._application)
        self._application.mainWindow.Unbind(wx.EVT_MENU,
                                            id=self.SET_PAGE_ALIAS_UID)

        self._selectedPage = None
