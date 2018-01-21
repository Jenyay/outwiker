# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty

import wx

from outwiker.gui.baseaction import BaseAction

from .i18n import get_
from .comboboxdialog import ComboBoxDialog
from .dialogcontroller import UserDialogController, CommunityDialogController


class BaseLJAction(BaseAction, metaclass=ABCMeta):
    def __init__(self, application):
        self._application = application

        global _
        _ = get_()

    @abstractproperty
    def dialogTitle(self):
        pass

    @abstractproperty
    def controllerType(self):
        pass

    def run(self, params):
        assert self._application.mainWindow is not None

        with ComboBoxDialog(self._application.mainWindow,
                            self.dialogTitle,
                            self.dialogTitle,
                            wx.CB_DROPDOWN | wx.CB_SORT) as dlg:
            editor = self._getPageView().codeEditor

            selText = editor.GetSelectedText()

            controller = self.controllerType(dlg, self._application, selText)
            if controller.showDialog() == wx.ID_OK:
                editor.replaceText(controller.result)

    def _getPageView(self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pageView


class LJUserAction(BaseLJAction):
    stringId = u"Livejournal_user"

    @property
    def title(self):
        return _(u"LiveJournal user (:ljuser ...:)")

    @property
    def description(self):
        return _(u"LiveJournal plugin. Insert (:ljuser... :) command to create the link to LiveJournal user")

    @property
    def dialogTitle(self):
        return _(u"LiveJournal user")

    @property
    def controllerType(self):
        return UserDialogController


class LJCommAction(BaseLJAction):
    stringId = u"LiveJournal_commmunity"

    @property
    def title(self):
        return _(u"LiveJournal community (:ljcomm ...:)")

    @property
    def description(self):
        return _(u"LiveJournal plugin. Insert (:ljcomm... :) command to create the link to LiveJournal community")

    @property
    def dialogTitle(self):
        return _(u"LiveJournal community")

    @property
    def controllerType(self):
        return CommunityDialogController
