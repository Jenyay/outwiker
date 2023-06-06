# -*- coding=utf-8 -*-

from pathlib import Path

import wx

from outwiker.gui.controls.controlnotify import ControlNotify


class SelectedFileValidator(wx.Validator):
    """
    Validate file selection (not directory!) in FilesTreeComboBox
    """
    def __init__(self):
        super().__init__()

    def Clone(self):
        return SelectedFileValidator()

    def TransferFromWindow(self):
        return True

    def TransferToWindow(self):
        return True

    def Validate(self, parent):
        notify = ControlNotify(self.GetWindow())
        title = _('Select file')

        root_dir = self.GetWindow().GetRootDir()
        path_relative = self.GetWindow().GetValue()

        if (path_relative is None or
                len(path_relative.strip()) == 0 or
                path_relative == '.'):
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
