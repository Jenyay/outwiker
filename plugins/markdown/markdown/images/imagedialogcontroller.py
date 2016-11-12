# -*- coding: utf-8 -*-

from outwiker.core.commands import isImage


class ImageDialogController (object):
    def __init__(self, dialog, attachList, selectedText):
        """
        dialog - ImageDialog instance
        attachList - list of the attached files
        selectedText - selected in the editor text
        """
        self._dialog = dialog
        self._attachList = attachList
        self._selectedText = selectedText.strip()

        # Result string after dialog running
        self.result = u""
        self._initDialog()

    def _initDialog(self):
        attach_str = u'__attach/'

        filesList = filter(isImage, self._attachList)
        filesList.sort()

        comboItems = [attach_str + item for item in filesList]
        self._dialog.filesList = comboItems

        if self._selectedText in comboItems:
            self._dialog.fileName = self._selectedText
        else:
            self._dialog.comment = self._selectedText

    def showDialog(self):
        resultDlg = self._dialog.ShowModal()
        self.result = self._generateText()
        return resultDlg

    def _generateText(self):
        fname = self._dialog.fileName
        comment = self._dialog.comment

        result = u"![{comment}]({url})".format(comment=comment, url=fname)
        return result
