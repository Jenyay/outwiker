# -*- coding: utf-8 -*-

import os
import re

import wx

from outwiker.api.app.application import getImagesDir
from outwiker.api.app.texteditor import insertCurrentDate
from outwiker.api.core.attachment import Attachment
from outwiker.api.gui.actions import polyactions
from outwiker.api.pages.wiki.gui import BaseWikiPageView

from .links.linkdialog import LinkDialog
from .links.linkdialogcontroller import LinkDialogController
from .images.imagedialog import ImageDialog
from .images.imagedialogcontroller import ImageDialogController
from .defines import MENU_MARKDOWN, TOOLBAR_MARKDOWN_GENERAL
from .markdowneditor import MarkdownEditor


class MarkdownPageView(BaseWikiPageView):
    def __init__(self, parent, application):
        super().__init__(parent, application)
        self.imagesDir = getImagesDir()

    def _isHtmlCodeShown(self):
        return True

    def getTextEditor(self):
        return MarkdownEditor

    def _getPageTitle(self):
        return _("Markdown")

    def _getMenuTitle(self):
        return _("Markdown")

    def _getMenuId(self):
        return MENU_MARKDOWN

    def _getToolbarsInfo(self, mainWindow):
        return [(TOOLBAR_MARKDOWN_GENERAL, _("Markdown"))]

    def _getPolyActions(self):
        return [
            polyactions.BOLD_STR_ID,
            polyactions.ITALIC_STR_ID,
            polyactions.BOLD_ITALIC_STR_ID,
            polyactions.HEADING_1_STR_ID,
            polyactions.HEADING_2_STR_ID,
            polyactions.HEADING_3_STR_ID,
            polyactions.HEADING_4_STR_ID,
            polyactions.HEADING_5_STR_ID,
            polyactions.HEADING_6_STR_ID,
            polyactions.CODE_STR_ID,
            polyactions.HORLINE_STR_ID,
            polyactions.LINK_STR_ID,
            polyactions.IMAGE_STR_ID,
            polyactions.HTML_ESCAPE_STR_ID,
            polyactions.CURRENT_DATE,
            polyactions.COMMENT_STR_ID,
        ] + self._baseTextPolyactions

    def _getSpecificActions(self):
        return []

    def _getAttachString(self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при
        вставке выбранных прикрепленных файлов из панели вложений

        Перегрузка метода из BaseTextPanel
        """
        text = ""
        count = len(fnames)

        for n in range(count):
            text += "__attach/" + fnames[n]
            if n != count - 1:
                text += "\n"

        return text

    def _createWikiTools(self):
        assert self.mainWindow is not None

        self.toolsMenu.AppendSeparator()
        self._addFontTools()
        self._addToolbarSeparator()
        self._addHeadingTools()
        self._addToolbarSeparator()
        self._addOtherTools()

    def _addFontTools(self):
        self._fontMenu = wx.Menu()
        self.toolsMenu.AppendSubMenu(self._fontMenu, _("Font"))

        toolbar = self._application.mainWindow.toolbars[TOOLBAR_MARKDOWN_GENERAL]
        menu = self._fontMenu
        actionController = self._application.actionController

        # Bold
        actionController.getAction(polyactions.BOLD_STR_ID).setFunc(
            lambda param: self.turnText("**", "**")
        )

        actionController.appendMenuItem(polyactions.BOLD_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.BOLD_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold.svg"),
            fullUpdate=False,
        )

        # Italic
        actionController.getAction(polyactions.ITALIC_STR_ID).setFunc(
            lambda param: self.turnText("*", "*")
        )

        actionController.appendMenuItem(polyactions.ITALIC_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_italic.svg"),
            fullUpdate=False,
        )

        # Bold italic
        bold_italic_action = actionController.getAction(polyactions.BOLD_ITALIC_STR_ID)
        bold_italic_action.setFunc(lambda param: self.turnText("**_", "_**"))

        actionController.appendMenuItem(polyactions.BOLD_ITALIC_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.BOLD_ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold_italic.svg"),
            fullUpdate=False,
        )

        # Comment
        actionController.getAction(polyactions.COMMENT_STR_ID).setFunc(
            lambda param: self.turnText("<!--", "-->")
        )
        actionController.appendMenuItem(polyactions.COMMENT_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.COMMENT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "comment.svg"),
            fullUpdate=False,
        )

    def _addHeadingTools(self):
        """
        Added headings buttons
        """
        self._headingMenu = wx.Menu()
        self.toolsMenu.AppendSubMenu(self._headingMenu, _("Heading"))

        toolbar = self._application.mainWindow.toolbars[TOOLBAR_MARKDOWN_GENERAL]
        menu = self._headingMenu
        actionController = self._application.actionController

        actionController.getAction(polyactions.HEADING_1_STR_ID).setFunc(
            lambda param: self._setHeading("# ")
        )

        actionController.getAction(polyactions.HEADING_2_STR_ID).setFunc(
            lambda param: self._setHeading("## ")
        )

        actionController.getAction(polyactions.HEADING_3_STR_ID).setFunc(
            lambda param: self._setHeading("### ")
        )

        actionController.getAction(polyactions.HEADING_4_STR_ID).setFunc(
            lambda param: self._setHeading("#### ")
        )

        actionController.getAction(polyactions.HEADING_5_STR_ID).setFunc(
            lambda param: self._setHeading("##### ")
        )

        actionController.getAction(polyactions.HEADING_6_STR_ID).setFunc(
            lambda param: self._setHeading("###### ")
        )

        actionController.appendMenuItem(polyactions.HEADING_1_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HEADING_1_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_1.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(polyactions.HEADING_2_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HEADING_2_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_2.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(polyactions.HEADING_3_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HEADING_3_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_3.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(polyactions.HEADING_4_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HEADING_4_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_4.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(polyactions.HEADING_5_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HEADING_5_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_5.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(polyactions.HEADING_6_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HEADING_6_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_6.svg"),
            fullUpdate=False,
        )

    def _addOtherTools(self):
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_MARKDOWN_GENERAL]
        menu = self.toolsMenu
        actionController = self._application.actionController

        # Link
        actionController.getAction(polyactions.LINK_STR_ID).setFunc(self._insertLink)

        actionController.appendMenuItem(polyactions.LINK_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.LINK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "link.svg"),
            fullUpdate=False,
        )

        # Image
        actionController.getAction(polyactions.IMAGE_STR_ID).setFunc(self._insertImage)

        actionController.appendMenuItem(polyactions.IMAGE_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.IMAGE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "image.png"),
            fullUpdate=False,
        )

        # Horizontal line
        actionController.getAction(polyactions.HORLINE_STR_ID).setFunc(
            lambda param: self.replaceText("----")
        )

        actionController.appendMenuItem(polyactions.HORLINE_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.HORLINE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_horizontalrule.png"),
            fullUpdate=False,
        )

        # Текущая дата
        actionController.getAction(polyactions.CURRENT_DATE).setFunc(
            lambda param: insertCurrentDate(self.mainWindow, self.codeEditor, self._application)
        )

        actionController.appendMenuItem(polyactions.CURRENT_DATE, menu)
        actionController.appendToolbarButton(
            polyactions.CURRENT_DATE,
            toolbar,
            os.path.join(self.imagesDir, "date.svg"),
            fullUpdate=False,
        )

        # Code block
        actionController.getAction(polyactions.CODE_STR_ID).setFunc(
            lambda param: self.turnText("```\n", "\n```")
        )

        actionController.appendMenuItem(polyactions.CODE_STR_ID, menu)
        actionController.appendToolbarButton(
            polyactions.CODE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "code.svg"),
            fullUpdate=False,
        )

        self.toolsMenu.AppendSeparator()

        # Преобразовать некоторые символы в и их HTML-представление
        actionController.getAction(polyactions.HTML_ESCAPE_STR_ID).setFunc(
            lambda param: self.escapeHtml()
        )
        actionController.appendMenuItem(polyactions.HTML_ESCAPE_STR_ID, menu)

    def _addToolbarSeparator(self):
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_MARKDOWN_GENERAL]
        toolbar.AddSeparator()

    def _setHeading(self, prefix):
        editor = self._application.mainWindow.pagePanel.pageView.codeEditor

        old_sel_start = editor.GetSelectionStart()
        old_sel_end = editor.GetSelectionEnd()
        first_line, last_line = editor.GetSelectionLines()

        prefix_regex = re.compile("^(#+\\s+)*", re.U | re.M)

        editor.BeginUndoAction()

        for n in range(first_line, last_line + 1):
            line = editor.GetLine(n)
            if line.startswith(prefix):
                newline = line[len(prefix) :]
            else:
                newline = prefix_regex.sub(prefix, line, 1)
            editor.SetLine(n, newline)

        if old_sel_start != old_sel_end:
            new_sel_start = editor.GetLineStartPosition(first_line)
            new_sel_end = editor.GetLineEndPosition(last_line)
        else:
            new_sel_start = new_sel_end = editor.GetLineEndPosition(last_line)

        editor.SetSelection(new_sel_start, new_sel_end)

        editor.EndUndoAction()

    def _insertLink(self, params):
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        page = self._application.selectedPage
        assert page is not None

        with LinkDialog(self._application.mainWindow) as dlg:
            linkController = LinkDialogController(
                self._application, page, dlg, codeEditor.GetSelectedText()
            )

            if linkController.showDialog() == wx.ID_OK:
                link_text, reference = linkController.linkResult
                codeEditor.replaceText(link_text)

    def _insertImage(self, params):
        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        page = self._application.selectedPage
        assert page is not None

        with ImageDialog(self._application.mainWindow) as dlg:
            attachList = Attachment(page).getAttachRelative()
            controller = ImageDialogController(
                dlg, attachList, codeEditor.GetSelectedText()
            )
            if controller.showDialog() == wx.ID_OK:
                codeEditor.replaceText(controller.result)
