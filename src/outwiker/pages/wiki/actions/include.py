# -*- coding: utf-8 -*-

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.core.attachment import Attachment
from outwiker.core.commands import showError


class WikiIncludeAction(BaseAction):
    """
    Вставка команды для вставки содержимого прикрепленного файла
    """
    stringId = u"WikiInclude"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Include (:include ...:)")

    @property
    def description(self):
        return _(u"Insert (:include:) command")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        if len(Attachment(self._application.selectedPage).attachmentFull) == 0:
            showError(self._application.mainWindow,
                      _(u"Current page does not have any attachments"))
            return

        with IncludeDialog(self._application.mainWindow) as dlg:
            controller = IncludeDialogController(
                dlg, self._application.selectedPage)

            text = controller.getDialogResult()
            if text is not None:
                self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(
                    text)


class IncludeDialogController (object):
    def __init__(self, dialog, selectedPage):
        assert selectedPage is not None
        assert dialog is not None

        self._dialog = dialog
        self._selectedPage = selectedPage

        encodings = [
            u"utf-8",
            u"utf-16",
            u"windows-1251",
            u"koi8_r",
            u"koi8_u",
            u"cp866",
            u"mac_cyrillic",
        ]

        self._dialog.encodingsList = encodings
        self._dialog.selectedEncoding = 0
        self._fillAttaches()

    def getDialogResult(self):
        if self._dialog.ShowModal() == wx.ID_OK:
            return self._getCommand()

    def _fillAttaches(self):
        attachList = Attachment(self._selectedPage).getAttachRelative()
        attachList.sort(key=str.lower)

        self._dialog.attachmentList = attachList

    def _getCommand(self):
        params = []

        params.append("Attach:" + self._dialog.selectedAttachment)

        if self._dialog.selectedEncoding != "utf-8":
            params.append("encoding=" + '"' +
                          self._dialog.selectedEncoding + '"')

        if self._dialog.escapeHtml:
            params.append("htmlescape")

        if self._dialog.parseWiki:
            params.append("wikiparse")

        return u"(:include {}:)".format(u" ".join(params))


class IncludeDialog (TestedDialog):
    def __init__(self, parent):
        super(IncludeDialog, self).__init__(parent)

        self.SetTitle(_(u"Insert (:include:) command"))

        self.__createGui()
        self.__layout()

    @property
    def selectedAttachment(self):
        return self._attachComboBox.GetValue()

    @selectedAttachment.setter
    def selectedAttachment(self, value):
        self._attachComboBox.SetSelection(value)

    @property
    def selectedEncoding(self):
        return self._encodingComboBox.GetValue()

    @selectedEncoding.setter
    def selectedEncoding(self, value):
        self._encodingComboBox.SetSelection(value)

    @property
    def escapeHtml(self):
        return self._escapeHtmlCheckBox.IsChecked()

    @escapeHtml.setter
    def escapeHtml(self, value):
        self._escapeHtmlCheckBox.SetValue(value)

    @property
    def parseWiki(self):
        return self._wikiParseCheckBox.IsChecked()

    @parseWiki.setter
    def parseWiki(self, value):
        self._wikiParseCheckBox.SetValue(value)

    def __createGui(self):
        # Выбор прикрепленного файла
        self._attachLabel = wx.StaticText(self, label=_(u"Select attachment"))
        self._attachComboBox = wx.ComboBox(
            self, style=wx.CB_DROPDOWN | wx.CB_READONLY)

        # Кодировка
        self._encodingLabel = wx.StaticText(self, label=_(u"Encoding"))
        self._encodingComboBox = wx.ComboBox(self, style=wx.CB_DROPDOWN)

        # Преобразовывать символы HTML?
        self._escapeHtmlCheckBox = wx.CheckBox(
            self, label=_(u"Convert symbols <, > and && to HTML"))

        # Делать разбор викинотации?
        self._wikiParseCheckBox = wx.CheckBox(
            self, label=_(u"Parse wiki notation"))

        self._buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)

    def __layout(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableCol(1)

        mainSizer.Add(self._attachLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.Add(self._attachComboBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        mainSizer.Add(self._encodingLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.Add(self._encodingComboBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        mainSizer.Add(self._escapeHtmlCheckBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.AddStretchSpacer()

        mainSizer.Add(self._wikiParseCheckBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        mainSizer.AddStretchSpacer()

        mainSizer.AddStretchSpacer()
        mainSizer.Add(
            self._buttonsSizer,
            flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
            border=2)

        self.SetSizer(mainSizer)
        self.Fit()

    @property
    def encodingsList(self):
        return self._encodingComboBox.GetStrings()

    @encodingsList.setter
    def encodingsList(self, encodings):
        self._encodingComboBox.Clear()
        self._encodingComboBox.AppendItems(encodings)

    @property
    def attachmentList(self):
        return self._attachComboBox.GetStrings()

    @attachmentList.setter
    def attachmentList(self, attachList):
        self._attachComboBox.Clear()
        self._attachComboBox.AppendItems(attachList)

        if self._attachComboBox.GetCount() > 0:
            self._attachComboBox.SetSelection(0)
