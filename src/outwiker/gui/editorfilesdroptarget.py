# -*- coding: utf-8 -*-

import os.path

import wx

from outwiker.core.attachment import Attachment


class EditorFilesDropTarget(wx.FileDropTarget):
    """
    Base class to drag files to the editors
    """
    def __init__(self, application, editor):
        wx.FileDropTarget.__init__(self)
        self._application = application
        self._editor = editor
        self._editor.SetDropTarget(self)

    def destroy(self):
        self._editor.SetDropTarget(None)
        self._editor = None

    def OnDropFiles(self, x, y, files):
        assert self._application.selectedPage is not None

        if len(files) == 1 and '\n' in files[0]:
            files = files[0].split('\n')

        file_protocol = 'file://'

        # Prepare absolute path for attach folder
        attach = Attachment(self._application.selectedPage)
        attach_path = os.path.realpath(
            os.path.abspath(attach.getAttachPath(False)))

        if not attach_path.endswith(os.sep):
            attach_path += os.sep

        correctedFiles = []
        is_attached = False

        for fname in files:
            if not fname.strip():
                continue

            # Remove file:// protocol
            if fname.startswith(file_protocol):
                fname = fname[len(file_protocol):]

            corrected_fname = os.path.realpath(os.path.abspath(fname))

            # Is attached file?
            prefix = os.path.commonprefix([corrected_fname, attach_path])
            if prefix == attach_path:
                is_attached = True
                corrected_fname = corrected_fname[len(prefix):]

            correctedFiles.append(corrected_fname)

        if is_attached:
            self._application.onAttachmentPaste(correctedFiles)
        else:
            text = ' '.join(correctedFiles)
            self._editor.replaceText(text)

        return True
