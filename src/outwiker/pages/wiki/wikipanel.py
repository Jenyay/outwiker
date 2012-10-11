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
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.linkdialogcontroller import LinkDialogContoller
from outwiker.pages.html.basehtmlpanel import BaseHtmlPanel
from wikiconfig import WikiConfig
from htmlgenerator import HtmlGenerator


class WikiPagePanel (BaseHtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        super (WikiPagePanel, self).__init__ (parent, *args, **kwds)

        self._configSection = u"wiki"
        self._hashKey = u"md5_hash"
        self.__WIKI_MENU_INDEX = 7

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

        if self.config.showHtmlCodeOptions.value:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.Layout()


    def onClose (self, event):
        if self._wikiPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._wikiPanelName)

        super (WikiPagePanel, self).onClose (event)


    @property
    def toolsMenu (self):
        return self.__wikiMenu


    def __createHtmlCodePanel (self, parentSizer):
        # Окно для просмотра получившегося кода HTML
        self.htmlCodeWindow = HtmlTextEditor(self.notebook, -1)
        self.htmlCodeWindow.SetReadOnly (True)
        parentSizer.Add(self.htmlCodeWindow, 1, wx.TOP|wx.BOTTOM|wx.EXPAND, 2)
        
        self.notebook.AddPage (self.htmlCodeWindow, _("HTML"))
        return self.notebook.GetPageCount () - 1
    

    def GetTextEditor(self):
        return WikiEditor


    def GetSearchPanel (self):
        if self.notebook.GetSelection() == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel
        elif self.notebook.GetSelection() == self.htmlcodePageIndex:
            return self.htmlCodeWindow.searchPanel

        return None


    def onTabChanged(self, event):
        if self._currentpage == None:
            return

        if self.notebook.GetSelection() == self.CODE_PAGE_INDEX:
            self._onSwitchToCode()

        elif self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()

        elif self.notebook.GetSelection() == self.htmlcodePageIndex:
            self._onSwitchCodeHtml()


    def _onSwitchCodeHtml (self):
        assert self._currentpage != None

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
        self.addTool (self.__fontMenu, 
                "ID_BOLD", 
                lambda event: self.codeEditor.turnText (u"'''", u"'''"), 
                _(u"Bold\tCtrl+B"), 
                _(u"Bold"), 
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_ITALIC", 
                lambda event: self.codeEditor.turnText (u"''", u"''"), 
                _(u"Italic\tCtrl+I"), 
                _(u"Italic"), 
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_BOLD_ITALIC", 
                lambda event: self.codeEditor.turnText (u"''''", u"''''"), 
                _(u"Bold italic\tCtrl+Shift+I"), 
                _(u"Bold italic"), 
                os.path.join (self.imagesDir, "text_bold_italic.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_UNDERLINE", 
                lambda event: self.codeEditor.turnText (u"{+", u"+}"), 
                _(u"Underline\tCtrl+U"), 
                _(u"Underline"), 
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_STRIKE", 
                lambda event: self.codeEditor.turnText (u"{-", u"-}"), 
                _(u"Strikethrough\tCtrl+K"), 
                _(u"Strikethrough"), 
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_SUBSCRIPT", 
                lambda event: self.codeEditor.turnText (u"'_", u"_'"), 
                _(u"Subscript\tCtrl+="), 
                _(u"Subscript"), 
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__fontMenu, 
                "ID_SUPERSCRIPT", 
                lambda event: self.codeEditor.turnText (u"'^", u"^'"), 
                _(u"Superscript\tCtrl++"), 
                _(u"Superscript"), 
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__fontMenu, 
                "ID_MONOSPACED", 
                lambda event: self.codeEditor.turnText (u"@@", u"@@"), 
                _(u"Monospaced\tCtrl+@"), 
                _(u"Monospaced"), 
                os.path.join (self.imagesDir, "text_monospace.png"),
                fullUpdate=False,
                panelname="wiki")
    

    def __addAlignTools (self):
        self.addTool (self.__alignMenu, 
                "ID_ALIGN_LEFT", 
                lambda event: self.codeEditor.turnText (u"%left%", u""), 
                _(u"Left align\tCtrl+Alt+L"), 
                _(u"Left align"), 
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__alignMenu, 
                "ID_ALIGN_CENTER", 
                lambda event: self.codeEditor.turnText (u"%center%", u""), 
                _(u"Center align\tCtrl+Alt+C"), 
                _(u"Center align"), 
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__alignMenu, 
                "ID_ALIGN_RIGHT", 
                lambda event: self.codeEditor.turnText (u"%right%", u""), 
                _(u"Right align\tCtrl+Alt+R"), 
                _(u"Right align"), 
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False,
                panelname="wiki")
    
        self.addTool (self.__alignMenu, 
                "ID_ALIGN_JUSTIFY", 
                lambda event: self.codeEditor.turnText (u"%justify%", u""), 
                _(u"Justify align\tCtrl+Alt+J"), 
                _(u"Justify align"), 
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False,
                panelname="wiki")


    def __addFormatTools (self):
        self.addTool (self.__formatMenu, 
                "ID_PREFORMAT", 
                lambda event: self.codeEditor.turnText (u"[@", u"@]"), 
                _(u"Preformat [@…@]\tCtrl+Alt+F"), 
                _(u"Preformat [@…@]"),
                None,
                fullUpdate=False)

        self.addTool (self.__formatMenu, 
                "ID_NONFORMAT", 
                lambda event: self.codeEditor.turnText (u"[=", u"=]"), 
                _(u"Non-parsed [=…=]"), 
                _(u"Non-parsed [=…=]"), 
                None,
                fullUpdate=False,
                panelname="wiki")

    
    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        self.addTool (self.__listMenu, 
                "ID_MARK_LIST", 
                lambda event: self.codeEditor.turnList (u'* '), 
                _(u"Bullets list\tCtrl+G"), 
                _(u"Bullets list"), 
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__listMenu, 
                "ID_NUMBER_LIST", 
                lambda event: self.codeEditor.turnList (u'# '), 
                _(u"Numbers list\tCtrl+J"), 
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
                _(u"H1\tCtrl+1"), 
                _(u"H1"), 
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H2", 
                lambda event: self.codeEditor.turnText (u"!!! ", u""), 
                _(u"H2\tCtrl+2"), 
                _(u"H2"), 
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False,
                panelname="wiki")
        
        self.addTool (self.__headingMenu, 
                "ID_H3", 
                lambda event: self.codeEditor.turnText (u"!!!! ", u""), 
                _(u"H3\tCtrl+3"), 
                _(u"H3"), 
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H4", 
                lambda event: self.codeEditor.turnText (u"!!!!! ", u""), 
                _(u"H4\tCtrl+4"), 
                _(u"H4"), 
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H5", 
                lambda event: self.codeEditor.turnText (u"!!!!!! ", u""), 
                _(u"H5\tCtrl+5"), 
                _(u"H5"), 
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__headingMenu, 
                "ID_H6", 
                lambda event: self.codeEditor.turnText (u"!!!!!!! ", u""), 
                _(u"H6\tCtrl+6"), 
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
                _(u'Thumbnail\tCtrl+M'), 
                _(u'Thumbnail'), 
                os.path.join (self.imagesDir, "images.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_LINK", 
                self.__onInsertLink, 
                _(u"Link\tCtrl+L"), 
                _(u'Link'), 
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__wikiMenu, 
                "ID_ANCHOR", 
                lambda event: self.codeEditor.turnText (u'[[#', u']]'), 
                _(u"Anchor\tCtrl+Alt+L"), 
                _(u'Anchor'), 
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False,
                panelname="wiki")


        self.addTool (self.__wikiMenu, 
                "ID_HORLINE", 
                lambda event: self.codeEditor.replaceText (u'----'), 
                _(u"Horizontal line\tCtrl+H"), 
                _(u"Horizontal line"), 
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_LINEBREAK", 
                lambda event: self.codeEditor.replaceText (u'[[<<]]'), 
                _(u"Line break\tCtrl+Return"), 
                _(u"Line break"), 
                os.path.join (self.imagesDir, "linebreak.png"),
                fullUpdate=False,
                panelname="wiki")

        self.addTool (self.__wikiMenu, 
                "ID_EQUATION", 
                lambda event: self.codeEditor.turnText (u'{$', u'$}'), 
                _(u"Equation\tCtrl+Q"), 
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

        self.addTool (self.__wikiMenu, 
                "ID_HTMLCODE", 
                self.__openHtmlCode, 
                _(u"HTML Code\tShift+F4"), 
                _(u"HTML Code"), 
                os.path.join (self.imagesDir, "html.png"),
                True,
                fullUpdate=False,
                panelname=self.mainWindow.GENERAL_TOOLBAR_STR)


        self._addRenderTools()
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
                _(u"&Wiki") )

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


    def __openHtmlCode (self, event):
        if self.htmlcodePageIndex == -1:
            self.htmlcodePageIndex = self.__createHtmlCodePanel(self.htmlSizer)

        self.notebook.SetSelection (self.htmlcodePageIndex)

    
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
            if linkController.comment == linkController.link:
                text = u"[[{link}]]".format (link=linkController.link)
            else:
                text = u"[[{comment} -> {link}]]".format (comment=linkController.comment, 
                        link=linkController.link)

            self.codeEditor.replaceText (text)


    def __onThumb (self, event):
        dlgController = ThumbDialogController (self, 
                self._currentpage, 
                self.codeEditor.GetSelectedText())

        if dlgController.showDialog() == wx.ID_OK:
            # self.codeEditor.turnText (u'%thumb%', u'%%')
            self.codeEditor.replaceText (dlgController.result)

