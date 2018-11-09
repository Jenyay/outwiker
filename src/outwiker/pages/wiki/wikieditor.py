# -*- coding: utf-8 -*-

import os
import os.path

import wx.stc

from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.gui.texteditor import TextEditor
from .wikiconfig import WikiConfig
from functools import reduce


class WikiEditor (TextEditor):
    def __init__(self, parent):
        self._colorizeSyntax = True
        self._styles = {}

        super(WikiEditor, self).__init__(parent)
        self.dropTarget = DropTarget(Application, self)

    def __createStyles(self, config):
        self._styles = {}

        # Константы для стилей
        self.STYLE_BOLD_ID = 1 << 0
        self.STYLE_ITALIC_ID = 1 << 1
        self.STYLE_UNDERLINE_ID = 1 << 2
        self.STYLE_LINK_ID = 1 << 3
        self.STYLE_HEADING_ID = 1 << 4
        self.STYLE_COMMAND_ID = (1 << 4) + 1

        # Комбинации стилей
        self.STYLE_BOLD_ITALIC_UNDERLINE_ID = (self.STYLE_BOLD_ID |
                                               self.STYLE_ITALIC_ID |
                                               self.STYLE_UNDERLINE_ID)

        self.STYLE_BOLD_ITALIC_ID = self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID
        self.STYLE_BOLD_UNDERLINE_ID = self.STYLE_BOLD_ID | self.STYLE_UNDERLINE_ID
        self.STYLE_ITALIC_UNDERLINE_ID = self.STYLE_ITALIC_ID | self.STYLE_UNDERLINE_ID

        self.STYLE_LINK_BOLD_ITALIC_UNDERLINE_ID = (self.STYLE_BOLD_ID |
                                                    self.STYLE_ITALIC_ID |
                                                    self.STYLE_UNDERLINE_ID |
                                                    self.STYLE_LINK_ID)

        self.STYLE_LINK_ITALIC_UNDERLINE_ID = (self.STYLE_ITALIC_ID |
                                               self.STYLE_UNDERLINE_ID |
                                               self.STYLE_LINK_ID)

        self.STYLE_LINK_BOLD_UNDERLINE_ID = (self.STYLE_BOLD_ID |
                                             self.STYLE_UNDERLINE_ID |
                                             self.STYLE_LINK_ID)

        self.STYLE_LINK_BOLD_ITALIC_ID = (self.STYLE_BOLD_ID |
                                          self.STYLE_ITALIC_ID |
                                          self.STYLE_LINK_ID)

        self.STYLE_LINK_ITALIC_ID = self.STYLE_ITALIC_ID | self.STYLE_LINK_ID
        self.STYLE_LINK_UNDERLINE_ID = self.STYLE_UNDERLINE_ID | self.STYLE_LINK_ID
        self.STYLE_LINK_BOLD_ID = self.STYLE_BOLD_ID | self.STYLE_LINK_ID

        # Заполняем словарь стилей
        self._styles[self.STYLE_BOLD_ID] = "bold"
        self._styles[self.STYLE_ITALIC_ID] = "italic"
        self._styles[self.STYLE_UNDERLINE_ID] = "underline"
        self._styles[self.STYLE_BOLD_ITALIC_UNDERLINE_ID] = "bold,italic,underline"
        self._styles[self.STYLE_BOLD_ITALIC_ID] = "bold,italic"
        self._styles[self.STYLE_BOLD_UNDERLINE_ID] = "bold,underline"
        self._styles[self.STYLE_ITALIC_UNDERLINE_ID] = "italic,underline"
        self._styles[self.STYLE_LINK_ID] = config.link.value.tostr()
        self._styles[self.STYLE_LINK_BOLD_ITALIC_UNDERLINE_ID] = self._styles[self.STYLE_LINK_ID] + \
            ",bold,italic,underline"
        self._styles[self.STYLE_LINK_ITALIC_UNDERLINE_ID] = self._styles[self.STYLE_LINK_ID] + \
            ",italic,underline"
        self._styles[self.STYLE_LINK_BOLD_UNDERLINE_ID] = self._styles[self.STYLE_LINK_ID] + ",bold,underline"
        self._styles[self.STYLE_LINK_UNDERLINE_ID] = self._styles[self.STYLE_LINK_ID] + ",underline"
        self._styles[self.STYLE_LINK_BOLD_ITALIC_ID] = self._styles[self.STYLE_LINK_ID] + ",bold,italic"
        self._styles[self.STYLE_LINK_ITALIC_ID] = self._styles[self.STYLE_LINK_ID] + ",italic"
        self._styles[self.STYLE_LINK_BOLD_ID] = self._styles[self.STYLE_LINK_ID] + ",bold"
        self._styles[self.STYLE_HEADING_ID] = config.heading.value.tostr()
        self._styles[self.STYLE_COMMAND_ID] = config.command.value.tostr()

    def setDefaultSettings(self):
        super(WikiEditor, self).setDefaultSettings()
        config = WikiConfig(Application.config)

        self.__createStyles(config)

        self._colorizeSyntax = config.colorizeSyntax.value

        self.textCtrl.SetLexer(wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(
            wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT)

        for (styleid, style) in self._styles.items():
            self.textCtrl.StyleSetSpec(styleid, style)
            self.textCtrl.StyleSetSize(styleid, self.config.fontSize.value)
            self.textCtrl.StyleSetFaceName(styleid, self.config.fontName.value)
            self.textCtrl.StyleSetBackground(
                styleid, self.config.backColor.value)

        self.textCtrl.StyleSetSpec(
            self.STYLE_HEADING_ID, self._styles[self.STYLE_HEADING_ID])
        self.textCtrl.StyleSetSize(
            self.STYLE_HEADING_ID,
            self.config.fontSize.value + 2)
        self.textCtrl.StyleSetFaceName(
            self.STYLE_HEADING_ID,
            self.config.fontName.value)
        self.textCtrl.StyleSetBackground(
            self.STYLE_HEADING_ID,
            self.config.backColor.value)

    @property
    def colorizeSyntax(self):
        return self._colorizeSyntax

    def turnList(self, itemStart):
        """
        Создать список
        """
        selText = self.textCtrl.GetSelectedText()
        items = [item for item in selText.split("\n") if len(item.strip()) > 0]

        # Собираем все элементы
        if len(items) > 0:
            itemsList = reduce(
                lambda result,
                item: result +
                itemStart +
                item.strip() +
                "\n",
                items,
                u"")
        else:
            itemsList = itemStart + "\n"

        itemsList = itemsList[: -1]

        self.textCtrl.ReplaceSelection(itemsList)


class DropTarget(wx.FileDropTarget):
    """
    Class to drag files to the wiki editor
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
                corrected_fname = 'Attach:' + corrected_fname[len(prefix):]

            correctedFiles.append(corrected_fname)

        text = ' '.join(correctedFiles)
        self._editor.replaceText(text)

        return True
