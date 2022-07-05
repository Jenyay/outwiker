# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Callable, Optional, Union

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox
from outwiker.core.attachfilters import getHiddenFilter, notFilter
from outwiker.core.attachment import Attachment
from outwiker.core.commands import showError


class WikiIncludeAction(BaseAction):
    """
    Вставка команды для вставки содержимого прикрепленного файла
    """
    stringId = "WikiInclude"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Include (:include ...:)")

    @property
    def description(self):
        return _("Insert (:include:) command")

    def run(self, params):
        assert self._application.mainWindow is not None
        assert self._application.mainWindow.pagePanel is not None

        if len(Attachment(self._application.selectedPage).attachmentFull) == 0:
            showError(self._application.mainWindow,
                      _("Current page does not have any attachments"))
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
            "utf-8",
            "utf-16",
            "windows-1251",
            "koi8_r",
            "koi8_u",
            "cp866",
            "mac_cyrillic",
        ]

        self._dialog.encodingsList = encodings
        self._dialog.selectedEncoding = 0
        filter = notFilter(getHiddenFilter(selectedPage))
        self._dialog.SetFilterFunc(filter)
        self._fillAttaches()

    def getDialogResult(self):
        if self._dialog.ShowModal() == wx.ID_OK:
            return self._getCommand()

    def _fillAttaches(self):
        attach = Attachment(self._selectedPage)
        self._dialog.setRootDir(attach.getAttachPath(create=False))

    def _getCommand(self):
        params = []

        params.append('Attach:"{}"'.format(self._dialog.selectedAttachment))

        if self._dialog.selectedEncoding != "utf-8":
            params.append("encoding=" + '"' +
                          self._dialog.selectedEncoding + '"')

        if self._dialog.escapeHtml:
            params.append("htmlescape")

        if self._dialog.parseWiki:
            params.append("wikiparse")

        return "(:include {}:)".format(u" ".join(params))


class IncludeDialog(TestedDialog):
    def __init__(self, parent):
        super().__init__(parent,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)

        self.SetTitle(_("Insert (:include:) command"))

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
        self._attachLabel = wx.StaticText(self, label=_("Select attachment"))
        self._attachComboBox = FilesTreeComboBox(self)

        # Кодировка
        self._encodingLabel = wx.StaticText(self, label=_("Encoding"))
        self._encodingComboBox = wx.ComboBox(self, style=wx.CB_DROPDOWN)

        # Преобразовывать символы HTML?
        self._escapeHtmlCheckBox = wx.CheckBox(
            self, label=_("Convert symbols <, > and && to HTML"))

        # Делать разбор викинотации?
        self._wikiParseCheckBox = wx.CheckBox(
            self, label=_("Parse wiki notation"))

        self._buttonsSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)

    def __layout(self):
        mainSizer = wx.FlexGridSizer(cols=2)
        mainSizer.AddGrowableCol(1)
        mainSizer.AddGrowableRow(4)

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
            flag=wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT,
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

    def setRootDir(self, root_dir: Union[str, Path]):
        self._attachComboBox.SetRootDir(root_dir)

    def SetFilterFunc(self, filter: Optional[Callable[[Path], bool]] = None):
        self._attachComboBox.SetFilterFunc(filter)
