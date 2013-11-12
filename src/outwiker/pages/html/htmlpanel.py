# -*- coding: utf-8 -*-

import os
import re

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.application import Application
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style

from .htmltoolbar import HtmlToolBar
from .basehtmlpanel import BaseHtmlPanel

from actions.headings import *
from actions.bold import HtmlBoldAction
from actions.italic import HtmlItalicAction
from actions.underline import HtmlUnderlineAction
from actions.strike import HtmlStrikeAction
from actions.subscript import HtmlSubscriptAction
from actions.superscript import HtmlSuperscriptAction
from actions.alignleft import HtmlAlignLeftAction
from actions.aligncenter import HtmlAlignCenterAction
from actions.alignright import HtmlAlignRightAction
from actions.alignjustify import HtmlAlignJustifyAction
from actions.table import HtmlTableAction
from actions.tablerow import HtmlTableRowAction
from actions.tablecell import HtmlTableCellAction
from actions.listbullets import HtmlListBulletsAction
from actions.listnumbers import HtmlListNumbersAction
from actions.code import HtmlCodeAction
from actions.preformat import HtmlPreformatAction
from actions.quote import HtmlQuoteAction
from actions.image import HtmlImageAction
from actions.link import HtmlLinkAction
from actions.anchor import HtmlAnchorAction
from actions.horline import HtmlHorLineAction
from actions.escapehtml import HtmlEscapeHtmlAction

from actions.autolinewrap import HtmlAutoLineWrap
from actions.switchcoderesult import SwitchCodeResultAction


class HtmlPagePanel (BaseHtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        super (HtmlPagePanel, self).__init__ (parent, *args, **kwds)

        self.__HTML_MENU_INDEX = 7
        self._htmlPanelName = "html"

        self.mainWindow.toolbars[self._htmlPanelName] = HtmlToolBar(self.mainWindow, 
                self.mainWindow.auiManager)
        self.mainWindow.toolbars[self._htmlPanelName].UpdateToolBar()

        # Список действий, которые нужно удалять с панелей и из меню. 
        # А еще их надо дизаблить при переходе на вкладку просмотра результата
        self.__htmlNotationActions = [
                HtmlBoldAction,
                HtmlItalicAction,
                HtmlUnderlineAction,
                HtmlStrikeAction,
                HtmlSubscriptAction,
                HtmlSuperscriptAction,
                HtmlAlignLeftAction,
                HtmlAlignCenterAction,
                HtmlAlignRightAction,
                HtmlAlignJustifyAction,
                HtmlTableAction,
                HtmlTableRowAction,
                HtmlTableCellAction,
                HtmlListBulletsAction,
                HtmlListNumbersAction,
                HtmlHeading1Action,
                HtmlHeading2Action,
                HtmlHeading3Action,
                HtmlHeading4Action,
                HtmlHeading5Action,
                HtmlHeading6Action,
                HtmlCodeAction,
                HtmlPreformatAction,
                HtmlQuoteAction,
                HtmlImageAction,
                HtmlLinkAction,
                HtmlAnchorAction,
                HtmlHorLineAction,
                HtmlEscapeHtmlAction,
                ]

        self.__createCustomTools()
        Application.mainWindow.updateShortcuts()
        self.mainWindow.UpdateAuiManager()

        Application.onPageUpdate += self.__onPageUpdate


    @property
    def toolsMenu (self):
        return self.__htmlMenu


    def onClose (self, event):
        Application.onPageUpdate -= self.__onPageUpdate

        self._removeActionTools()

        if self._htmlPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._htmlPanelName)

        super (HtmlPagePanel, self).onClose (event)


    def _removeActionTools (self):
        actionController = Application.actionController

        self.mainWindow.Freeze()

        # Удалим элементы меню
        map (lambda action: actionController.removeMenuItem (action.stringId), 
                self.__htmlNotationActions)

        Application.actionController.removeMenuItem (HtmlAutoLineWrap.stringId)
        Application.actionController.removeMenuItem (SwitchCodeResultAction.stringId)
        
        # Удалим кнопки с панелей инструментов
        if self._htmlPanelName in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId), 
                self.__htmlNotationActions)

            Application.actionController.removeToolbarButton (HtmlAutoLineWrap.stringId)
            Application.actionController.removeToolbarButton (SwitchCodeResultAction.stringId)

        self.mainWindow.Thaw()


    def _enableActions (self, enabled):
        actionController = Application.actionController

        self.mainWindow.Freeze()

        map (lambda action: actionController.enableTools (action.stringId, enabled), 
                self.__htmlNotationActions)

        self.mainWindow.Thaw()


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions (True)
        super (HtmlPagePanel, self)._onSwitchToCode()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self._enableActions (False)
        super (HtmlPagePanel, self)._onSwitchToPreview()


    def __onPageUpdate (self, sender):
        if sender == self._currentpage:
            if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
                self._showHtml()


    def UpdateView (self, page):
        self.__updateLineWrapTools()
        BaseHtmlPanel.UpdateView (self, page)


    def __createLineWrapTools (self):
        """
        Создать кнопки и пункты меню, отображающие настройки страницы
        """
        image = os.path.join (self.imagesDir, "linewrap.png")
        toolbar = self.mainWindow.toolbars["html"]

        Application.actionController.appendMenuCheckItem (HtmlAutoLineWrap.stringId, self.__htmlMenu)
        Application.actionController.appendToolbarCheckButton (HtmlAutoLineWrap.stringId, 
                toolbar,
                image,
                fullUpdate=False)

        self.__updateLineWrapTools()


    def __updateLineWrapTools (self):
        if self._currentpage != None:
            Application.actionController.check (HtmlAutoLineWrap.stringId, 
                    self._currentpage.autoLineWrap)


    def __createCustomTools (self):
        """
        Создать кнопки и меню для данного типа страниц
        """
        assert self.mainWindow != None

        self.__htmlMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__tableMenu = wx.Menu()

        self.mainWindow.Freeze()

        self.__createLineWrapTools ()
        self.toolsMenu.AppendSeparator()

        self.__htmlMenu.AppendSubMenu (self.__headingMenu, _(u"Heading"))
        self.__htmlMenu.AppendSubMenu (self.__fontMenu, _(u"Font"))
        self.__htmlMenu.AppendSubMenu (self.__alignMenu, _(u"Alignment"))
        self.__htmlMenu.AppendSubMenu (self.__formatMenu, _(u"Formatting"))
        self.__htmlMenu.AppendSubMenu (self.__listMenu, _(u"Lists"))
        self.__htmlMenu.AppendSubMenu (self.__tableMenu, _(u"Table"))

        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addTableTools()
        self.__addListTools()
        self.__addFormatTools()
        self.__addOtherTools()
        self._addRenderTools()

        self.mainWindow.Thaw()

        self.mainWindow.mainMenu.Insert (self.__HTML_MENU_INDEX, self.__htmlMenu, _(u"Html"))


    def _addRenderTools (self):
        Application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        Application.actionController.appendToolbarButton (SwitchCodeResultAction.stringId, 
                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                os.path.join (self.imagesDir, "render.png"),
                fullUpdate=False)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__fontMenu

        # Полужирный шрифт
        Application.actionController.appendMenuItem (HtmlBoldAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlBoldAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False)


        # Курсивный шрифт
        Application.actionController.appendMenuItem (HtmlItalicAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlItalicAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False)


        # Подчеркнутый шрифт
        Application.actionController.appendMenuItem (HtmlUnderlineAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlUnderlineAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False)


        # Зачеркнутый шрифт
        Application.actionController.appendMenuItem (HtmlStrikeAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlStrikeAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False)


        # Нижний индекс
        Application.actionController.appendMenuItem (HtmlSubscriptAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlSubscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False)


        # Верхний индекс
        Application.actionController.appendMenuItem (HtmlSuperscriptAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlSuperscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False)


    
    def __addAlignTools (self):
        """
        Добавить инструменты, связанные с выравниванием
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__alignMenu

        # Выравнивание по левому краю
        Application.actionController.appendMenuItem (HtmlAlignLeftAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlAlignLeftAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False)


        # Выравнивание по центру
        Application.actionController.appendMenuItem (HtmlAlignCenterAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlAlignCenterAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False)


        # Выравнивание по правому краю
        Application.actionController.appendMenuItem (HtmlAlignRightAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlAlignRightAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False)


        # Выравнивание по ширине
        Application.actionController.appendMenuItem (HtmlAlignJustifyAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlAlignJustifyAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False)



    def __addTableTools (self):
        """
        Добавить инструменты, связанные с таблицами
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__tableMenu

        # Вставить таблицу
        Application.actionController.appendMenuItem (HtmlTableAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlTableAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "table.png"),
                fullUpdate=False)


        # Вставить строку таблицы
        Application.actionController.appendMenuItem (HtmlTableRowAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlTableRowAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "table_insert_row.png"),
                fullUpdate=False)


        # Вставить ячейку таблицы
        Application.actionController.appendMenuItem (HtmlTableCellAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlTableCellAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "table_insert_cell.png"),
                fullUpdate=False)


    
    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__listMenu

        # Ненумерованный список
        Application.actionController.appendMenuItem (HtmlListBulletsAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlListBulletsAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False)

        # Нумерованный список
        Application.actionController.appendMenuItem (HtmlListNumbersAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlListNumbersAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False)



    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__headingMenu

        Application.actionController.appendMenuItem (HtmlHeading1Action.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHeading1Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (HtmlHeading2Action.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHeading2Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (HtmlHeading3Action.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHeading3Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (HtmlHeading4Action.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHeading4Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (HtmlHeading5Action.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHeading5Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False)

        Application.actionController.appendMenuItem (HtmlHeading6Action.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHeading6Action.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False) 


    def __addFormatTools (self):
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__formatMenu

        # Код
        Application.actionController.appendMenuItem (HtmlCodeAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlCodeAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "code.png"),
                fullUpdate=False)

        # Preformat
        Application.actionController.appendMenuItem (HtmlPreformatAction.stringId, menu)

        # Цитирование
        Application.actionController.appendMenuItem (HtmlQuoteAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlQuoteAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "quote.png"),
                fullUpdate=False)


    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        toolbar = self.mainWindow.toolbars[self._htmlPanelName]
        menu = self.__htmlMenu

        # Вставить картинку
        Application.actionController.appendMenuItem (HtmlImageAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlImageAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "image.png"),
                fullUpdate=False)


        # Вставить ссылку
        Application.actionController.appendMenuItem (HtmlLinkAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlLinkAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False)


        # Вставить якорь
        Application.actionController.appendMenuItem (HtmlAnchorAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlAnchorAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False)


        # Вставить горизонтальную линию
        Application.actionController.appendMenuItem (HtmlHorLineAction.stringId, menu)
        Application.actionController.appendToolbarButton (HtmlHorLineAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False)


        self.__htmlMenu.AppendSeparator()

        # Преобразовать символы в их HTML-представление
        Application.actionController.appendMenuItem (HtmlEscapeHtmlAction.stringId, menu)



    def generateHtml (self, page):
        path = self.getHtmlPath (page)

        if page.readonly and os.path.exists (path):
            # Если страница открыта только для чтения и html-файл уже существует, то покажем его
            return path

        style = Style()
        stylepath = style.getPageStyle (page)

        try:
            tpl = HtmlTemplate (stylepath)
        except:
            MessageBox (_(u"Page style Error. Style by default is used"),  
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

            tpl = HtmlTemplate (style.getDefaultStyle())

        if page.autoLineWrap:
            text = HtmlImprover.run (page.content)
            text = re.sub ("\n<BR>\n(<li>)|(<LI>)", "\n<LI>", text)
        else:
            text = page.content

        result = tpl.substitute (content=text)

        with open (path, "wb") as fp:
            fp.write (result.encode ("utf-8"))

        return path


    def removeGui (self):
        super (HtmlPagePanel, self).removeGui ()
        self.mainWindow.mainMenu.Remove (self.__HTML_MENU_INDEX - 1)
