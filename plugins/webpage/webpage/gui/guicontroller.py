# -*- coding: UTF-8 -*-

import os

import wx

from outwiker.core.commands import insertCurrentDate
from outwiker.core.system import getOS, getImagesDir
from outwiker.gui.tabledialog import TableDialog
from outwiker.gui.tablerowsdialog import TableRowsDialog
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction
from outwiker.pages.html.actions.link import insertLink
from outwiker.pages.html.tabledialogcontroller import (
    TableDialogController,
    TableRowsDialogController
)
from outwiker.actions.polyactionsid import *

from webpage.i18n import get_
from webpage.webnotepage import WebNotePage

from webpage.actions.downloadaction import (CreateChildWebPageAction,
                                            CreateSiblingWebPageAction)
from webpage.actions.opensourceurl import OpenSourceURLAction
from webpage.actions.showpageinfo import ShowPageInfoAction
from webpage.misc import polyActions, panelName
from webpagetoolbar import WebPageToolBar


class GuiController (object):
    """Controller for creation and destroying GUI."""
    def __init__ (self, application):
        self._application = application

        self._addedWebPageMenuItems = False
        self.imagesDir = getImagesDir()
        self._MENU_INDEX = 5
        self._menuName = None


    def initialize (self):
        global _
        _ = get_()

        self._application.onPageViewDestroy += self._onPageViewDestroy
        self._application.onPageViewCreate += self._onPageViewCreate

        self._menuName = _(u"Web page")
        self._createGui()


    def destroy (self):
        self._application.onPageViewDestroy -= self._onPageViewDestroy
        self._application.onPageViewCreate -= self._onPageViewCreate

        self._removeGui()


    def _onPageViewCreate (self, page):
        assert page is not None
        if page.getTypeString() == WebNotePage.getTypeString():
            self._addWebPageGui()


    def _onPageViewDestroy (self, page):
        assert page is not None
        if page.getTypeString() == WebNotePage.getTypeString():
            self._removeWebPageGui()


    def _createGui (self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            self._createMenu()
            self._createSiblingWebPageAction()
            self._createChildWebPageAction()


    def _removeGui (self):
        mainWindow = self._application.mainWindow
        if mainWindow is not None:
            actionController = self._application.actionController
            actionController.removeMenuItem (CreateChildWebPageAction.stringId)
            actionController.removeToolbarButton (CreateChildWebPageAction.stringId)
            actionController.removeAction (CreateChildWebPageAction.stringId)

            actionController.removeMenuItem (CreateSiblingWebPageAction.stringId)
            actionController.removeToolbarButton (CreateSiblingWebPageAction.stringId)
            actionController.removeAction (CreateSiblingWebPageAction.stringId)

            if (self._application.selectedPage is not None and
                    self._application.selectedPage.getTypeString() == WebNotePage.getTypeString()):
                self._removeWebPageGui()

            index = mainWindow.mainMenu.FindMenu (self._menuName)
            assert index != wx.NOT_FOUND

            mainWindow.mainMenu.Remove (index)


    def _addWebPageGui (self):
        mainWindow = self._application.mainWindow

        if (mainWindow is not None and not self._addedWebPageMenuItems):
            controller = self._application.actionController

            mainWindow.toolbars[panelName] = WebPageToolBar(
                mainWindow,
                mainWindow.auiManager)

            openSourceAction = OpenSourceURLAction(self._application)
            controller.register (openSourceAction, hotkey=None)
            controller.appendMenuItem (openSourceAction.stringId, self._menu)

            showInfoAction = ShowPageInfoAction(self._application)
            controller.register (showInfoAction, hotkey=None)
            controller.appendMenuItem (showInfoAction.stringId, self._menu)

            self._createWebPageMenu()

            self._addFontTools()
            self._addAlignTools()
            self._addHTools()
            self._addTableTools()
            self._addListTools()
            self._addFormatTools()
            self._addOtherTools()
            self._addRenderTools()

            self._application.mainWindow.UpdateAuiManager()

            self._addedWebPageMenuItems = True


    def _removeWebPageGui (self):
        if self._addedWebPageMenuItems:
            actionController = self._application.actionController

            actionController.removeMenuItem (OpenSourceURLAction.stringId)
            actionController.removeAction (OpenSourceURLAction.stringId)

            actionController.removeMenuItem (ShowPageInfoAction.stringId)
            actionController.removeAction (ShowPageInfoAction.stringId)

            actionController.removeMenuItem (SwitchCodeResultAction.stringId)

            self._removePolyActionTools()
            if panelName in self._application.mainWindow.toolbars:
                actionController.removeToolbarButton (SwitchCodeResultAction.stringId)
                self._application.mainWindow.toolbars.destroyToolBar (panelName)

            self._menu.DestroyItem (self._headingMenuItem)
            self._menu.DestroyItem (self._fontMenuItem)
            self._menu.DestroyItem (self._alignMenuItem)
            self._menu.DestroyItem (self._formatMenuItem)
            self._menu.DestroyItem (self._listMenuItem)
            self._menu.DestroyItem (self._tableMenuItem)

            self._addedWebPageMenuItems = False


    def _removePolyActionTools (self):
        actionController = self._application.actionController

        # Удалим элементы меню полиморфных действий
        map (lambda strid: actionController.removeMenuItem (strid),
             polyActions)

        # Удалим кнопки с панелей инструментов
        if panelName in self._application.mainWindow.toolbars:
            map (lambda strid: actionController.removeToolbarButton (strid),
                 polyActions)

        # Обнулим функции действия в полиморфных действиях
        map (lambda strid: actionController.getAction (strid).setFunc (None),
             polyActions)


    def _createMenu (self):
        self._menu = wx.Menu (u'')
        self._application.mainWindow.mainMenu.Insert (self._MENU_INDEX,
                                                      self._menu,
                                                      self._menuName)

    def _createWebPageMenu (self):
        self._headingMenu = wx.Menu()
        self._fontMenu = wx.Menu()
        self._alignMenu = wx.Menu()
        self._formatMenu = wx.Menu()
        self._listMenu = wx.Menu()
        self._tableMenu = wx.Menu()

        self.toolsMenu.AppendSeparator()

        self._headingMenuItem = self._menu.AppendSubMenu (
            self._headingMenu,
            _(u"Heading")
        )

        self._fontMenuItem = self._menu.AppendSubMenu (
            self._fontMenu,
            _(u"Font")
        )

        self._alignMenuItem = self._menu.AppendSubMenu (
            self._alignMenu,
            _(u"Alignment")
        )

        self._formatMenuItem = self._menu.AppendSubMenu (
            self._formatMenu,
            _(u"Formatting")
        )

        self._listMenuItem = self._menu.AppendSubMenu (
            self._listMenu,
            _(u"Lists")
        )

        self._tableMenuItem = self._menu.AppendSubMenu (
            self._tableMenu,
            _(u"Tables")
        )


    @property
    def toolsMenu (self):
        return self._menu


    def _addRenderTools (self):
        self._application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        self._application.actionController.appendToolbarButton (
            SwitchCodeResultAction.stringId,
            self._application.mainWindow.toolbars[self._application.mainWindow.GENERAL_TOOLBAR_STR],
            os.path.join (self.imagesDir, "render.png"),
            fullUpdate=False)


    def _addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._fontMenu

        # Полужирный шрифт
        self._application.actionController.getAction (BOLD_STR_ID).setFunc (lambda param: self.turnText (u"<b>", u"</b>"))

        self._application.actionController.appendMenuItem (BOLD_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_bold.png"),
                                                                fullUpdate=False)


        # Курсивный шрифт
        self._application.actionController.getAction (ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"<i>", u"</i>"))

        self._application.actionController.appendMenuItem (ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ITALIC_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_italic.png"),
                                                                fullUpdate=False)

        # Полужирный курсивный шрифт
        self._application.actionController.getAction (BOLD_ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"<b><i>", u"</i></b>"))

        self._application.actionController.appendMenuItem (BOLD_ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_ITALIC_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_bold_italic.png"),
                                                                fullUpdate=False)


        # Подчеркнутый шрифт
        self._application.actionController.getAction (UNDERLINE_STR_ID).setFunc (lambda param: self.turnText (u"<u>", u"</u>"))

        self._application.actionController.appendMenuItem (UNDERLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (UNDERLINE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_underline.png"),
                                                                fullUpdate=False)


        # Зачеркнутый шрифт
        self._application.actionController.getAction (STRIKE_STR_ID).setFunc (lambda param: self.turnText (u"<strike>", u"</strike>"))

        self._application.actionController.appendMenuItem (STRIKE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (STRIKE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_strikethrough.png"),
                                                                fullUpdate=False)


        # Нижний индекс
        self._application.actionController.getAction (SUBSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"<sub>", u"</sub>"))

        self._application.actionController.appendMenuItem (SUBSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUBSCRIPT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_subscript.png"),
                                                                fullUpdate=False)


        # Верхний индекс
        self._application.actionController.getAction (SUPERSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"<sup>", u"</sup>"))

        self._application.actionController.appendMenuItem (SUPERSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUPERSCRIPT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_superscript.png"),
                                                                fullUpdate=False)



    def _addAlignTools (self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._alignMenu

        # Выравнивание по левому краю
        self._application.actionController.getAction (ALIGN_LEFT_STR_ID).setFunc (lambda param: self.turnText (u'<div align="left">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_LEFT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_LEFT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_left.png"),
                                                                fullUpdate=False)


        # Выравнивание по центру
        self._application.actionController.getAction (ALIGN_CENTER_STR_ID).setFunc (lambda param: self.turnText (u'<div align="center">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_CENTER_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_CENTER_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_center.png"),
                                                                fullUpdate=False)


        # Выравнивание по правому краю
        self._application.actionController.getAction (ALIGN_RIGHT_STR_ID).setFunc (lambda param: self.turnText (u'<div align="right">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_RIGHT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_RIGHT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_right.png"),
                                                                fullUpdate=False)


        # Выравнивание по ширине
        self._application.actionController.getAction (ALIGN_JUSTIFY_STR_ID).setFunc (lambda param: self.turnText (u'<div align="justify">', u'</div>'))

        self._application.actionController.appendMenuItem (ALIGN_JUSTIFY_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_JUSTIFY_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_justify.png"),
                                                                fullUpdate=False)



    def _addTableTools (self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._tableMenu

        # Вставить таблицу
        self._application.actionController.getAction (TABLE_STR_ID).setFunc (
            self._insertTable
        )

        self._application.actionController.appendMenuItem (TABLE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (TABLE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "table.png"),
                                                                fullUpdate=False)


        # Вставить строку таблицы
        self._application.actionController.getAction (TABLE_ROW_STR_ID).setFunc (
            self._insertTableRows
        )

        self._application.actionController.appendMenuItem (TABLE_ROW_STR_ID, menu)
        self._application.actionController.appendToolbarButton (TABLE_ROW_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "table_insert_row.png"),
                                                                fullUpdate=False)


        # Вставить ячейку таблицы
        self._application.actionController.getAction (TABLE_CELL_STR_ID).setFunc (lambda param: self.turnText (u'<td>', u'</td>'))

        self._application.actionController.appendMenuItem (TABLE_CELL_STR_ID, menu)
        self._application.actionController.appendToolbarButton (TABLE_CELL_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "table_insert_cell.png"),
                                                                fullUpdate=False)



    def _addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._listMenu

        # Ненумерованный список
        self._application.actionController.getAction (LIST_BULLETS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'))

        self._application.actionController.appendMenuItem (LIST_BULLETS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_BULLETS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_bullets.png"),
                                                                fullUpdate=False)

        # Нумерованный список
        self._application.actionController.getAction (LIST_NUMBERS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'))

        self._application.actionController.appendMenuItem (LIST_NUMBERS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_NUMBERS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_numbers.png"),
                                                                fullUpdate=False)



    def _addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._headingMenu

        self._application.actionController.getAction (HEADING_1_STR_ID).setFunc (lambda param: self.turnText (u"<h1>", u"</h1>"))
        self._application.actionController.getAction (HEADING_2_STR_ID).setFunc (lambda param: self.turnText (u"<h2>", u"</h2>"))
        self._application.actionController.getAction (HEADING_3_STR_ID).setFunc (lambda param: self.turnText (u"<h3>", u"</h3>"))
        self._application.actionController.getAction (HEADING_4_STR_ID).setFunc (lambda param: self.turnText (u"<h4>", u"</h4>"))
        self._application.actionController.getAction (HEADING_5_STR_ID).setFunc (lambda param: self.turnText (u"<h5>", u"</h5>"))
        self._application.actionController.getAction (HEADING_6_STR_ID).setFunc (lambda param: self.turnText (u"<h6>", u"</h6>"))

        self._application.actionController.appendMenuItem (HEADING_1_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_1_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_1.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_2_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_2_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_2.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_3_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_3_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_3.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_4_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_4_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_4.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_5_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_5_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_5.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_6_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_6_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_6.png"),
                                                                fullUpdate=False)


    def _addFormatTools (self):
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._formatMenu

        # Preformat
        self._application.actionController.getAction (PREFORMAT_STR_ID).setFunc (lambda param: self.turnText (u"<pre>", u"</pre>"))
        self._application.actionController.appendMenuItem (PREFORMAT_STR_ID, menu)

        # Цитирование
        self._application.actionController.getAction (QUOTE_STR_ID).setFunc (lambda param: self.turnText (u"<blockquote>", u"</blockquote>"))

        self._application.actionController.appendMenuItem (QUOTE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (QUOTE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "quote.png"),
                                                                fullUpdate=False)

        # Код
        self._application.actionController.getAction (CODE_STR_ID).setFunc (lambda param: self.turnText (u'<code>', u'</code>'))

        self._application.actionController.appendMenuItem (CODE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (CODE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "code.png"),
                                                                fullUpdate=False)


    def _addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        toolbar = self._application.mainWindow.toolbars[panelName]
        menu = self._menu

        # Вставить картинку
        self._application.actionController.getAction (IMAGE_STR_ID).setFunc (lambda param: self.turnText (u'<img src="', u'"/>'))

        self._application.actionController.appendMenuItem (IMAGE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (IMAGE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "image.png"),
                                                                fullUpdate=False)


        # Вставить ссылку
        self._application.actionController.getAction (LINK_STR_ID).setFunc (lambda param: insertLink (self._application))

        self._application.actionController.appendMenuItem (LINK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "link.png"),
                                                                fullUpdate=False)


        # Вставить якорь
        self._application.actionController.getAction (ANCHOR_STR_ID).setFunc (lambda param: self.turnText (u'<a name="', u'"></a>'))

        self._application.actionController.appendMenuItem (ANCHOR_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ANCHOR_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "anchor.png"),
                                                                fullUpdate=False)


        # Вставить горизонтальную линию
        self._application.actionController.getAction (HORLINE_STR_ID).setFunc (lambda param: self.replaceText (u"<hr>"))

        self._application.actionController.appendMenuItem (HORLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HORLINE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                                                                fullUpdate=False)


        # Вставка разрыва страницы
        self._application.actionController.getAction (LINE_BREAK_STR_ID).setFunc (lambda param: self.replaceText (u"<br>\n"))

        self._application.actionController.appendMenuItem (LINE_BREAK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINE_BREAK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "linebreak.png"),
                                                                fullUpdate=False)

        # Текущая дата
        self._application.actionController.getAction (CURRENT_DATE).setFunc (lambda param: insertCurrentDate (self._application.mainWindow,
                                                                                                              self.codeEditor))

        self._application.actionController.appendMenuItem (CURRENT_DATE, menu)
        self._application.actionController.appendToolbarButton (CURRENT_DATE,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "date.png"),
                                                                fullUpdate=False)


        self._menu.AppendSeparator()

        # Преобразовать символы в их HTML-представление
        self._application.actionController.getAction (HTML_ESCAPE_STR_ID).setFunc (lambda param: self.escapeHtml ())
        self._application.actionController.appendMenuItem (HTML_ESCAPE_STR_ID, menu)


    def _createChildWebPageAction (self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            action = CreateChildWebPageAction(self._application)
            toolbar = mainWindow.treePanel.panel.toolbar
            image = self.getImagePath (u'create-child.png')

            controller = self._application.actionController

            controller.register (action, hotkey=None)
            controller.appendMenuItem (action.stringId, self._menu)
            controller.appendToolbarButton (action.stringId,
                                            toolbar,
                                            image)
            toolbar.Realize()


    def _createSiblingWebPageAction (self):
        mainWindow = self._application.mainWindow

        if mainWindow is not None:
            action = CreateSiblingWebPageAction(self._application)
            toolbar = mainWindow.treePanel.panel.toolbar
            image = self.getImagePath (u'create-sibling.png')

            controller = self._application.actionController

            controller.register (action, hotkey=None)
            controller.appendMenuItem (action.stringId, self._menu)
            controller.appendToolbarButton (action.stringId,
                                            toolbar,
                                            image)
            toolbar.Realize()


    def getImagePath (self, imageName):
        """Return path to images directory."""
        selfdir = os.path.dirname (__file__)
        parentdir = os.path.dirname (selfdir)
        imagedir = unicode (os.path.join (parentdir, "images"), getOS().filesEncoding)
        fname = os.path.join (imagedir, imageName)
        return fname


    def _insertTable (self, param):
        editor = self._application.mainWindow.pagePanel.pageView.codeEditor
        parent = self._application.mainWindow

        with TableDialog (parent) as dlg:
            controller = TableDialogController (dlg, self._application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText (result)


    def _insertTableRows (self, param):
        editor = self._application.mainWindow.pagePanel.pageView.codeEditor
        parent = self._application.mainWindow

        with TableRowsDialog (parent) as dlg:
            controller = TableRowsDialogController (dlg,
                                                    self._application.config)
            if controller.showDialog() == wx.ID_OK:
                result = controller.getResult()
                editor.replaceText (result)

    def turnText (self, left, right):
        """
        Обернуть выделенный текст строками left и right.
        Метод предназначен в первую очередь для упрощения доступа к одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.turnText (left, right)


    def replaceText (self, text):
        """
        Заменить выделенный текст строкой text
        Метод предназначен в первую очередь для упрощения доступа к одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.replaceText (text)


    def escapeHtml (self):
        """
        Заменить символы на их HTML-представление
        Метод предназначен в первую очередь для упрощения доступа к одноименному методу из codeEditor
        """
        self._application.mainWindow.pagePanel.pageView.codeEditor.escapeHtml ()
