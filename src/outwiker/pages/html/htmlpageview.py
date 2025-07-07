# -*- coding: utf-8 -*-

import logging
import os

import wx

from outwiker.actions.polyactionsid import *
from outwiker.app.services.texteditor import insertCurrentDate
from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW, PAGE_ATTACH_DIR
from outwiker.core.system import getBuiltinImagePath
from outwiker.gui.defines import TOOLBAR_ORDER_TEXT
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from outwiker.pages.html.guitools import insertTable, insertTableRows

from .actions.autolinewrap import HtmlAutoLineWrap
from .actions.link import insertLink
from .actions.switchcoderesult import SwitchCodeResultAction
from . import defines


logger = logging.getLogger("outwiker.pages.html.htmlpageview")


class HtmlPageView(BaseHtmlPanel):
    def __init__(self, parent, application):
        logger.debug("HtmlPageView creation started")
        super().__init__(parent, application)

        self.__HTML_MENU_INDEX = 7
        self._menuName = _("HTML")

        self._toolbars = [
            (defines.TOOLBAR_HTML_GENERAL, _("HTML")),
            (defines.TOOLBAR_HTML_HEADING, _("Heading")),
            (defines.TOOLBAR_HTML_FONT, _("Font")),
            (defines.TOOLBAR_HTML_ALIGN, _("Align")),
            (defines.TOOLBAR_HTML_TABLE, _("Table")),
        ]
        for toolbar_id, title in self._toolbars:
            self.mainWindow.toolbars.createToolBar(
                toolbar_id, title, order=TOOLBAR_ORDER_TEXT
            )

        # Список используемых полиморфных действий
        self.__polyActions = [
            BOLD_STR_ID,
            ITALIC_STR_ID,
            BOLD_ITALIC_STR_ID,
            UNDERLINE_STR_ID,
            STRIKE_STR_ID,
            SUBSCRIPT_STR_ID,
            SUPERSCRIPT_STR_ID,
            ALIGN_LEFT_STR_ID,
            ALIGN_CENTER_STR_ID,
            ALIGN_RIGHT_STR_ID,
            ALIGN_JUSTIFY_STR_ID,
            HEADING_1_STR_ID,
            HEADING_2_STR_ID,
            HEADING_3_STR_ID,
            HEADING_4_STR_ID,
            HEADING_5_STR_ID,
            HEADING_6_STR_ID,
            PREFORMAT_STR_ID,
            CODE_STR_ID,
            ANCHOR_STR_ID,
            HORLINE_STR_ID,
            LINK_STR_ID,
            LIST_BULLETS_STR_ID,
            LIST_NUMBERS_STR_ID,
            LINE_BREAK_STR_ID,
            HTML_ESCAPE_STR_ID,
            TABLE_STR_ID,
            TABLE_ROW_STR_ID,
            TABLE_CELL_STR_ID,
            QUOTE_STR_ID,
            IMAGE_STR_ID,
            CURRENT_DATE,
            MARK_STR_ID,
            COMMENT_STR_ID,
        ] + self._baseTextPolyactions

        # Список действий, которые нужно удалять с панелей и из меню.
        # А еще их надо дизаблить при переходе на вкладку просмотра результата
        # Не убираю пустой список, поскольку в будущем могут появиться
        # нестандартные действия, специфические только для HTML-страниц
        self.__htmlNotationActions = []

        self.__createCustomTools()
        self.mainWindow.UpdateAuiManager()

        self._application.onPageModeChange += self.onTabChanged
        logger.debug("HtmlPageView creation ended")

    def getTextEditor(self):
        return HtmlTextEditor

    @property
    def toolsMenu(self):
        return self.__htmlMenu

    def onTabChanged(self, page, params):
        if self._currentpage is not None:
            if params.pagemode == PAGE_MODE_PREVIEW:
                self._onSwitchToPreview()
            elif params.pagemode == PAGE_MODE_TEXT:
                self._onSwitchToCode()
            else:
                assert False

            self.savePageTab(self._currentpage)

    def Clear(self):
        self._application.onPageModeChange -= self.onTabChanged
        self._removeActionTools()

        for toolbar_info in self._toolbars:
            self.mainWindow.toolbars.destroyToolBar(toolbar_info[0])

        super().Clear()

    def _removeActionTools(self):
        actionController = self._application.actionController

        # Удалим элементы меню
        for action in self.__htmlNotationActions:
            actionController.removeMenuItem(action.stringId)

        # Удалим элементы меню полиморфных действий
        for strid in self.__polyActions:
            actionController.removeMenuItem(strid)

        actionController.removeMenuItem(HtmlAutoLineWrap.stringId)
        actionController.removeMenuItem(SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        for action in self.__htmlNotationActions:
            actionController.removeToolbarButton(action.stringId)

        for strid in self.__polyActions:
            actionController.removeToolbarButton(strid)

        actionController.removeToolbarButton(HtmlAutoLineWrap.stringId)

        # Обнулим функции действия в полиморфных действиях
        for strid in self.__polyActions:
            actionController.getAction(strid).setFunc(None)

    def _enableActions(self, enabled):
        actionController = self._application.actionController

        for action in self.__htmlNotationActions:
            actionController.enableTools(action.stringId, enabled)

        # Активируем / дизактивируем полиморфные действия
        for strid in self.__polyActions:
            actionController.enableTools(strid, enabled)

    def UpdateView(self, page):
        self.__updateLineWrapTools()
        BaseHtmlPanel.UpdateView(self, page)

    def __createLineWrapTools(self):
        """
        Create button and menu item to enable / disable lines wrap.
        """
        image = os.path.join(self.imagesDir, "linewrap.png")
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_GENERAL]
        actionController = self._application.actionController

        actionController.appendMenuCheckItem(HtmlAutoLineWrap.stringId, self.__htmlMenu)
        actionController.appendToolbarCheckButton(
            HtmlAutoLineWrap.stringId, toolbar, image, fullUpdate=False
        )
        self.__updateLineWrapTools()

    def __updateLineWrapTools(self):
        if self._currentpage is not None:
            self._application.actionController.check(
                HtmlAutoLineWrap.stringId, self._currentpage.autoLineWrap
            )

    def __createCustomTools(self):
        """
        Создать кнопки и меню для данного типа страниц
        """
        assert self.mainWindow is not None

        self.__htmlMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__tableMenu = wx.Menu()

        self.__createLineWrapTools()
        self.toolsMenu.AppendSeparator()

        self.__htmlMenu.AppendSubMenu(self.__headingMenu, _("Heading"))
        self.__htmlMenu.AppendSubMenu(self.__fontMenu, _("Font"))
        self.__htmlMenu.AppendSubMenu(self.__alignMenu, _("Alignment"))
        self.__htmlMenu.AppendSubMenu(self.__formatMenu, _("Formatting"))
        self.__htmlMenu.AppendSubMenu(self.__listMenu, _("Lists"))
        self.__htmlMenu.AppendSubMenu(self.__tableMenu, _("Tables"))

        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addTableTools()
        self.__addListTools()
        self.__addFormatTools()
        self._addSeparator()

        self.__addOtherTools()
        self._addRenderTools()

        mainMenu = self.mainWindow.menuController.getRootMenu()
        mainMenu.Insert(self.__HTML_MENU_INDEX, self.__htmlMenu, self._menuName)

    def _addRenderTools(self):
        self._application.actionController.appendMenuItem(
            SwitchCodeResultAction.stringId, self.toolsMenu
        )

    def __addFontTools(self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_FONT]
        menu = self.__fontMenu
        actionController = self._application.actionController

        # Полужирный шрифт
        actionController.getAction(BOLD_STR_ID).setFunc(
            lambda param: self.turnText("<b>", "</b>")
        )

        actionController.appendMenuItem(BOLD_STR_ID, menu)
        actionController.appendToolbarButton(
            BOLD_STR_ID,
            toolbar,
            getBuiltinImagePath("text_bold.svg"),
            fullUpdate=False,
        )

        # Курсивный шрифт
        actionController.getAction(ITALIC_STR_ID).setFunc(
            lambda param: self.turnText("<i>", "</i>")
        )

        actionController.appendMenuItem(ITALIC_STR_ID, menu)
        actionController.appendToolbarButton(
            ITALIC_STR_ID,
            toolbar,
            getBuiltinImagePath("text_italic.svg"),
            fullUpdate=False,
        )

        # Полужирный курсивный шрифт
        actionController.getAction(BOLD_ITALIC_STR_ID).setFunc(
            lambda param: self.turnText("<b><i>", "</i></b>")
        )

        actionController.appendMenuItem(BOLD_ITALIC_STR_ID, menu)
        actionController.appendToolbarButton(
            BOLD_ITALIC_STR_ID,
            toolbar,
            getBuiltinImagePath("text_bold_italic.svg"),
            fullUpdate=False,
        )

        # Подчеркнутый шрифт
        actionController.getAction(UNDERLINE_STR_ID).setFunc(
            lambda param: self.turnText("<u>", "</u>")
        )

        actionController.appendMenuItem(UNDERLINE_STR_ID, menu)
        actionController.appendToolbarButton(
            UNDERLINE_STR_ID,
            toolbar,
            getBuiltinImagePath("text_underline.svg"),
            fullUpdate=False,
        )

        # Зачеркнутый шрифт
        actionController.getAction(STRIKE_STR_ID).setFunc(
            lambda param: self.turnText("<strike>", "</strike>")
        )

        actionController.appendMenuItem(STRIKE_STR_ID, menu)
        actionController.appendToolbarButton(
            STRIKE_STR_ID,
            toolbar,
            getBuiltinImagePath("text_strikethrough.svg"),
            fullUpdate=False,
        )

        # Нижний индекс
        actionController.getAction(SUBSCRIPT_STR_ID).setFunc(
            lambda param: self.turnText("<sub>", "</sub>")
        )

        actionController.appendMenuItem(SUBSCRIPT_STR_ID, menu)
        actionController.appendToolbarButton(
            SUBSCRIPT_STR_ID,
            toolbar,
            getBuiltinImagePath("text_subscript.svg"),
            fullUpdate=False,
        )

        # Верхний индекс
        actionController.getAction(SUPERSCRIPT_STR_ID).setFunc(
            lambda param: self.turnText("<sup>", "</sup>")
        )

        actionController.appendMenuItem(SUPERSCRIPT_STR_ID, menu)
        actionController.appendToolbarButton(
            SUPERSCRIPT_STR_ID,
            toolbar,
            getBuiltinImagePath("text_superscript.svg"),
            fullUpdate=False,
        )

    def __addAlignTools(self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_ALIGN]
        menu = self.__alignMenu
        actionController = self._application.actionController

        # Выравнивание по левому краю
        actionController.getAction(ALIGN_LEFT_STR_ID).setFunc(
            lambda param: self.turnText('<div align="left">', "</div>")
        )

        actionController.appendMenuItem(ALIGN_LEFT_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_LEFT_STR_ID,
            toolbar,
            getBuiltinImagePath("text_align_left.svg"),
            fullUpdate=False,
        )

        # Выравнивание по центру
        actionController.getAction(ALIGN_CENTER_STR_ID).setFunc(
            lambda param: self.turnText('<div align="center">', "</div>")
        )

        actionController.appendMenuItem(ALIGN_CENTER_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_CENTER_STR_ID,
            toolbar,
            getBuiltinImagePath("text_align_center.svg"),
            fullUpdate=False,
        )

        # Выравнивание по правому краю
        actionController.getAction(ALIGN_RIGHT_STR_ID).setFunc(
            lambda param: self.turnText('<div align="right">', "</div>")
        )

        actionController.appendMenuItem(ALIGN_RIGHT_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_RIGHT_STR_ID,
            toolbar,
            getBuiltinImagePath("text_align_right.svg"),
            fullUpdate=False,
        )

        # Выравнивание по ширине
        actionController.getAction(ALIGN_JUSTIFY_STR_ID).setFunc(
            lambda param: self.turnText('<div align="justify">', "</div>")
        )

        actionController.appendMenuItem(ALIGN_JUSTIFY_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_JUSTIFY_STR_ID,
            toolbar,
            getBuiltinImagePath("text_align_justify.svg"),
            fullUpdate=False,
        )

    def __addTableTools(self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_TABLE]
        menu = self.__tableMenu
        actionController = self._application.actionController

        # Вставить таблицу
        actionController.getAction(TABLE_STR_ID).setFunc(self._insertTable)

        actionController.appendMenuItem(TABLE_STR_ID, menu)
        actionController.appendToolbarButton(
            TABLE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table.png"),
            fullUpdate=False,
        )

        # Вставить строку таблицы
        actionController.getAction(TABLE_ROW_STR_ID).setFunc(self._insertTableRows)

        actionController.appendMenuItem(TABLE_ROW_STR_ID, menu)
        actionController.appendToolbarButton(
            TABLE_ROW_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table_insert_row.png"),
            fullUpdate=False,
        )

        # Вставить ячейку таблицы
        actionController.getAction(TABLE_CELL_STR_ID).setFunc(
            lambda param: self.turnText("<td>", "</td>")
        )

        actionController.appendMenuItem(TABLE_CELL_STR_ID, menu)
        actionController.appendToolbarButton(
            TABLE_CELL_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table_insert_cell.png"),
            fullUpdate=False,
        )

    def __addListTools(self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_ALIGN]
        menu = self.__listMenu
        actionController = self._application.actionController

        # Ненумерованный список
        actionController.getAction(LIST_BULLETS_STR_ID).setFunc(
            lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList(
                "<ul>\n", "</ul>", "<li>", "</li>"
            )
        )

        actionController.appendMenuItem(LIST_BULLETS_STR_ID, menu)
        actionController.appendToolbarButton(
            LIST_BULLETS_STR_ID,
            toolbar,
            getBuiltinImagePath("text_list_bullets.svg"),
            fullUpdate=False,
        )

        # Нумерованный список
        actionController.getAction(LIST_NUMBERS_STR_ID).setFunc(
            lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList(
                "<ol>\n", "</ol>", "<li>", "</li>"
            )
        )

        actionController.appendMenuItem(LIST_NUMBERS_STR_ID, menu)
        actionController.appendToolbarButton(
            LIST_NUMBERS_STR_ID,
            toolbar,
            getBuiltinImagePath("text_list_numbers.svg"),
            fullUpdate=False,
        )

    def __addHTools(self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_HEADING]
        menu = self.__headingMenu
        actionController = self._application.actionController

        actionController.getAction(HEADING_1_STR_ID).setFunc(
            lambda param: self.turnText("<h1>", "</h1>")
        )

        actionController.getAction(HEADING_2_STR_ID).setFunc(
            lambda param: self.turnText("<h2>", "</h2>")
        )

        actionController.getAction(HEADING_3_STR_ID).setFunc(
            lambda param: self.turnText("<h3>", "</h3>")
        )

        actionController.getAction(HEADING_4_STR_ID).setFunc(
            lambda param: self.turnText("<h4>", "</h4>")
        )

        actionController.getAction(HEADING_5_STR_ID).setFunc(
            lambda param: self.turnText("<h5>", "</h5>")
        )

        actionController.getAction(HEADING_6_STR_ID).setFunc(
            lambda param: self.turnText("<h6>", "</h6>")
        )

        actionController.appendMenuItem(HEADING_1_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_1_STR_ID,
            toolbar,
            getBuiltinImagePath("text_heading_1.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(HEADING_2_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_2_STR_ID,
            toolbar,
            getBuiltinImagePath("text_heading_2.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(HEADING_3_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_3_STR_ID,
            toolbar,
            getBuiltinImagePath("text_heading_3.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(HEADING_4_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_4_STR_ID,
            toolbar,
            getBuiltinImagePath("text_heading_4.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(HEADING_5_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_5_STR_ID,
            toolbar,
            getBuiltinImagePath("text_heading_5.svg"),
            fullUpdate=False,
        )

        actionController.appendMenuItem(HEADING_6_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_6_STR_ID,
            toolbar,
            getBuiltinImagePath("text_heading_6.svg"),
            fullUpdate=False,
        )

    def __addFormatTools(self):
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_GENERAL]
        menu = self.__formatMenu
        actionController = self._application.actionController

        # Preformat
        actionController.getAction(PREFORMAT_STR_ID).setFunc(
            lambda param: self.turnText("<pre>", "</pre>")
        )
        actionController.appendMenuItem(PREFORMAT_STR_ID, menu)

        # Comment
        actionController.getAction(COMMENT_STR_ID).setFunc(
            lambda param: self.turnText("<!--", "-->")
        )
        actionController.appendMenuItem(COMMENT_STR_ID, menu)
        actionController.appendToolbarButton(
            COMMENT_STR_ID,
            toolbar,
            getBuiltinImagePath("comment.svg"),
            fullUpdate=False,
        )

        # Цитирование
        actionController.getAction(QUOTE_STR_ID).setFunc(
            lambda param: self.turnText("<blockquote>", "</blockquote>")
        )

        actionController.appendMenuItem(QUOTE_STR_ID, menu)
        actionController.appendToolbarButton(
            QUOTE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "quote.svg"),
            fullUpdate=False,
        )

        # Mark
        actionController.getAction(MARK_STR_ID).setFunc(
            lambda param: self.turnText("<mark>", "</mark>")
        )

        actionController.appendMenuItem(MARK_STR_ID, menu)
        actionController.appendToolbarButton(
            MARK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "mark.svg"),
            fullUpdate=False,
        )

        # Код
        actionController.getAction(CODE_STR_ID).setFunc(
            lambda param: self.turnText("<code>", "</code>")
        )

        actionController.appendMenuItem(CODE_STR_ID, menu)
        actionController.appendToolbarButton(
            CODE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "code.svg"),
            fullUpdate=False,
        )

    def __addOtherTools(self):
        """
        Добавить остальные инструменты
        """
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_GENERAL]
        menu = self.__htmlMenu
        actionController = self._application.actionController

        # Вставить картинку
        actionController.getAction(IMAGE_STR_ID).setFunc(
            lambda param: self.turnText('<img src="', '"/>')
        )

        actionController.appendMenuItem(IMAGE_STR_ID, menu)
        actionController.appendToolbarButton(
            IMAGE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "picture.svg"),
            fullUpdate=False,
        )
        
        # Текущая дата
        actionController.getAction(CURRENT_DATE).setFunc(
            lambda param: insertCurrentDate(self.mainWindow, self.codeEditor, self._application)
        )

        actionController.appendMenuItem(CURRENT_DATE, menu)
        actionController.appendToolbarButton(
            CURRENT_DATE,
            toolbar,
            getBuiltinImagePath("date.svg"),
            fullUpdate=False,
        )
        
        # Вставить якорь
        actionController.getAction(ANCHOR_STR_ID).setFunc(
            lambda param: self.turnText('<a name="', '"></a>')
        )

        actionController.appendMenuItem(ANCHOR_STR_ID, menu)
        actionController.appendToolbarButton(
            ANCHOR_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "anchor.svg"),
            fullUpdate=False,
        )

        # Вставить ссылку
        actionController.getAction(LINK_STR_ID).setFunc(
            lambda param: insertLink(self._application)
        )

        actionController.appendMenuItem(LINK_STR_ID, menu)
        actionController.appendToolbarButton(
            LINK_STR_ID,
            toolbar,
            getBuiltinImagePath("link.svg"),
            fullUpdate=False,
        )

        # Вставить горизонтальную линию
        actionController.getAction(HORLINE_STR_ID).setFunc(
            lambda param: self.replaceText("<hr>")
        )

        actionController.appendMenuItem(HORLINE_STR_ID, menu)
        actionController.appendToolbarButton(
            HORLINE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_horline.svg"),
            fullUpdate=False,
        )

        # Вставка разрыва страницы
        actionController.getAction(LINE_BREAK_STR_ID).setFunc(
            lambda param: self.replaceText("<br>\n")
        )

        actionController.appendMenuItem(LINE_BREAK_STR_ID, menu)
        actionController.appendToolbarButton(
            LINE_BREAK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "linebreak.svg"),
            fullUpdate=False,
        )

        self.__htmlMenu.AppendSeparator()

        # Преобразовать символы в их HTML-представление
        actionController.getAction(HTML_ESCAPE_STR_ID).setFunc(
            lambda param: self.escapeHtml()
        )
        actionController.appendMenuItem(HTML_ESCAPE_STR_ID, menu)

    def _addSeparator(self):
        toolbar = self._application.mainWindow.toolbars[defines.TOOLBAR_HTML_GENERAL]
        toolbar.AddSeparator()

    def removeGui(self):
        super(HtmlPageView, self).removeGui()
        mainMenu = self.mainWindow.menuController.getRootMenu()
        index = mainMenu.FindMenu(self._menuName)
        assert index != wx.NOT_FOUND

        mainMenu.Remove(index)

    def _insertTable(self, param):
        insertTable(self._application, self.codeEditor)

    def _insertTableRows(self, param):
        insertTableRows(self._application, self.codeEditor)

    def _getAttachString(self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при
        вставке выбранных прикрепленных файлов из панели вложений
        """
        return " ".join([PAGE_ATTACH_DIR + "/" + fname for fname in fnames])
