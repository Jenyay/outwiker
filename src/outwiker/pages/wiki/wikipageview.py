#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx
import os

from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.config import Config, StringOption
from outwiker.core.tree import RootWikiPage
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style

from .wikieditor import WikiEditor
from .wikitoolbar import WikiToolBar
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from wikiconfig import WikiConfig
from htmlgenerator import HtmlGenerator
from outwiker.actions.polyactionsid import *

from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.nonparsed import WikiNonParsedAction
from actions.thumb import WikiThumbAction
from actions.link import insertLink
from actions.equation import WikiEquationAction
from actions.openhtmlcode import WikiOpenHtmlCodeAction
from actions.updatehtml import WikiUpdateHtmlAction
from actions.attachlist import WikiAttachListAction
from actions.childlist import WikiChildListAction
from actions.include import WikiIncludeAction
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction


class WikiPageView (BaseHtmlPanel):
    HTML_RESULT_PAGE_INDEX = BaseHtmlPanel.RESULT_PAGE_INDEX + 1


    def __init__ (self, parent, *args, **kwds):
        super (WikiPageView, self).__init__ (parent, *args, **kwds)

        self._application = Application

        self._configSection = u"wiki"
        self._hashKey = u"md5_hash"
        self.__WIKI_MENU_INDEX = 7
        self.__toolbarName = "wiki"

        # Список используемых полиморфных действий
        self.__polyActions = [
                BOLD_STR_ID,
                ITALIC_STR_ID,
                BOLD_ITALIC_STR_ID,
                UNDERLINE_STR_ID,
                STRIKE_STR_ID,
                SUBSCRIPT_STR_ID,
                SUPERSCRIPT_STR_ID,
                QUOTE_STR_ID,
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
                ]

        # Список действий, которые нужно удалять с панелей и из меню. 
        # А еще их надо дизаблить при переходе на вкладки просмотра результата или HTML
        self.__wikiNotationActions = [
                WikiFontSizeBigAction,
                WikiFontSizeSmallAction,
                WikiNonParsedAction,
                WikiThumbAction,
                WikiEquationAction,
                WikiAttachListAction,
                WikiChildListAction,
                WikiIncludeAction,
                ]

        self._wikiPanelName = "wiki"

        self.mainWindow.toolbars[self._wikiPanelName] = WikiToolBar(self.mainWindow, self.mainWindow.auiManager)

        self.notebook.SetPageText (0, _(u"Wiki"))

        self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.htmlSizer.AddGrowableRow(0)
        self.htmlSizer.AddGrowableCol(0)

        # Номер вкладки с кодом HTML. -1, если вкладки нет
        self.htmlcodePageIndex = -1

        self.config = WikiConfig (self._application.config)

        self.__createCustomTools()
        self._application.mainWindow.updateShortcuts()
        self.mainWindow.UpdateAuiManager()

        if self.config.showHtmlCodeOptions.value:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()


    def onClose (self, event):
        self._removeActionTools()

        if self._wikiPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._wikiPanelName)

        super (WikiPageView, self).onClose (event)


    def _removeActionTools (self):
        actionController = self._application.actionController

        # Удалим элементы меню
        map (lambda action: actionController.removeMenuItem (action.stringId), 
                self.__wikiNotationActions)

        # Удалим элементы меню полиморфных действий
        map (lambda strid: actionController.removeMenuItem (strid), 
                self.__polyActions)

        actionController.removeMenuItem (WikiOpenHtmlCodeAction.stringId)
        actionController.removeMenuItem (WikiUpdateHtmlAction.stringId)
        actionController.removeMenuItem (SwitchCodeResultAction.stringId)

        # Удалим кнопки с панелей инструментов
        if self._wikiPanelName in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId), 
                self.__wikiNotationActions)

            map (lambda strid: actionController.removeToolbarButton (strid), 
                self.__polyActions)

            actionController.removeToolbarButton (WikiOpenHtmlCodeAction.stringId)
            actionController.removeToolbarButton (SwitchCodeResultAction.stringId)

        # Обнулим функции действия в полиморфных действиях
        map (lambda strid: actionController.getAction (strid).setFunc (None), 
                self.__polyActions)


    @property
    def toolsMenu (self):
        return self.__wikiMenu


    def __createHtmlCodePanel (self, parentSizer):
        # Окно для просмотра получившегося кода HTML
        self.htmlCodeWindow = HtmlTextEditor(self.notebook, -1)
        self.htmlCodeWindow.SetReadOnly (True)
        parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 2)
        
        self.addPage (self.htmlCodeWindow, _("HTML"))
        return self.pageCount - 1
    

    def GetTextEditor(self):
        return WikiEditor


    def GetSearchPanel (self):
        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel
        elif self.selectedPageIndex == self.htmlcodePageIndex:
            return self.htmlCodeWindow.searchPanel

        return None


    def onTabChanged(self, event):
        if self._currentpage == None:
            return

        if self.selectedPageIndex == self.CODE_PAGE_INDEX:
            self._onSwitchToCode()

        elif self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()

        elif self.selectedPageIndex == self.htmlcodePageIndex:
            self._onSwitchCodeHtml()

        self.savePageTab(self._currentpage)


    def _enableActions (self, enabled):
        actionController = self._application.actionController

        # Активируем / дизактивируем собственные действия
        map (lambda action: actionController.enableTools (action.stringId, enabled), 
                self.__wikiNotationActions)

        # Активируем / дизактивируем полиморфные действия
        map (lambda strid: actionController.enableTools (strid, enabled), 
                self.__polyActions)


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions (True)
        super (WikiPageView, self)._onSwitchToCode()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self._enableActions (False)
        super (WikiPageView, self)._onSwitchToPreview()


    def _onSwitchCodeHtml (self):
        assert self._currentpage != None

        self._enableActions (False)

        self.Save()
        status_item = 0
        setStatusText (_(u"Page rendered. Please wait…"), status_item)
        self._application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

        try:
            self.currentHtmlFile = self.generateHtml (self._currentpage)
            self._showHtmlCode(self.currentHtmlFile)
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
        except OSError as e:
            MessageBox (_(u"Can't save HTML-file\n\n%s") % (unicode (e)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)

        setStatusText (u"", status_item)
        self._application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)

        self._enableAllTools ()
        self.htmlCodeWindow.SetFocus()
        self.htmlCodeWindow.Update()


    def _showHtmlCode (self, path):
        try:
            with open (path) as fp:
                text = unicode (fp.read(), "utf8")

                self.htmlCodeWindow.SetReadOnly (False)
                self.htmlCodeWindow.SetText (text)
                self.htmlCodeWindow.SetReadOnly (True)
        except IOError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)
        except OSError:
            MessageBox (_(u"Can't load HTML-file"), _(u"Error"), wx.ICON_ERROR | wx.OK)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__fontMenu

        # Полужирный шрифт
        self._application.actionController.getAction (BOLD_STR_ID).setFunc (lambda param: self.turnText (u"'''", u"'''"))

        self._application.actionController.appendMenuItem (BOLD_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False)


        # Курсивный шрифт
        self._application.actionController.getAction (ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"''", u"''"))

        self._application.actionController.appendMenuItem (ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ITALIC_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False)

        # Полужирный курсивный шрифт
        self._application.actionController.getAction (BOLD_ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"''''", u"''''"))

        self._application.actionController.appendMenuItem (BOLD_ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_ITALIC_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold_italic.png"),
                fullUpdate=False)


        # Подчеркнутый шрифт
        self._application.actionController.getAction (UNDERLINE_STR_ID).setFunc (lambda param: self.turnText (u"{+", u"+}"))

        self._application.actionController.appendMenuItem (UNDERLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (UNDERLINE_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False)


        # Зачеркнутый шрифт
        self._application.actionController.getAction (STRIKE_STR_ID).setFunc (lambda param: self.turnText (u"{-", u"-}"))

        self._application.actionController.appendMenuItem (STRIKE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (STRIKE_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False)


        # Нижний индекс
        self._application.actionController.getAction (SUBSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"'_", u"_'"))

        self._application.actionController.appendMenuItem (SUBSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUBSCRIPT_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False)


        # Верхний индекс
        self._application.actionController.getAction (SUPERSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"'^", u"^'"))

        self._application.actionController.appendMenuItem (SUPERSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUPERSCRIPT_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False)


        # Крупный шрифт
        self._application.actionController.appendMenuItem (WikiFontSizeBigAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiFontSizeBigAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_big.png"),
                fullUpdate=False)


        # Мелкий шрифт
        self._application.actionController.appendMenuItem (WikiFontSizeSmallAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiFontSizeSmallAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_small.png"),
                fullUpdate=False)


    def __addAlignTools (self):
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__alignMenu

        # Выравнивание по левому краю
        self._application.actionController.getAction (ALIGN_LEFT_STR_ID).setFunc (lambda param: self.turnText (u"%left%", u""))

        self._application.actionController.appendMenuItem (ALIGN_LEFT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_LEFT_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False)


        # Выравнивание по центру
        self._application.actionController.getAction (ALIGN_CENTER_STR_ID).setFunc (lambda param: self.turnText (u"%center%", u""))

        self._application.actionController.appendMenuItem (ALIGN_CENTER_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_CENTER_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False)


        # Выравнивание по правому краю
        self._application.actionController.getAction (ALIGN_RIGHT_STR_ID).setFunc (lambda param: self.turnText (u"%right%", u""))

        self._application.actionController.appendMenuItem (ALIGN_RIGHT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_RIGHT_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False)


        # Выравнивание по ширине
        self._application.actionController.getAction (ALIGN_JUSTIFY_STR_ID).setFunc (lambda param: self.turnText (u"%justify%", u""))

        self._application.actionController.appendMenuItem (ALIGN_JUSTIFY_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_JUSTIFY_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False)


    def __addFormatTools (self):
        menu = self.__formatMenu
        toolbar = self.mainWindow.toolbars[self.__toolbarName]

        # Текст, который не нужно разбирать википарсером
        self._application.actionController.appendMenuItem (WikiNonParsedAction.stringId, menu)

        # Форматированный текст
        self._application.actionController.getAction (PREFORMAT_STR_ID).setFunc (lambda param: self.turnText (u"[@", u"@]"))
        self._application.actionController.appendMenuItem (PREFORMAT_STR_ID, menu)

        # Цитата
        self._application.actionController.getAction (QUOTE_STR_ID).setFunc (lambda param: self.turnText (u'[>', u'<]'))

        self._application.actionController.appendMenuItem (QUOTE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (QUOTE_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "quote.png"),
                fullUpdate=False)


        # Моноширинный шрифт
        self._application.actionController.getAction (CODE_STR_ID).setFunc (lambda param: self.turnText (u'@@', u'@@'))

        self._application.actionController.appendMenuItem (CODE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (CODE_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "code.png"),
                fullUpdate=False)
        


    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__listMenu

        # Ненумерованный список
        self._application.actionController.getAction (LIST_BULLETS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList ("* "))

        self._application.actionController.appendMenuItem (LIST_BULLETS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_BULLETS_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False)


        # Нумерованный список
        self._application.actionController.getAction (LIST_NUMBERS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList ("# "))

        self._application.actionController.appendMenuItem (LIST_NUMBERS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_NUMBERS_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False)


    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__headingMenu

        self._application.actionController.getAction (HEADING_1_STR_ID).setFunc (lambda param: self.turnText (u"!! ", u""))
        self._application.actionController.getAction (HEADING_2_STR_ID).setFunc (lambda param: self.turnText (u"!!! ", u""))
        self._application.actionController.getAction (HEADING_3_STR_ID).setFunc (lambda param: self.turnText (u"!!!! ", u""))
        self._application.actionController.getAction (HEADING_4_STR_ID).setFunc (lambda param: self.turnText (u"!!!!! ", u""))
        self._application.actionController.getAction (HEADING_5_STR_ID).setFunc (lambda param: self.turnText (u"!!!!!! ", u""))
        self._application.actionController.getAction (HEADING_6_STR_ID).setFunc (lambda param: self.turnText (u"!!!!!!! ", u""))

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



    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        # Добавить миниатюру
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__wikiMenu

        self._application.actionController.appendMenuItem (WikiThumbAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiThumbAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "images.png"),
                fullUpdate=False)


        # Вставка ссылок
        self._application.actionController.getAction (LINK_STR_ID).setFunc (lambda param: insertLink (self._application))

        self._application.actionController.appendMenuItem (LINK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINK_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False)


        # Вставка якоря
        self._application.actionController.getAction (ANCHOR_STR_ID).setFunc (lambda param: self.turnText (u"[[#", u"]]"))

        self._application.actionController.appendMenuItem (ANCHOR_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ANCHOR_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False)


        # Вставка горизонтальной линии
        self._application.actionController.getAction (HORLINE_STR_ID).setFunc (lambda param: self.replaceText (u"----"))

        self._application.actionController.appendMenuItem (HORLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HORLINE_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False)


        # Вставка разрыва страницы
        self._application.actionController.getAction (LINE_BREAK_STR_ID).setFunc (lambda param: self.replaceText (u"[[<<]]"))

        self._application.actionController.appendMenuItem (LINE_BREAK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINE_BREAK_STR_ID, 
                toolbar,
                os.path.join (self.imagesDir, "linebreak.png"),
                fullUpdate=False)


        # Вставка формулы
        self._application.actionController.appendMenuItem (WikiEquationAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiEquationAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "equation.png"),
                fullUpdate=False)


        self.__wikiMenu.AppendSeparator()

        # Преобразовать некоторые символы в и их HTML-представление
        self._application.actionController.getAction (HTML_ESCAPE_STR_ID).setFunc (lambda param: self.escapeHtml ())
        self._application.actionController.appendMenuItem (HTML_ESCAPE_STR_ID, menu)


    def _addRenderTools (self):
        self._application.actionController.appendMenuItem (SwitchCodeResultAction.stringId, self.toolsMenu)
        self._application.actionController.appendToolbarButton (SwitchCodeResultAction.stringId, 
                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                os.path.join (self.imagesDir, "render.png"),
                fullUpdate=False)


    def __createCustomTools (self):
        assert self.mainWindow != None

        self.__wikiMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__commandsMenu = wx.Menu()

        self._addRenderTools()

        # Переключиться на код HTML
        self._application.actionController.appendMenuItem (WikiOpenHtmlCodeAction.stringId, self.__wikiMenu)
        self._application.actionController.appendToolbarButton (WikiOpenHtmlCodeAction.stringId, 
                self.mainWindow.toolbars[self.mainWindow.GENERAL_TOOLBAR_STR],
                os.path.join (self.imagesDir, "html.png"),
                fullUpdate=False)

        # Обновить код HTML
        self._application.actionController.appendMenuItem (WikiUpdateHtmlAction.stringId, self.__wikiMenu)

        self.toolsMenu.AppendSeparator()

        self.__wikiMenu.AppendSubMenu (self.__headingMenu, _(u"Heading"))
        self.__wikiMenu.AppendSubMenu (self.__fontMenu, _(u"Font"))
        self.__wikiMenu.AppendSubMenu (self.__alignMenu, _(u"Alignment"))
        self.__wikiMenu.AppendSubMenu (self.__formatMenu, _(u"Formatting"))
        self.__wikiMenu.AppendSubMenu (self.__listMenu, _(u"Lists"))
        self.__wikiMenu.AppendSubMenu (self.__commandsMenu, _(u"Commands"))

        self.__addCommandsTools()
        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addListTools()
        self.__addFormatTools()
        self.__addOtherTools()

        self.mainWindow.mainMenu.Insert (self.__WIKI_MENU_INDEX, 
                self.__wikiMenu, 
                _(u"Wiki") )


    @property
    def commandsMenu (self):
        """
        Свойство возвращает меню с викикомандами
        """
        return self.__commandsMenu


    def __addCommandsTools (self):
        # Команда (:attachlist:)
        self._application.actionController.appendMenuItem (WikiAttachListAction.stringId, self.commandsMenu)

        # Команда (:childlist:)
        self._application.actionController.appendMenuItem (WikiChildListAction.stringId, self.commandsMenu)

        # Команда (:include:)
        self._application.actionController.appendMenuItem (WikiIncludeAction.stringId, self.commandsMenu)


    @BaseHtmlPanel.selectedPageIndex.setter
    def selectedPageIndex (self, index):
        """
        Устанавливает выбранную страницу (код, просмотр или полученный HTML)
        """
        if index == self.HTML_RESULT_PAGE_INDEX and self.htmlcodePageIndex == -1:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)
            selectedPage = self.htmlcodePageIndex
        else:
            selectedPage = index

        BaseHtmlPanel.selectedPageIndex.fset (self, selectedPage)


    def openHtmlCode (self):
        self.selectedPageIndex = self.HTML_RESULT_PAGE_INDEX


    def generateHtml (self, page):
        style = Style()
        stylepath = style.getPageStyle (page)
        generator = HtmlGenerator (page)

        try:
            html = generator.makeHtml(stylepath)
        except:
            MessageBox (_(u"Page style Error. Style by default is used"),  
                    _(u"Error"),
                    wx.ICON_ERROR | wx.OK)

            html = generator.makeHtml (style.getDefaultStyle())

        return html


    def removeGui (self):
        super (WikiPageView, self).removeGui ()
        self.mainWindow.mainMenu.Remove (self.__WIKI_MENU_INDEX - 1)


    def _getAttachString (self, fnames):
        """
        Функция возвращает текст, который будет вставлен на страницу при вставке выбранных прикрепленных файлов из панели вложений

        Перегрузка метода из BaseTextPanel
        """
        text = ""
        count = len (fnames)

        for n in range (count):
            text += "Attach:" + fnames[n]
            if n != count -1:
                text += "\n"

        return text


    def updateHtml (self):
        """
        Сбросить кэш для того, чтобы заново сделать HTML
        """
        HtmlGenerator (self._currentpage).resetHash()
        if self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()
        elif self.selectedPageIndex == self.HTML_RESULT_PAGE_INDEX:
            self._onSwitchCodeHtml()
