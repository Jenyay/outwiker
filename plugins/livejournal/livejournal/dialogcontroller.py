# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import wx

from .ljconfig import LJConfig


class DialogController(object, metaclass=ABCMeta):
    """
    Базовый класс для диалога вставки пользователя и сообщества ЖЖ
    """
    def __init__(self, dialog, application, initial=u""):
        self._dialog = dialog
        self._application = application

        items = sorted(self.getParam(LJConfig(self._application.config)))
        self._items = [item.strip()
                       for item in items
                       if len(item.strip()) != 0]

        self._result = u""

        self._initDialog(initial)

    def _initDialog(self, initial):
        self._dialog.Clear()
        self._dialog.AppendItems(self._items)
        self._dialog.SetValue(initial)

    @abstractmethod
    def getParam(self, config):
        pass

    @abstractmethod
    def setParam(self, config, value):
        pass

    @abstractmethod
    def getCommandName(self):
        pass

    @property
    def result(self):
        return self._result

    def showDialog(self):
        dlgResult = self._dialog.ShowModal()
        if dlgResult == wx.ID_OK:
            name = self._dialog.GetValue().strip()
            self._result = u"(:{command} {name}:)".format(
                command=self.getCommandName(),
                name=name)

            if(len(name) != 0 and name not in self._items):
                self._items.append(name)

                clearItems = sorted([item
                                     for item in self._items
                                     if len(item.strip()) != 0])
                self.setParam(LJConfig(self._application.config), clearItems)

        return dlgResult


class UserDialogController(DialogController):
    """
    Класс контроллера для вставки пользователя ЖЖ
    """
    def getParam(self, config):
        return config.users.value

    def setParam(self, config, value):
        config.users.value = value

    def getCommandName(self):
        return u"ljuser"


class CommunityDialogController(DialogController):
    """
    Класс контроллера для вставки сообщества ЖЖ
    """
    def getParam(self, config):
        return config.communities.value

    def setParam(self, config, value):
        config.communities.value = value

    def getCommandName(self):
        return u"ljcomm"
