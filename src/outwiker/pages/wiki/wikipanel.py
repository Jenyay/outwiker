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
from .thumbdialogcontroller import ThumbDialogController
from .linkcreator import LinkCreator
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.linkdialogcontroller import LinkDialogContoller
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from wikiconfig import WikiConfig
from htmlgenerator import HtmlGenerator

from actions.bold import WikiBoldAction
from actions.italic import WikiItalicAction
from actions.bolditalic import WikiBoldItalicAction
from actions.underline import WikiUnderlineAction
from actions.strike import WikiStrikeAction
from actions.subscript import WikiSubscriptAction
from actions.superscript import WikiSuperscriptAction
from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.monospace import WikiMonospaceAction
from actions.alignleft import WikiAlignLeftAction
from actions.alignright import WikiAlignRightAction
from actions.aligncenter import WikiAlignCenterAction
from actions.alignjustify import WikiAlignJustifyAction
from actions.preformat import WikiPreformatAction
from actions.nonparsed import WikiNonParsedAction


class WikiPagePanel (BaseHtmlPanel):
    HTML_RESULT_PAGE_INDEX = BaseHtmlPanel.RESULT_PAGE_INDEX + 1


    def __init__ (self, parent, *args, **kwds):
        super (WikiPagePanel, self).__init__ (parent, *args, **kwds)

        self._application = Application

        self._configSection = u"wiki"
        self._hashKey = u"md5_hash"
        self.__WIKI_MENU_INDEX = 7
        self.__toolbarName = "wiki"

        # Список действий, которые нужно удалять с панелей и из меню. 
        # А еще их надо дизаблить при переходе на вкладки просмотра результата или HTML
        self.__wikiNotationActions = [
                WikiBoldAction,
                WikiItalicAction,
                WikiBoldItalicAction,
                WikiUnderlineAction,
                WikiStrikeAction,
                WikiSubscriptAction,
                WikiSuperscriptAction,
                WikiFontSizeBigAction,
                WikiFontSizeSmallAction,
                WikiMonospaceAction,
                WikiAlignLeftAction,
                WikiAlignRightAction,
                WikiAlignCenterAction,
                WikiAlignJustifyAction,
                WikiPreformatAction,
                WikiNonParsedAction]

        self._wikiPanelName = "wiki"

        self.mainWindow.toolbars[self._wikiPanelName] = WikiToolBar(self.mainWindow, self.mainWindow.auiManager)
        self.mainWindow.toolbars[self._wikiPanelName].UpdateToolBar()

        self.notebook.SetPageText (0, _(u"Wiki"))

        self.htmlSizer = wx.FlexGridSizer(1, 1, 0, 0)
        self.htmlSizer.AddGrowableRow(0)
        self.htmlSizer.AddGrowableCol(0)

        # Номер вкладки с кодом HTML. -1, если вкладки нет
        self.htmlcodePageIndex = -1

        self.config = WikiConfig (Application.config)

        self.__createCustomTools()
        Application.mainWindow.updateShortcuts()

        if self.config.showHtmlCodeOptions.value:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()


    def onClose (self, event):
        self._removeActionTools()

        if self._wikiPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._wikiPanelName)

        super (WikiPagePanel, self).onClose (event)


    def _removeActionTools (self):
        actionController = Application.actionController

        map (lambda action: actionController.removeMenuItem (action.stringId), 
                self.__wikiNotationActions)

        if self._wikiPanelName in self.mainWindow.toolbars:
            map (lambda action: actionController.removeToolbarButton (action.stringId), 
                self.__wikiNotationActions)


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
        actionController = Application.actionController

        self.mainWindow.Freeze()

        map (lambda action: actionController.enableTools (action.stringId, enabled), 
                self.__wikiNotationActions)

        self.mainWindow.Thaw()


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self._enableActions (True)
        super (WikiPagePanel, self)._onSwitchToCode()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self._enableActions (False)
        super (WikiPagePanel, self)._onSwitchToPreview()


    def _onSwitchCodeHtml (self):
        assert self._currentpage != None

        self._enableActions (False)

        self.Save()
        status_item = 0
        setStatusText (_(u"Page rendered. Please wait…"), status_item)
        Application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

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
        Application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)

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
        Application.actionController.appendMenuItem (WikiBoldAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiBoldAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False)


        # Курсивный шрифт
        Application.actionController.appendMenuItem (WikiItalicAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiItalicAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False)

        # Полужирный курсивный шрифт
        Application.actionController.appendMenuItem (WikiBoldItalicAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiBoldItalicAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_bold_italic.png"),
                fullUpdate=False)


        # Подчеркнутый шрифт
        Application.actionController.appendMenuItem (WikiUnderlineAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiUnderlineAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False)


        # Зачеркнутый шрифт
        Application.actionController.appendMenuItem (WikiStrikeAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiStrikeAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False)


        # Нижний индекс
        Application.actionController.appendMenuItem (WikiSubscriptAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiSubscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False)


        # Верхний индекс
        Application.actionController.appendMenuItem (WikiSuperscriptAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiSuperscriptAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False)


        # Крупный шрифт
        Application.actionController.appendMenuItem (WikiFontSizeBigAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiFontSizeBigAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_big.png"),
                fullUpdate=False)


        # Мелкий шрифт
        Application.actionController.appendMenuItem (WikiFontSizeSmallAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiFontSizeSmallAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_small.png"),
                fullUpdate=False)


        # Моноширинный шрифт
        Application.actionController.appendMenuItem (WikiMonospaceAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiMonospaceAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_monospace.png"),
                fullUpdate=False)


    def __addAlignTools (self):
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__alignMenu

        # Выравнивание по левому краю
        Application.actionController.appendMenuItem (WikiAlignLeftAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignLeftAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False)


        # Выравнивание по центру
        Application.actionController.appendMenuItem (WikiAlignCenterAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignCenterAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False)


        # Выравнивание по правому краю
        Application.actionController.appendMenuItem (WikiAlignRightAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignRightAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False)


        # Выравнивание по ширине
        Application.actionController.appendMenuItem (WikiAlignJustifyAction.stringId, menu)
        Application.actionController.appendToolbarButton (WikiAlignJustifyAction.stringId, 
                toolbar,
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False)

    
    def __addFormatTools (self):
        toolbar = self.mainWindow.toolbars[self.__toolbarName]
        menu = self.__formatMenu

        # Форматированный текст
        Application.actionController.appendMenuItem (WikiPreformatAction.stringId, menu)

        # Текст, который не нужно разбирать википарсером
        Application.actionController.appendMenuItem (WikiNonParsedAction.stringId, menu)


    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        self.addTool (self.__listMenu, 
                "ID_MARK_LIST", 
                lambda event: self.codeEditor.turnList (u'* '), 
                _(u"Bullets list") + "\tCtrl+G", 
                _(u"Bullets list"), 
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__listMenu, 
                "ID_NUMBER_LIST", 
                lambda event: self.codeEditor.turnList (u'# '), 
                _(u"Numbers list") + "\tCtrl+J", 
                _(u"Numbers list"), 
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False,
                panelname="wiki")
    

    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        self.addTool (self.__headingMenu, 
                "ID_H1", 
                lambda event: self.codeEditor.turnText (u"\n!! ", u""), 
                _(u"H1") + "\tCtrl+1", 
                _(u"H1"), 
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H2", 
                lambda event: self.codeEditor.turnText (u"!!! ", u""), 
                _(u"H2") + "\tCtrl+2", 
                _(u"H2"), 
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False,
                panelname="wiki")
        
        self.addTool (self.__headingMenu, 
                "ID_H3", 
                lambda event: self.codeEditor.turnText (u"!!!! ", u""), 
                _(u"H3") + "\tCtrl+3", 
                _(u"H3"), 
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H4", 
                lambda event: self.codeEditor.turnText (u"!!!!! ", u""), 
                _(u"H4") + "\tCtrl+4", 
                _(u"H4"), 
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H5", 
                lambda event: self.codeEditor.turnText (u"!!!!!! ", u""), 
                _(u"H5") + "\tCtrl+5", 
                _(u"H5"), 
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H6", 
                lambda event: self.codeEditor.turnText (u"!!!!!!! ", u""), 
                _(u"H6") + "\tCtrl+6", 
                _(u"H6"), 
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False,
                panelname="wiki")
    

    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        self.addTool (self.__wikiMenu, 
                "ID_THUMB", 
                self.__onThumb,
                _(u"Thumbnail") + "\tCtrl+M", 
                _(u"Thumbnail"), 
                os.path.join (self.imagesDir, "images.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_LINK", 
                self.__onInsertLink, 
                _(u"Link") + "\tCtrl+L", 
                _(u'Link'), 
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__wikiMenu, 
                "ID_ANCHOR", 
                lambda event: self.codeEditor.turnText (u'[[#', u']]'), 
                _(u"Anchor") + "\tCtrl+Alt+N",
                _(u'Anchor'), 
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__wikiMenu, 
                "ID_HORLINE", 
                lambda event: self.codeEditor.replaceText (u'----'), 
                _(u"Horizontal line") + "\tCtrl+H", 
                _(u"Horizontal line"), 
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_LINEBREAK", 
                lambda event: self.codeEditor.replaceText (u'[[<<]]'), 
                _(u"Line break") + "\tCtrl+Return", 
                _(u"Line break"), 
                os.path.join (self.imagesDir, "linebreak.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_EQUATION", 
                lambda event: self.codeEditor.turnText (u'{$', u'$}'), 
                _(u"Equation") + "\tCtrl+Q", 
                _(u'Equation'), 
                os.path.join (self.imagesDir, "equation.png"),
                fullUpdate=False,
                panelname="wiki")

        self.__wikiMenu.AppendSeparator()

        self.addTool (self.__wikiMenu, 
                "ID_ESCAPEHTML", 
                self.codeEditor.escapeHtml, 
                _(u"Convert HTML Symbols"), 
                _(u"Convert HTML Symbols"), 
                None,
                fullUpdate=False,
                panelname="wiki")


    def __createCustomTools (self):
        assert self.mainWindow != None

        self.__wikiMenu = wx.Menu()

        self.__headingMenu = wx.Menu()
        self.__fontMenu = wx.Menu()
        self.__alignMenu = wx.Menu()
        self.__formatMenu = wx.Menu()
        self.__listMenu = wx.Menu()
        self.__commandsMenu = wx.Menu()

        self.mainWindow.Freeze()

        self._addRenderTools()

        self.addTool (self.__wikiMenu, 
                "ID_HTMLCODE", 
                self.__openHtmlCode, 
                _(u"HTML Code") + "\tShift+F4", 
                _(u"HTML Code"), 
                os.path.join (self.imagesDir, "html.png"),
                True,
                fullUpdate=False,
                panelname=self.mainWindow.GENERAL_TOOLBAR_STR)

        self.addTool (self.__wikiMenu, 
                "ID_UPDATE_HTML", 
                self.__updateHtml, 
                _(u"Update HTML Code") + "\tCtrl+F4", 
                _(u"Update HTML Code"), 
                None,
                True,
                fullUpdate=False,
                panelname="wiki")

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

        self.mainWindow.Thaw()


    @property
    def commandsMenu (self):
        """
        Свойство возвращает меню с вики-командами
        """
        return self.__commandsMenu

    
    def __addCommandsTools (self):
        self.addTool (self.commandsMenu, 
                "ID_ATTACHLIST", 
                lambda event: self.codeEditor.replaceText (u"(:attachlist:)"), 
                _(u"Attachment (:attachlist:)"), 
                _(u"Attachment (:attachlist:)"), 
                None,
                fullUpdate=False)

        self.addTool (self.commandsMenu, 
                "ID_CHILDLIST", 
                lambda event: self.codeEditor.replaceText (u"(:childlist:)"), 
                _(u"Children (:childlist:)"), 
                _(u"Children (:childlist:)"), 
                None,
                fullUpdate=False)

        self.addTool (self.commandsMenu, 
                "ID_INCLUDE", 
                lambda event: self.codeEditor.turnText (u"(:include ", u":)"), 
                _(u"Include (:include ...:)"), 
                _(u"Include (:include ...:)"), 
                None,
                fullUpdate=False)


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


    def __openHtmlCode (self, event):
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
        super (WikiPagePanel, self).removeGui ()
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


    def __onInsertLink (self, event):
        linkController = LinkDialogContoller (self, self.codeEditor.GetSelectedText())
        if linkController.showDialog() == wx.ID_OK:
            linkCreator = LinkCreator (self.config)
            text = linkCreator.create (linkController.link, linkController.comment)
            self.codeEditor.replaceText (text)


    def __onThumb (self, event):
        dlgController = ThumbDialogController (self, 
                self._currentpage, 
                self.codeEditor.GetSelectedText())

        if dlgController.showDialog() == wx.ID_OK:
            self.codeEditor.replaceText (dlgController.result)


    def selectFontSize (self, selIndex):
        fontSizeSelector = FontSizeSelector (self._application.mainWindow)
        notation = fontSizeSelector.selectFontSize (selIndex)

        codeEditor = self._application.mainWindow.pagePanel.pageView.codeEditor
        codeEditor.turnText (notation[0], notation[1])


    def __updateHtml (self, event):
        """
        Сбросить кэш для того, чтобы заново сделать HTML
        """
        HtmlGenerator (self._currentpage).resetHash()
        if self.selectedPageIndex == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()
        elif self.selectedPageIndex == self.HTML_RESULT_PAGE_INDEX:
            self._onSwitchCodeHtml()

