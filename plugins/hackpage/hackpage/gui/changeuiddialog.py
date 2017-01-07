# -*- coding: UTF-8 -*-

import re

import wx

from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.commands import MessageBox

from hackpage.i18n import get_


class ChangeUidDialog(TestedDialog):
    """
    The dialog to enter a new page UID
    """
    def __init__(self, parent):
        global _
        _ = get_()

        super(ChangeUidDialog, self).__init__(
            parent,
            style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME,
            title=_(u"Change page UID")
        )

        # Функция для проверки правильности введенного идентификатора
        self.uidValidator = None

        self._createGui()
        self._newUidText.SetFocus()
        self._newUidText.SetSelection(0, -1)

        self.Center(wx.CENTRE_ON_SCREEN)

        self.Bind(wx.EVT_BUTTON, self.__onOk, id=wx.ID_OK)
        self.Bind(wx.EVT_TEXT, self.__onTextChanged, self._newUidText)

    def __onOk(self, event):
        result = u'' if self.uidValidator is None else self.uidValidator(self.uid)

        if len(result) == 0:
            self.EndModal(wx.ID_OK)
        else:
            MessageBox(result, _(u"Error"), wx.ICON_ERROR | wx.OK)

    def __onTextChanged(self, event):
        self.Unbind(wx.EVT_TEXT, self._newUidText)

        selFrom, selTo = self._newUidText.GetSelection()
        self._newUidText.Value = self._newUidText.Value.replace(u" ", u"_")
        self._newUidText.SetSelection(selTo, selTo)

        self.Bind(wx.EVT_TEXT, self.__onTextChanged, self._newUidText)

    def _createGui(self):
        """
        Создать элементы управления
        """
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(2)

        self._questionLabel = wx.StaticText(
            self,
            label=_(u"Enter new page identifier")
        )

        newUidSizer = wx.FlexGridSizer(cols=2)
        newUidSizer.AddGrowableCol(1)

        protocolLabel = wx.StaticText(self, label=u"page://")
        self._newUidText = wx.TextCtrl(self)
        self._newUidText.SetMinSize((400, -1))

        newUidSizer.Add(protocolLabel,
                        flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                        border=2)
        newUidSizer.Add(self._newUidText, flag=wx.ALL | wx.EXPAND, border=2)

        mainSizer.Add(self._questionLabel, flag=wx.ALL, border=2)
        mainSizer.Add(newUidSizer, flag=wx.ALL | wx.EXPAND, border=2)

        self._createOkCancelButtons(mainSizer)

        self.SetSizer(mainSizer)
        self.Fit()

    def _createOkCancelButtons(self, mainSizer):
        okCancel = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        mainSizer.Add(
            okCancel,
            flag=wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM,
            border=2
        )

    @property
    def uid(self):
        newuid = self._newUidText.GetValue().strip()
        assert len(newuid) != 0
        return newuid

    @uid.setter
    def uid(self, value):
        self._newUidText.SetValue(value.strip())

    def setPageTitle(self, pageTitle):
        self._questionLabel.SetLabel(_(u'Enter new identifier for page "{}"').format(pageTitle))
        self.Fit()


class ChangeUidDialogController(object):
    """
    Класс для управления диалогом ChangeUidDialog
    """
    def __init__(self, application, dialog, page):
        """
        dialog - экземпляр класса InsertDialog,
                который надо будет показать пользователю.
        page - текущая страница, для которой показывается диалог
        """
        assert page is not None
        assert dialog is not None
        assert application is not None

        self._application = application
        self._dialog = dialog
        self._page = page
        self._dialog.uid = self._application.pageUidDepot.createUid(self._page)
        self._dialog.setPageTitle(self._page.display_title)
        self._dialog.uidValidator = self.validate

    def showDialog(self):
        """
        Метод показывает диалог и возвращает строку,
        соответствующую выбранным настройкам.
        Если пользователь нажимает кнопку "Cancel", возвращается None
        """
        result = self._dialog.ShowModal()
        return result

    def validate(self, newiud):
        """
        Возвращает пустую строку, если newiud соответствует требованиям
            к идентификаторам.
        Возвращает строку с описанием ошибки, если что-то неверно.
        """
        otherpage = self._application.pageUidDepot[newiud]

        if(otherpage is not None and otherpage != self._page):
            return _(u"Same identifier exist already")

        regexp = re.compile(r"^[-\w,\$\.\+\!\*\(\):@|&=\?~\#\%]+$",
                            re.I | re.U)
        match = regexp.match(newiud)

        if match is None:
            return _(u"Identifier contain invalid character")

        return u""
