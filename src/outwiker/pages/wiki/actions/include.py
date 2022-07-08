# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Callable, Optional, Union

import wx

from outwiker.gui.baseaction import BaseAction
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.controls.controlnotify import ControlNotify
from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox
from outwiker.gui.guiconfig import GuiConfig
from outwiker.gui.windowssizesaver import WindowSizeSaver
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
        self._size_saver = WindowSizeSaver('wiki_include_dialog',
                                           self._application.config)

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
            self._size_saver.restoreSize(dlg)
            controller = IncludeDialogController(dlg, self._application.selectedPage)

            text = controller.getDialogResult()
            if text is not None:
                self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(text)

            self._size_saver.saveSize(dlg)

class IncludeDialogController:
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

        return "(:include {}:)".format(" ".join(params))


class IncludeDialog(TestedDialog):
    def __init__(self, parent):
        super().__init__(parent,
                         style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER)
        self.SetTitle(_("Insert (:include:) command"))

        self._createGui()
        self._layout()

    @property
    def selectedAttachment(self) -> str:
        return self._attachComboBox.GetValue()

    @selectedAttachment.setter
    def selectedAttachment(self, value: str):
        self._attachComboBox.SetValue(value)

    @property
    def selectedEncoding(self) -> str:
        return self._encodingComboBox.GetValue()

    @selectedEncoding.setter
    def selectedEncoding(self, value: int):
        self._encodingComboBox.SetSelection(value)

    @property
    def escapeHtml(self) -> bool:
        return self._escapeHtmlCheckBox.IsChecked()

    @escapeHtml.setter
    def escapeHtml(self, value: bool):
        self._escapeHtmlCheckBox.SetValue(value)

    @property
    def parseWiki(self) -> bool:
        return self._wikiParseCheckBox.IsChecked()

    @parseWiki.setter
    def parseWiki(self, value: bool):
        self._wikiParseCheckBox.SetValue(value)

    def _createGui(self):
        # Выбор прикрепленного файла
        self._attachLabel = wx.StaticText(self, label=_("Select attachment"))
        font = self._attachLabel.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        self._attachLabel.SetFont(font)

        self._attachComboBox = FilesTreeComboBox(self)
        self._attachComboBox.SetValidator(IncludeFileValidator())

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

        self.Bind(wx.EVT_CLOSE, handler=self._onClose)

    def _onClose(self, event):
        self.EndModal(wx.ID_CANCEL)

    def _layout(self):
        main_sizer = wx.FlexGridSizer(cols=1)
        main_sizer.AddGrowableCol(0)
        main_sizer.AddGrowableRow(5)

        main_sizer.Add(self._attachLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=4)
        main_sizer.Add(self._attachComboBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        second_sizer = wx.FlexGridSizer(cols=2)
        second_sizer.AddGrowableCol(1)
        second_sizer.AddGrowableRow(0)

        second_sizer.Add(self._encodingLabel,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)
        second_sizer.Add(self._encodingComboBox,
                      flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT,
                      border=2)

        main_sizer.Add(second_sizer, flag=wx.EXPAND | wx.ALL, border=2)

        main_sizer.Add(self._escapeHtmlCheckBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        main_sizer.Add(self._wikiParseCheckBox,
                      flag=wx.EXPAND | wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                      border=2)

        main_sizer.Add(
            self._buttonsSizer,
            flag=wx.ALL | wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT,
            border=2)

        self.SetSizer(main_sizer)
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


class IncludeFileValidator(wx.Validator):
    def __init__(self):
        super().__init__()

    def Clone(self):
        return IncludeFileValidator()

    def TransferFromWindow(self):
        return True

    def TransferToWindow(self):
        return True

    def Validate(self, parent):
        notify = ControlNotify(self.GetWindow())
        title = _('Select file')

        root_dir = self.GetWindow().GetRootDir()
        path_relative = self.GetWindow().GetValue()

        if root_dir is None or path_relative is None or path_relative == '.':
            message = _('File not selected')
            notify.ShowError(title, message)
            return False

        full_path = Path(root_dir, path_relative)

        if not full_path.exists():
            message = _('Selected file not exists')
            notify.ShowError(title, message)
            return False

        if full_path.is_dir():
            message = _('Select a file, not a folder')
            notify.ShowError(title, message)
            return False

        return True
