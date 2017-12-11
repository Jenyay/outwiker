# -*- coding: utf-8 -*-

import os

import wx

from outwiker.core.commands import insertCurrentDate
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.tabledialog import TableDialog
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.gui.toolbars.simpletoolbar import SimpleToolBar
from outwiker.pages.html.basehtmlpanel import (BaseHtmlPanel,
                                               EVT_PAGE_TAB_CHANGED)
from outwiker.pages.html.tabledialogcontroller import (
    TableDialogController,
    TableRowsDialogController
)
from .actions.autolinewrap import HtmlAutoLineWrap
from .actions.link import insertLink
from .actions.switchcoderesult import SwitchCodeResultAction
from outwiker.actions.polyactionsid import *


class HtmlPageView(BaseHtmlPanel):
    def __init__(self, parent, application):
        super(HtmlPageView, self).__init__(parent, application)

        self.__HTML_MENU_INDEX = 7
        self._menuName = _(u"HTML")

        self._toolbars = self._createToolbars()
        map(lambda toolbar: self.mainWindow.toolbars.addToolbar(toolbar),
            self._toolbars)

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
        ] + self._baseTextPolyactions

        # Список действий, которые нужно удалять с панелей и из меню.
        # А еще их надо дизаблить при переходе на вкладку просмотра результата
        # Не убираю пустой список, поскольку в будущем могут появиться
        # нестандартные действия, специфические только для HTML-страниц
        self.__htmlNotationActions = [
        ]

        self.__createCustomTools()
        self.mainWindow.UpdateAuiManager()

        self.Bind(EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)

    def _createToolbars(self):
        self._toolbar_general = SimpleToolBar(self.mainWindow,
                                              self.mainWindow.auiManager,
                                              u"html_general_toolbar",
                                              _(u"HTML"))

        self._toolbar_heading = SimpleToolBar(
            self.mainWindow,
            self.mainWindow.auiManager,
            u"html_heading_toolbar",
            _(u"Heading"))

        self._toolbar_font = SimpleToolBar(
            self.mainWindow,
            self.mainWindow.auiManager,
            u"html_font_toolbar",
            _(u"Font"))

        self._toolbar_align = SimpleToolBar(
            self.mainWindow,
            self.mainWindow.auiManager,
            u"html_align_toolbar",
            _(u"Align"))

        self._toolbar_table = SimpleToolBar(
            self.mainWindow,
            self.mainWindow.auiManager,
            u"html_table_toolbar",
            _(u"Table"))

        toolbars = [self._toolbar_general,
                    self._toolbar_heading,
                    self._toolbar_font,
                    self._toolbar_align,
                    self._toolbar_table,
                    ]

        return toolbars

    def getTextEditor(self):
        return HtmlTextEditor

    @property
    def toolsMenu(self):
        return self.__htmlMenu

    def onTabChanged(self, event):
        if self._currentpage is not None:
            if event.tab == self.RESULT_PAGE_INDEX:
                self._onSwitchToPreview()
            else:
                self._onSwitchToCode()

            self.savePageTab(self._currentpage)

        event.Skip()

    def Clear(self):
        self.Unbind(EVT_PAGE_TAB_CHANGED, handler=self.onTabChanged)

        self._removeActionTools()

        self.mainWindow.toolbars.updatePanesInfo()
        for toolbar in self._toolbars:
            self.mainWindow.toolbars.destroyToolBar(toolbar.name)

        super(HtmlPageView, self).Clear()

    def _removeActionTools(self):
        actionController = self._application.actionController

        # Удалим элементы меню
        map(lambda action: actionController.removeMenuItem(action.stringId),
            self.__htmlNotationActions)

        # Удалим элементы меню полиморфных действий
        map(lambda strid: actionController.removeMenuItem(strid),
            self.__polyActions)

        actionController.removeMenuItem(HtmlAutoLineWrap.stringId)
        actionController.removeMenuItem(SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        map(lambda action: actionController.removeToolbarButton(
            action.stringId),
            self.__htmlNotationActions)

        map(lambda strid: actionController.removeToolbarButton(strid),
            self.__polyActions)

        actionController.removeToolbarButton(HtmlAutoLineWrap.stringId)

        # Обнулим функции действия в полиморфных действиях
        map(lambda strid: actionController.getAction(strid).setFunc(None),
            self.__polyActions)

    def _enableActions(self, enabled):
        actionController = self._application.actionController

        map(lambda action: actionController.enableTools(action.stringId,
                                                        enabled),
            self.__htmlNotationActions)

        # Активируем / дизактивируем полиморфные действия
        map(lambda strid: actionController.enableTools(strid, enabled),
            self.__polyActions)

    def UpdateView(self, page):
        self.__updateLineWrapTools()
        BaseHtmlPanel.UpdateView(self, page)

    def __createLineWrapTools(self):
        """
        Create button and menu item to enable / disable lines wrap.
        """
        image = os.path.join(self.imagesDir, "linewrap.png")
        toolbar = self._toolbar_general
        actionController = self._application.actionController

        actionController.appendMenuCheckItem(HtmlAutoLineWrap.stringId,
                                             self.__htmlMenu)
        actionController.appendToolbarCheckButton(
            HtmlAutoLineWrap.stringId,
            toolbar,
            image,
            fullUpdate=False)
        self.__updateLineWrapTools()

    def __updateLineWrapTools(self):
        if self._currentpage is not None:
            self._application.actionController.check(
                HtmlAutoLineWrap.stringId,
                self._currentpage.autoLineWrap)

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

        self.__htmlMenu.AppendSubMenu(self.__headingMenu, _(u"Heading"))
        self.__htmlMenu.AppendSubMenu(self.__fontMenu, _(u"Font"))
        self.__htmlMenu.AppendSubMenu(self.__alignMenu, _(u"Alignment"))
        self.__htmlMenu.AppendSubMenu(self.__formatMenu, _(u"Formatting"))
        self.__htmlMenu.AppendSubMenu(self.__listMenu, _(u"Lists"))
        self.__htmlMenu.AppendSubMenu(self.__tableMenu, _(u"Tables"))

        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addTableTools()
        self.__addListTools()
        self.__addFormatTools()
        self._addSeparator()

        self.__addOtherTools()
        self._addRenderTools()

        self.mainWindow.mainMenu.Insert(self.__HTML_MENU_INDEX,
                                        self.__htmlMenu,
                                        self._menuName)

    def _addRenderTools(self):
        self._application.actionController.appendMenuItem(
            SwitchCodeResultAction.stringId,
            self.toolsMenu)

    def __addFontTools(self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self._toolbar_font
        menu = self.__fontMenu
        actionController = self._application.actionController

        # Полужирный шрифт
        actionController.getAction(BOLD_STR_ID).setFunc(
            lambda param: self.turnText(u"<b>", u"</b>"))

        actionController.appendMenuItem(BOLD_STR_ID, menu)
        actionController.appendToolbarButton(
            BOLD_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold.png"),
            fullUpdate=False)

        # Курсивный шрифт
        actionController.getAction(ITALIC_STR_ID).setFunc(
            lambda param: self.turnText(u"<i>", u"</i>"))

        actionController.appendMenuItem(ITALIC_STR_ID, menu)
        actionController.appendToolbarButton(
            ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_italic.png"),
            fullUpdate=False)

        # Полужирный курсивный шрифт
        actionController.getAction(BOLD_ITALIC_STR_ID).setFunc(
            lambda param: self.turnText(u"<b><i>", u"</i></b>"))

        actionController.appendMenuItem(BOLD_ITALIC_STR_ID, menu)
        actionController.appendToolbarButton(
            BOLD_ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold_italic.png"),
            fullUpdate=False)

        # Подчеркнутый шрифт
        actionController.getAction(UNDERLINE_STR_ID).setFunc(
            lambda param: self.turnText(u"<u>", u"</u>"))

        actionController.appendMenuItem(UNDERLINE_STR_ID, menu)
        actionController.appendToolbarButton(
            UNDERLINE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_underline.png"),
            fullUpdate=False)

        # Зачеркнутый шрифт
        actionController.getAction(STRIKE_STR_ID).setFunc(
            lambda param: self.turnText(u"<strike>", u"</strike>"))

        actionController.appendMenuItem(STRIKE_STR_ID, menu)
        actionController.appendToolbarButton(
            STRIKE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_strikethrough.png"),
            fullUpdate=False)

        # Нижний индекс
        actionController.getAction(SUBSCRIPT_STR_ID).setFunc(
            lambda param: self.turnText(u"<sub>", u"</sub>"))

        actionController.appendMenuItem(SUBSCRIPT_STR_ID, menu)
        actionController.appendToolbarButton(
            SUBSCRIPT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_subscript.png"),
            fullUpdate=False)

        # Верхний индекс
        actionController.getAction(SUPERSCRIPT_STR_ID).setFunc(
            lambda param: self.turnText(u"<sup>", u"</sup>"))

        actionController.appendMenuItem(SUPERSCRIPT_STR_ID, menu)
        actionController.appendToolbarButton(
            SUPERSCRIPT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_superscript.png"),
            fullUpdate=False)

    def __addAlignTools(self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbar = self._toolbar_align
        menu = self.__alignMenu
        actionController = self._application.actionController

        # Выравнивание по левому краю
        actionController.getAction(ALIGN_LEFT_STR_ID).setFunc(
            lambda param: self.turnText(u'<div align="left">', u'</div>'))

        actionController.appendMenuItem(
            ALIGN_LEFT_STR_ID,
            menu)
        actionController.appendToolbarButton(
            ALIGN_LEFT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_left.png"),
            fullUpdate=False)

        # Выравнивание по центру
        actionController.getAction(ALIGN_CENTER_STR_ID).setFunc(
            lambda param: self.turnText(u'<div align="center">', u'</div>'))

        actionController.appendMenuItem(ALIGN_CENTER_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_CENTER_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_center.png"),
            fullUpdate=False)

        # Выравнивание по правому краю
        actionController.getAction(ALIGN_RIGHT_STR_ID).setFunc(
            lambda param: self.turnText(u'<div align="right">', u'</div>'))

        actionController.appendMenuItem(ALIGN_RIGHT_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_RIGHT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_right.png"),
            fullUpdate=False)

        # Выравнивание по ширине
        actionController.getAction(ALIGN_JUSTIFY_STR_ID).setFunc(
            lambda param: self.turnText(u'<div align="justify">', u'</div>'))

        actionController.appendMenuItem(ALIGN_JUSTIFY_STR_ID, menu)
        actionController.appendToolbarButton(
            ALIGN_JUSTIFY_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_justify.png"),
            fullUpdate=False)

    def __addTableTools(self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbar = self._toolbar_table
        menu = self.__tableMenu
        actionController = self._application.actionController

        # Вставить таблицу
        actionController.getAction(TABLE_STR_ID).setFunc(self._insertTable)

        actionController.appendMenuItem(TABLE_STR_ID, menu)
        actionController.appendToolbarButton(
            TABLE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table.png"),
            fullUpdate=False)

        # Вставить строку таблицы
        actionController.getAction(TABLE_ROW_STR_ID).setFunc(
            self._insertTableRows
        )

        actionController.appendMenuItem(TABLE_ROW_STR_ID, menu)
        actionController.appendToolbarButton(
            TABLE_ROW_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table_insert_row.png"),
            fullUpdate=False)

        # Вставить ячейку таблицы
        actionController.getAction(TABLE_CELL_STR_ID).setFunc(
            lambda param: self.turnText(u'<td>', u'</td>'))

        actionController.appendMenuItem(TABLE_CELL_STR_ID, menu)
        actionController.appendToolbarButton(
            TABLE_CELL_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table_insert_cell.png"),
            fullUpdate=False)

    def __addListTools(self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self._toolbar_align
        menu = self.__listMenu
        actionController = self._application.actionController

        # Ненумерованный список
        actionController.getAction(LIST_BULLETS_STR_ID).setFunc(
            lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList(u'<ul>\n', u'</ul>', u'<li>', u'</li>'))

        actionController.appendMenuItem(LIST_BULLETS_STR_ID, menu)
        actionController.appendToolbarButton(
            LIST_BULLETS_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_list_bullets.png"),
            fullUpdate=False)

        # Нумерованный список
        actionController.getAction(LIST_NUMBERS_STR_ID).setFunc(
            lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList(u'<ol>\n', u'</ol>', u'<li>', u'</li>'))

        actionController.appendMenuItem(LIST_NUMBERS_STR_ID, menu)
        actionController.appendToolbarButton(
            LIST_NUMBERS_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_list_numbers.png"),
            fullUpdate=False)

    def __addHTools(self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self._toolbar_heading
        menu = self.__headingMenu
        actionController = self._application.actionController

        actionController.getAction(HEADING_1_STR_ID).setFunc(
            lambda param: self.turnText(u"<h1>", u"</h1>"))

        actionController.getAction(HEADING_2_STR_ID).setFunc(
            lambda param: self.turnText(u"<h2>", u"</h2>"))

        actionController.getAction(HEADING_3_STR_ID).setFunc(
            lambda param: self.turnText(u"<h3>", u"</h3>"))

        actionController.getAction(HEADING_4_STR_ID).setFunc(
            lambda param: self.turnText(u"<h4>", u"</h4>"))

        actionController.getAction(HEADING_5_STR_ID).setFunc(
            lambda param: self.turnText(u"<h5>", u"</h5>"))

        actionController.getAction(HEADING_6_STR_ID).setFunc(
            lambda param: self.turnText(u"<h6>", u"</h6>"))

        actionController.appendMenuItem(HEADING_1_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_1_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_1.png"),
            fullUpdate=False)

        actionController.appendMenuItem(HEADING_2_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_2_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_2.png"),
            fullUpdate=False)

        actionController.appendMenuItem(HEADING_3_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_3_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_3.png"),
            fullUpdate=False)

        actionController.appendMenuItem(HEADING_4_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_4_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_4.png"),
            fullUpdate=False)

        actionController.appendMenuItem(HEADING_5_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_5_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_5.png"),
            fullUpdate=False)

        actionController.appendMenuItem(HEADING_6_STR_ID, menu)
        actionController.appendToolbarButton(
            HEADING_6_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_6.png"),
            fullUpdate=False)

    def __addFormatTools(self):
        toolbar = self._toolbar_general
        menu = self.__formatMenu
        actionController = self._application.actionController

        # Preformat
        actionController.getAction(PREFORMAT_STR_ID).setFunc(
            lambda param: self.turnText(u"<pre>", u"</pre>"))
        actionController.appendMenuItem(PREFORMAT_STR_ID, menu)

        # Цитирование
        actionController.getAction(QUOTE_STR_ID).setFunc(
            lambda param: self.turnText(u"<blockquote>", u"</blockquote>"))

        actionController.appendMenuItem(QUOTE_STR_ID, menu)
        actionController.appendToolbarButton(
            QUOTE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "quote.png"),
            fullUpdate=False)

        # Mark
        actionController.getAction(MARK_STR_ID).setFunc(
            lambda param: self.turnText(u"<mark>", u"</mark>"))

        actionController.appendMenuItem(MARK_STR_ID, menu)
        actionController.appendToolbarButton(
            MARK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "mark.png"),
            fullUpdate=False)

        # Код
        actionController.getAction(CODE_STR_ID).setFunc(
            lambda param: self.turnText(u'<code>', u'</code>'))

        actionController.appendMenuItem(CODE_STR_ID, menu)
        actionController.appendToolbarButton(
            CODE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "code.png"),
            fullUpdate=False)

    def __addOtherTools(self):
        """
        Добавить остальные инструменты
        """
        toolbar = self._toolbar_general
        menu = self.__htmlMenu
        actionController = self._application.actionController

        # Вставить картинку
        actionController.getAction(IMAGE_STR_ID).setFunc(
            lambda param: self.turnText(u'<img src="', u'"/>'))

        actionController.appendMenuItem(IMAGE_STR_ID, menu)
        actionController.appendToolbarButton(
            IMAGE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "image.png"),
            fullUpdate=False)

        # Вставить ссылку
        actionController.getAction(LINK_STR_ID).setFunc(
            lambda param: insertLink(self._application))

        actionController.appendMenuItem(LINK_STR_ID, menu)
        actionController.appendToolbarButton(
            LINK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "link.png"),
            fullUpdate=False)

        # Вставить якорь
        actionController.getAction(ANCHOR_STR_ID).setFunc(
            lambda param: self.turnText(u'<a name="', u'"></a>'))

        actionController.appendMenuItem(ANCHOR_STR_ID, menu)
        actionController.appendToolbarButton(
            ANCHOR_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "anchor.png"),
            fullUpdate=False)

        # Вставить горизонтальную линию
        actionController.getAction(HORLINE_STR_ID).setFunc(
            lambda param: self.replaceText(u"<hr>"))

        actionController.appendMenuItem(HORLINE_STR_ID, menu)
        actionController.appendToolbarButton(
            HORLINE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_horizontalrule.png"),
            fullUpdate=False)

        # Вставка разрыва страницы
        actionController.getAction(LINE_BREAK_STR_ID).setFunc(
            lambda param: self.replaceText(u"<br>\n"))

        actionController.appendMenuItem(LINE_BREAK_STR_ID, menu)
        actionController.appendToolbarButton(
            LINE_BREAK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "linebreak.png"),
            fullUpdate=False)

        # Текущая дата
        actionController.getAction(CURRENT_DATE).setFunc(
            lambda param: insertCurrentDate(self.mainWindow,
                                            self.codeEditor))

        actionController.appendMenuItem(CURRENT_DATE, menu)
        actionController.appendToolbarButton(
            CURRENT_DATE,
            toolbar,
            os.path.join(self.imagesDir, "date.png"),
            fullUpdate=False)

        self.__htmlMenu.AppendSeparator()

        # Преобразовать символы в их HTML-представление
        actionController.getAction(HTML_ESCAPE_STR_ID).setFunc(
            lambda param: self.escapeHtml())
        actionController.appendMenuItem(HTML_ESCAPE_STR_ID, menu)

    def _addSeparator(self):
        toolbar = self._toolbar_general
        toolbar.AddSeparator()

    def removeGui(self):
        super(HtmlPageView, self).removeGui()
        mainMenu = self._application.mainWindow.mainMenu
        index = mainMenu.FindMenu(self._menuName)
        assert index != wx.NOT_FOUND

        mainMenu.Remove(index)

    def _insertTable(self, param):
        editor = self.codeEditor
        parent = self._application.mainWindow

        with TableDialog(parent) as dlg:
            controller = TableDialogController(dlg, self._application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText(result)

    def _insertTableRows(self, param):
        editor = self.codeEditor
        parent = self._application.mainWindow

        with TableRowsDialog(parent) as dlg:
            controller = TableRowsDialogController(dlg,
                                                   self._application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText(result)
