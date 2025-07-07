# -*- coding: utf-8 -*-

from functools import reduce

import wx.stc

from outwiker.gui.texteditor import TextEditor
from .wikiconfig import WikiConfig


class WikiEditor(TextEditor):
    def __init__(self, parent, application):
        super().__init__(parent, application)
        self._colorizeSyntax = True
        self._styles = {}

    def __createStyles(self, config):
        self._styles = {}

        # Константы для стилей
        self.STYLE_BOLD_ID = 1 << 0
        self.STYLE_ITALIC_ID = 1 << 1
        self.STYLE_UNDERLINE_ID = 1 << 2
        self.STYLE_LINK_ID = 1 << 3
        self.STYLE_HEADING_ID = 1 << 4
        self.STYLE_COMMAND_ID = (1 << 4) + 1
        self.STYLE_COMMENT_ID = (1 << 4) + 2
        self.STYLE_ATTACHMENT_ID = (1 << 4) + 3
        self.STYLE_THUMBNAIL_ID = (1 << 4) + 4

        # Комбинации стилей
        self.STYLE_BOLD_ITALIC_UNDERLINE_ID = (
            self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID | self.STYLE_UNDERLINE_ID
        )

        self.STYLE_BOLD_ITALIC_ID = self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID
        self.STYLE_BOLD_UNDERLINE_ID = self.STYLE_BOLD_ID | self.STYLE_UNDERLINE_ID
        self.STYLE_ITALIC_UNDERLINE_ID = self.STYLE_ITALIC_ID | self.STYLE_UNDERLINE_ID

        self.STYLE_LINK_BOLD_ITALIC_UNDERLINE_ID = (
            self.STYLE_BOLD_ID
            | self.STYLE_ITALIC_ID
            | self.STYLE_UNDERLINE_ID
            | self.STYLE_LINK_ID
        )

        self.STYLE_LINK_ITALIC_UNDERLINE_ID = (
            self.STYLE_ITALIC_ID | self.STYLE_UNDERLINE_ID | self.STYLE_LINK_ID
        )

        self.STYLE_LINK_BOLD_UNDERLINE_ID = (
            self.STYLE_BOLD_ID | self.STYLE_UNDERLINE_ID | self.STYLE_LINK_ID
        )

        self.STYLE_LINK_BOLD_ITALIC_ID = (
            self.STYLE_BOLD_ID | self.STYLE_ITALIC_ID | self.STYLE_LINK_ID
        )

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
        self._styles[self.STYLE_LINK_BOLD_ITALIC_UNDERLINE_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",bold,italic,underline"
        )
        self._styles[self.STYLE_LINK_ITALIC_UNDERLINE_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",italic,underline"
        )
        self._styles[self.STYLE_LINK_BOLD_UNDERLINE_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",bold,underline"
        )
        self._styles[self.STYLE_LINK_UNDERLINE_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",underline"
        )
        self._styles[self.STYLE_LINK_BOLD_ITALIC_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",bold,italic"
        )
        self._styles[self.STYLE_LINK_ITALIC_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",italic"
        )
        self._styles[self.STYLE_LINK_BOLD_ID] = (
            self._styles[self.STYLE_LINK_ID] + ",bold"
        )
        self._styles[self.STYLE_HEADING_ID] = config.heading.value.tostr()
        self._styles[self.STYLE_COMMAND_ID] = config.command.value.tostr()
        self._styles[self.STYLE_COMMENT_ID] = config.comment.value.tostr()
        self._styles[self.STYLE_ATTACHMENT_ID] = config.attachment.value.tostr()
        self._styles[self.STYLE_THUMBNAIL_ID] = config.thumbnail.value.tostr()

    def setDefaultSettings(self):
        super().setDefaultSettings()
        config = WikiConfig(self._application.config)

        self.__createStyles(config)

        self._colorizeSyntax = config.colorizeSyntax.value

        self.textCtrl.SetLexer(wx.stc.STC_LEX_CONTAINER)
        self.textCtrl.SetModEventMask(
            wx.stc.STC_MOD_INSERTTEXT | wx.stc.STC_MOD_DELETETEXT
        )

        for styleid, style in self._styles.items():
            self.textCtrl.StyleSetSpec(styleid, style)
            self.textCtrl.StyleSetSize(styleid, self.config.fontSize.value)
            self.textCtrl.StyleSetFaceName(styleid, self.config.fontName.value)
            self.textCtrl.StyleSetBackground(styleid, self.config.backColor.value)

        self.textCtrl.StyleSetSpec(
            self.STYLE_HEADING_ID, self._styles[self.STYLE_HEADING_ID]
        )
        self.textCtrl.StyleSetSize(
            self.STYLE_HEADING_ID, self.config.fontSize.value + 2
        )
        self.textCtrl.StyleSetFaceName(
            self.STYLE_HEADING_ID, self.config.fontName.value
        )
        self.textCtrl.StyleSetBackground(
            self.STYLE_HEADING_ID, self.config.backColor.value
        )

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
                lambda result, item: result + itemStart + item.strip() + "\n", items, ""
            )
        else:
            itemsList = itemStart + "\n"

        itemsList = itemsList[:-1]

        self.textCtrl.ReplaceSelection(itemsList)
