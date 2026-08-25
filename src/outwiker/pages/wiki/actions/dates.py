# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.dateformatdialog import DateFormatDialog


class WikiDateBaseAction(BaseAction, metaclass=ABCMeta):
    def __init__(self, application):
        self._application = application

    @abstractmethod
    def getCommandName(self):
        pass

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        with DateFormatDialog(
            self._application.mainWindow,
            _("Date format\n(empty string - format from program setting)"),
            _("Date format"),
            "",
        ) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                params = ' format="{}"'.format(dlg.Value) if len(dlg.Value) != 0 else ""
                text = "(:{}{}:)".format(self.getCommandName(), params)

                self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(
                    text
                )


class WikiDateCreationAction(WikiDateBaseAction):
    """
    Вставка команды для вывода даты создания страницы
    """

    stringId = "WikiDateCreation"

    @property
    def title(self):
        return _("Creation date (:crdate:)")

    @property
    def description(self):
        return _("Insert command (:crdate:) for show date of creation of the page")

    def getCommandName(self):
        return "crdate"


class WikiDateEditionAction(WikiDateBaseAction):
    """
    Вставка команды для вывода даты последнего редактирования страницы
    """

    stringId = "WikiDateEdit"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Edition date (:eddate:)")

    @property
    def description(self):
        return _(
            "Insert command (:eddate:) for show date of last modification of the page"
        )

    def getCommandName(self):
        return "eddate"
