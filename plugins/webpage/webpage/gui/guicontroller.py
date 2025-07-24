# -*- coding: utf-8 -*-

import os

import wx

from outwiker.api.app.application import getImagesDir
from outwiker.api.app.texteditor import insertCurrentDate
from outwiker.api.core.events import EVENT_PRIORITY_DEFAULT, pagetype
from outwiker.api.gui.actions import polyactions
from outwiker.api.pages.html.actions import SwitchCodeResultAction
from outwiker.api.pages.html.guitools import insertLink, insertTable, insertTableRows

from ..i18n import get_

from ..actions.downloadaction import (
    CreateChildWebPageAction,
    CreateSiblingWebPageAction,
)
from ..actions.opensourceurl import OpenSourceURLAction
from ..actions.showpageinfo import ShowPageInfoAction
from ..actions.disablescripts import DisableScriptsAction
from ..actions.copysourceurl import CopySourceURLToClipboardAction
from ..defines import PAGE_TYPE_STRING
from ..misc import polyActions
from ..webnotepage import WebPageFactory
from .defines import TOOLBAR_WEBPAGE


class GuiController:
    """Controller for creation and destroying GUI"""

    def __init__(self, application):
        self._application = application

        self._addedWebPageMenuItems = False
        self.imagesDir = getImagesDir()
        self._MENU_INDEX = 5
        self._menuName = None
        self._menu = None

    def initialize(self):
        global _
        _ = get_()

        self._application.onPageViewDestroy += self._onPageViewDestroy
        self._application.onPageViewCreate += self._onPageViewCreate
        self._application.onPageSelect.bind(
            self._onPageSelect, EVENT_PRIORITY_DEFAULT - 10
        )

        self._menuName = _("Web page")
        self._createMenu()

    def destroy(self):
        self._application.onPageViewDestroy -= self._onPageViewDestroy
        self._application.onPageViewCreate -= self._onPageViewCreate
        self._application.onPageSelect -= self._onPageSelect

        self._removeGui()

    @pagetype(PAGE_TYPE_STRING)
    def _onPageSelect(self, page):
        page_adapter = WebPageFactory().createPageAdapter(page)
        self._application.actionController.check(
            DisableScriptsAction.stringId, page_adapter.disableScripts
        )

    def _onPageViewCreate(self, page):
        assert page is not None
        self._createMenu()
        if page.getTypeString() == PAGE_TYPE_STRING:
            self._addWebPageGui()

    @pagetype(PAGE_TYPE_STRING)
    def _onPageViewDestroy(self, page):
        self._removeGui()
        self._createMenu()

    def _removeGui(self):
        mainWindow = self._application.mainWindow
        if mainWindow is not None:
            actionController = self._application.actionController

            actionController.removeMenuItem(CreateChildWebPageAction.stringId)

            actionController.removeToolbarButton(CreateChildWebPageAction.stringId)

            actionController.removeMenuItem(CreateSiblingWebPageAction.stringId)

            actionController.removeToolbarButton(CreateSiblingWebPageAction.stringId)

            self._removeWebPageGui()
            self._removeMenu()

    def _removeMenu(self):
        if self._menu is not None:
            mainMenu = self._application.mainWindow.menuController.getRootMenu()
            index = mainMenu.FindMenu(self._menuName)
            assert index != wx.NOT_FOUND

            mainMenu.Remove(index)
            self._menu = None

    def _addWebPageGui(self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None and not self._addedWebPageMenuItems:
            controller = self._application.actionController

            mainWindow.toolbars.createToolBar(TOOLBAR_WEBPAGE, _("Web Page"))

            self._menu.AppendSeparator()

            openSourceAction = OpenSourceURLAction(self._application)
            controller.appendMenuItem(openSourceAction.stringId, self._menu)

            copySourceUrlAction = CopySourceURLToClipboardAction(self._application)

            controller.appendMenuItem(copySourceUrlAction.stringId, self._menu)

            showInfoAction = ShowPageInfoAction(self._application)
            controller.appendMenuItem(showInfoAction.stringId, self._menu)

            self._addDisableScriptsTools()
            self._addToolbarSeparator()

            self._createWebPageMenu()

            self._addFontTools()
            self._addToolbarSeparator()

            self._addAlignTools()
            self._addToolbarSeparator()

            self._addHTools()
            self._addToolbarSeparator()

            self._addTableTools()
            self._addToolbarSeparator()

            self._addListTools()
            self._addToolbarSeparator()

            self._addFormatTools()
            self._addOtherTools()
            self._addRenderTools()

            self._application.mainWindow.UpdateAuiManager()

            self._addedWebPageMenuItems = True

    def _removeWebPageGui(self):
        if self._addedWebPageMenuItems:
            actionController = self._application.actionController

            actionController.removeMenuItem(OpenSourceURLAction.stringId)
            actionController.removeMenuItem(CopySourceURLToClipboardAction.stringId)
            actionController.removeMenuItem(ShowPageInfoAction.stringId)
            actionController.removeMenuItem(SwitchCodeResultAction.stringId)
            actionController.removeMenuItem(DisableScriptsAction.stringId)

            self._removePolyActionTools()
            if TOOLBAR_WEBPAGE in self._application.mainWindow.toolbars:
                actionController.removeToolbarButton(SwitchCodeResultAction.stringId)

                actionController.removeToolbarButton(DisableScriptsAction.stringId)

                self._application.mainWindow.toolbars.destroyToolBar(TOOLBAR_WEBPAGE)

            self._menu.DestroyItem(self._headingMenuItem)
            self._menu.DestroyItem(self._fontMenuItem)
            self._menu.DestroyItem(self._alignMenuItem)
            self._menu.DestroyItem(self._formatMenuItem)
            self._menu.DestroyItem(self._listMenuItem)
            self._menu.DestroyItem(self._tableMenuItem)

            self._addedWebPageMenuItems = False

    def _removePolyActionTools(self):
        actionController = self._application.actionController

        # Удалим элементы меню полиморфных действий
        for strid in polyActions:
            actionController.removeMenuItem(strid)

        # Удалим кнопки с панелей инструментов
        if TOOLBAR_WEBPAGE in self._application.mainWindow.toolbars:
            for strid in polyActions:
                actionController.removeToolbarButton(strid)

        # Обнулим функции действия в полиморфных действиях
        for strid in polyActions:
            actionController.getAction(strid).setFunc(None)

    def _createMenu(self):
        if self._application.mainWindow is not None and self._menu is None:
            self._menu = wx.Menu("")
            mainMenu = self._application.mainWindow.menuController.getRootMenu()
            mainMenu.Insert(self._MENU_INDEX, self._menu, self._menuName)
            self._createSiblingWebPageAction()
            self._createChildWebPageAction()

    def _createWebPageMenu(self):
        self._headingMenu = wx.Menu()
        self._fontMenu = wx.Menu()
        self._alignMenu = wx.Menu()
        self._formatMenu = wx.Menu()
        self._listMenu = wx.Menu()
        self._tableMenu = wx.Menu()

        self.toolsMenu.AppendSeparator()

        self._headingMenuItem = self._menu.AppendSubMenu(
            self._headingMenu, _("Heading")
        )

        self._fontMenuItem = self._menu.AppendSubMenu(self._fontMenu, _("Font"))

        self._alignMenuItem = self._menu.AppendSubMenu(self._alignMenu, _("Alignment"))

        self._formatMenuItem = self._menu.AppendSubMenu(
            self._formatMenu, _("Formatting")
        )

        self._listMenuItem = self._menu.AppendSubMenu(self._listMenu, _("Lists"))

        self._tableMenuItem = self._menu.AppendSubMenu(self._tableMenu, _("Tables"))

    @property
    def toolsMenu(self):
        return self._menu

    def _addRenderTools(self):
        self._application.actionController.appendMenuItem(
            SwitchCodeResultAction.stringId, self.toolsMenu
        )
        self._application.actionController.appendToolbarButton(
            SwitchCodeResultAction.stringId,
            self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE],
            os.path.join(self.imagesDir, "render.png"),
            fullUpdate=False,
        )

    def _addDisableScriptsTools(self):
        """
        Create button and menu item to enable / disable scripts.
        """
        image = self.getImagePath("script-delete.png")
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self.toolsMenu

        self._application.actionController.appendMenuCheckItem(
            DisableScriptsAction.stringId, menu
        )
        self._application.actionController.appendToolbarCheckButton(
            DisableScriptsAction.stringId, toolbar, image, fullUpdate=False
        )

    def _addFontTools(self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._fontMenu

        # Полужирный шрифт
        self._application.actionController.getAction(polyactions.BOLD_STR_ID).setFunc(
            lambda param: self.turnText("<b>", "</b>")
        )

        self._application.actionController.appendMenuItem(polyactions.BOLD_STR_ID, menu)
        self._application.actionController.appendToolbarButton(
            polyactions.BOLD_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold.svg"),
            fullUpdate=False,
        )

        # Курсивный шрифт
        self._application.actionController.getAction(polyactions.ITALIC_STR_ID).setFunc(
            lambda param: self.turnText("<i>", "</i>")
        )

        self._application.actionController.appendMenuItem(
            polyactions.ITALIC_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_italic.svg"),
            fullUpdate=False,
        )

        # Полужирный курсивный шрифт
        self._application.actionController.getAction(
            polyactions.BOLD_ITALIC_STR_ID
        ).setFunc(lambda param: self.turnText("<b><i>", "</i></b>"))

        self._application.actionController.appendMenuItem(
            polyactions.BOLD_ITALIC_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.BOLD_ITALIC_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_bold_italic.svg"),
            fullUpdate=False,
        )

        # Подчеркнутый шрифт
        self._application.actionController.getAction(
            polyactions.UNDERLINE_STR_ID
        ).setFunc(lambda param: self.turnText("<u>", "</u>"))

        self._application.actionController.appendMenuItem(
            polyactions.UNDERLINE_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.UNDERLINE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_underline.svg"),
            fullUpdate=False,
        )

        # Зачеркнутый шрифт
        self._application.actionController.getAction(polyactions.STRIKE_STR_ID).setFunc(
            lambda param: self.turnText("<strike>", "</strike>")
        )

        self._application.actionController.appendMenuItem(
            polyactions.STRIKE_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.STRIKE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_strikethrough.svg"),
            fullUpdate=False,
        )

        # Нижний индекс
        self._application.actionController.getAction(
            polyactions.SUBSCRIPT_STR_ID
        ).setFunc(lambda param: self.turnText("<sub>", "</sub>"))

        self._application.actionController.appendMenuItem(
            polyactions.SUBSCRIPT_STR_ID, menu
        )

        self._application.actionController.appendToolbarButton(
            polyactions.SUBSCRIPT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_subscript.svg"),
            fullUpdate=False,
        )

        # Верхний индекс
        self._application.actionController.getAction(
            polyactions.SUPERSCRIPT_STR_ID
        ).setFunc(lambda param: self.turnText("<sup>", "</sup>"))

        self._application.actionController.appendMenuItem(
            polyactions.SUPERSCRIPT_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.SUPERSCRIPT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_superscript.svg"),
            fullUpdate=False,
        )

    def _addAlignTools(self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._alignMenu

        # Выравнивание по левому краю
        self._application.actionController.getAction(
            polyactions.ALIGN_LEFT_STR_ID
        ).setFunc(lambda param: self.turnText('<div align="left">', "</div>"))

        self._application.actionController.appendMenuItem(
            polyactions.ALIGN_LEFT_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.ALIGN_LEFT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_left.svg"),
            fullUpdate=False,
        )

        # Выравнивание по центру
        self._application.actionController.getAction(
            polyactions.ALIGN_CENTER_STR_ID
        ).setFunc(lambda param: self.turnText('<div align="center">', "</div>"))

        self._application.actionController.appendMenuItem(
            polyactions.ALIGN_CENTER_STR_ID, menu
        )

        self._application.actionController.appendToolbarButton(
            polyactions.ALIGN_CENTER_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_center.svg"),
            fullUpdate=False,
        )

        # Выравнивание по правому краю
        self._application.actionController.getAction(
            polyactions.ALIGN_RIGHT_STR_ID
        ).setFunc(lambda param: self.turnText('<div align="right">', "</div>"))

        self._application.actionController.appendMenuItem(
            polyactions.ALIGN_RIGHT_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.ALIGN_RIGHT_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_right.svg"),
            fullUpdate=False,
        )

        # Выравнивание по ширине
        self._application.actionController.getAction(
            polyactions.ALIGN_JUSTIFY_STR_ID
        ).setFunc(lambda param: self.turnText('<div align="justify">', "</div>"))

        self._application.actionController.appendMenuItem(
            polyactions.ALIGN_JUSTIFY_STR_ID, menu
        )

        self._application.actionController.appendToolbarButton(
            polyactions.ALIGN_JUSTIFY_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_align_justify.svg"),
            fullUpdate=False,
        )

    def _addTableTools(self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._tableMenu

        # Вставить таблицу
        self._application.actionController.getAction(polyactions.TABLE_STR_ID).setFunc(
            self._insertTable
        )

        self._application.actionController.appendMenuItem(
            polyactions.TABLE_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.TABLE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table.png"),
            fullUpdate=False,
        )

        # Вставить строку таблицы
        self._application.actionController.getAction(
            polyactions.TABLE_ROW_STR_ID
        ).setFunc(self._insertTableRows)

        self._application.actionController.appendMenuItem(
            polyactions.TABLE_ROW_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.TABLE_ROW_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table_insert_row.png"),
            fullUpdate=False,
        )

        # Вставить ячейку таблицы
        self._application.actionController.getAction(
            polyactions.TABLE_CELL_STR_ID
        ).setFunc(lambda param: self.turnText("<td>", "</td>"))

        self._application.actionController.appendMenuItem(
            polyactions.TABLE_CELL_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.TABLE_CELL_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "table_insert_cell.png"),
            fullUpdate=False,
        )

    def _addListTools(self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._listMenu

        # Ненумерованный список
        self._application.actionController.getAction(
            polyactions.LIST_BULLETS_STR_ID
        ).setFunc(
            lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList(
                "<ul>\n", "</ul>", "<li>", "</li>"
            )
        )

        self._application.actionController.appendMenuItem(
            polyactions.LIST_BULLETS_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.LIST_BULLETS_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_list_bullets.svg"),
            fullUpdate=False,
        )

        # Нумерованный список
        self._application.actionController.getAction(
            polyactions.LIST_NUMBERS_STR_ID
        ).setFunc(
            lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList(
                "<ol>\n", "</ol>", "<li>", "</li>"
            )
        )

        self._application.actionController.appendMenuItem(
            polyactions.LIST_NUMBERS_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.LIST_NUMBERS_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_list_numbers.svg"),
            fullUpdate=False,
        )

    def _addHTools(self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._headingMenu

        self._application.actionController.getAction(
            polyactions.HEADING_1_STR_ID
        ).setFunc(lambda param: self.turnText("<h1>", "</h1>"))

        self._application.actionController.getAction(
            polyactions.HEADING_2_STR_ID
        ).setFunc(lambda param: self.turnText("<h2>", "</h2>"))

        self._application.actionController.getAction(
            polyactions.HEADING_3_STR_ID
        ).setFunc(lambda param: self.turnText("<h3>", "</h3>"))

        self._application.actionController.getAction(
            polyactions.HEADING_4_STR_ID
        ).setFunc(lambda param: self.turnText("<h4>", "</h4>"))

        self._application.actionController.getAction(
            polyactions.HEADING_5_STR_ID
        ).setFunc(lambda param: self.turnText("<h5>", "</h5>"))

        self._application.actionController.getAction(
            polyactions.HEADING_6_STR_ID
        ).setFunc(lambda param: self.turnText("<h6>", "</h6>"))

        self._application.actionController.appendMenuItem(
            polyactions.HEADING_1_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HEADING_1_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_1.svg"),
            fullUpdate=False,
        )

        self._application.actionController.appendMenuItem(
            polyactions.HEADING_2_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HEADING_2_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_2.svg"),
            fullUpdate=False,
        )

        self._application.actionController.appendMenuItem(
            polyactions.HEADING_3_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HEADING_3_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_3.svg"),
            fullUpdate=False,
        )

        self._application.actionController.appendMenuItem(
            polyactions.HEADING_4_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HEADING_4_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_4.svg"),
            fullUpdate=False,
        )

        self._application.actionController.appendMenuItem(
            polyactions.HEADING_5_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HEADING_5_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_5.svg"),
            fullUpdate=False,
        )

        self._application.actionController.appendMenuItem(
            polyactions.HEADING_6_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HEADING_6_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_heading_6.svg"),
            fullUpdate=False,
        )

    def _addFormatTools(self):
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._formatMenu

        # Preformat
        self._application.actionController.getAction(
            polyactions.PREFORMAT_STR_ID
        ).setFunc(lambda param: self.turnText("<pre>", "</pre>"))
        self._application.actionController.appendMenuItem(
            polyactions.PREFORMAT_STR_ID, menu
        )

        # Цитирование
        self._application.actionController.getAction(polyactions.QUOTE_STR_ID).setFunc(
            lambda param: self.turnText("<blockquote>", "</blockquote>")
        )

        self._application.actionController.appendMenuItem(
            polyactions.QUOTE_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.QUOTE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "quote.svg"),
            fullUpdate=False,
        )

        # Mark
        self._application.actionController.getAction(polyactions.MARK_STR_ID).setFunc(
            lambda param: self.turnText("<mark>", "</mark>")
        )

        self._application.actionController.appendMenuItem(polyactions.MARK_STR_ID, menu)
        self._application.actionController.appendToolbarButton(
            polyactions.MARK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "mark.svg"),
            fullUpdate=False,
        )

        # Код
        self._application.actionController.getAction(polyactions.CODE_STR_ID).setFunc(
            lambda param: self.turnText("<code>", "</code>")
        )

        self._application.actionController.appendMenuItem(polyactions.CODE_STR_ID, menu)
        self._application.actionController.appendToolbarButton(
            polyactions.CODE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "code.svg"),
            fullUpdate=False,
        )

    def _addOtherTools(self):
        """
        Добавить остальные инструменты
        """
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        menu = self._menu

        # Вставить картинку
        self._application.actionController.getAction(polyactions.IMAGE_STR_ID).setFunc(
            lambda param: self.turnText('<img src="', '"/>')
        )

        self._application.actionController.appendMenuItem(
            polyactions.IMAGE_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.IMAGE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "image.png"),
            fullUpdate=False,
        )

        # Вставить ссылку
        self._application.actionController.getAction(polyactions.LINK_STR_ID).setFunc(
            lambda param: insertLink(self._application)
        )

        self._application.actionController.appendMenuItem(polyactions.LINK_STR_ID, menu)
        self._application.actionController.appendToolbarButton(
            polyactions.LINK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "link.svg"),
            fullUpdate=False,
        )

        # Вставить якорь
        self._application.actionController.getAction(polyactions.ANCHOR_STR_ID).setFunc(
            lambda param: self.turnText('<a name="', '"></a>')
        )

        self._application.actionController.appendMenuItem(
            polyactions.ANCHOR_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.ANCHOR_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "anchor.svg"),
            fullUpdate=False,
        )

        # Вставить горизонтальную линию
        self._application.actionController.getAction(
            polyactions.HORLINE_STR_ID
        ).setFunc(lambda param: self.replaceText("<hr>"))

        self._application.actionController.appendMenuItem(
            polyactions.HORLINE_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.HORLINE_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "text_horizontalrule.png"),
            fullUpdate=False,
        )

        # Вставка разрыва страницы
        self._application.actionController.getAction(
            polyactions.LINE_BREAK_STR_ID
        ).setFunc(lambda param: self.replaceText("<br>\n"))

        self._application.actionController.appendMenuItem(
            polyactions.LINE_BREAK_STR_ID, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.LINE_BREAK_STR_ID,
            toolbar,
            os.path.join(self.imagesDir, "linebreak.svg"),
            fullUpdate=False,
        )

        # Текущая дата
        self._application.actionController.getAction(polyactions.CURRENT_DATE).setFunc(
            lambda param: insertCurrentDate(
                self._application.mainWindow, self.codeEditor, self._application
            )
        )

        self._application.actionController.appendMenuItem(
            polyactions.CURRENT_DATE, menu
        )
        self._application.actionController.appendToolbarButton(
            polyactions.CURRENT_DATE,
            toolbar,
            os.path.join(self.imagesDir, "date.svg"),
            fullUpdate=False,
        )

        self._menu.AppendSeparator()

        # Преобразовать символы в их HTML-представление
        self._application.actionController.getAction(
            polyactions.HTML_ESCAPE_STR_ID
        ).setFunc(lambda param: self.escapeHtml())
        self._application.actionController.appendMenuItem(
            polyactions.HTML_ESCAPE_STR_ID, menu
        )

    def _addToolbarSeparator(self):
        toolbar = self._application.mainWindow.toolbars[TOOLBAR_WEBPAGE]
        toolbar.AddSeparator()

    def _createChildWebPageAction(self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            action = CreateChildWebPageAction(self._application)
            toolbar = mainWindow.treePanel.panel.toolbar
            image = self.getImagePath("create-child.png")

            controller = self._application.actionController

            controller.appendMenuItem(action.stringId, self._menu)
            controller.appendToolbarButton(action.stringId, toolbar, image)
            toolbar.Realize()

    def _createSiblingWebPageAction(self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            action = CreateSiblingWebPageAction(self._application)
            toolbar = mainWindow.treePanel.panel.toolbar
            image = self.getImagePath("create-sibling.png")

            controller = self._application.actionController

            controller.appendMenuItem(action.stringId, self._menu)
            controller.appendToolbarButton(action.stringId, toolbar, image)
            toolbar.Realize()

    def getImagePath(self, imageName):
        """Return path to images directory."""
        selfdir = os.path.dirname(__file__)
        parentdir = os.path.dirname(selfdir)
        imagedir = os.path.join(parentdir, "images")
        fname = os.path.join(imagedir, imageName)
        return fname

    def _insertTable(self, param):
        insertTable(
            self._application,
            self._application.mainWindow.pagePanel.pageView.codeEditor,
        )

    def _insertTableRows(self, param):
        insertTableRows(
            self._application,
            self._application.mainWindow.pagePanel.pageView.codeEditor,
        )

    def turnText(self, left, right):
        """
        Обернуть выделенный текст строками left и right.
        Метод предназначен в первую очередь для упрощения доступа к одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.turnText(left, right)

    def replaceText(self, text):
        """
        Заменить выделенный текст строкой text
        Метод предназначен в первую очередь для упрощения доступа к одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText(text)

    def escapeHtml(self):
        """
        Заменить символы на их HTML-представление
        Метод предназначен в первую очередь для упрощения доступа к одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.escapeHtml()
