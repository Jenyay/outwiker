# -*- coding: utf-8 -*-

import os
import re

import wx

from outwiker.core.commands import MessageBox
from outwiker.core.application import Application
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.style import Style

from outwiker.gui.linkdialogcontroller import LinkDialogContoller

from .htmltoolbar import HtmlToolBar
from .basehtmlpanel import BaseHtmlPanel


class HtmlPagePanel (BaseHtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        super (HtmlPagePanel, self).__init__ (parent, *args, **kwds)

        self._htmlPanelName = "html"

        self.mainWindow.toolbars[self._htmlPanelName] = HtmlToolBar(self.mainWindow, self.mainWindow.auiManager)
        self.mainWindow.toolbars[self._htmlPanelName].UpdateToolBar()

        self.__HTML_MENU_INDEX = 7
        self.__createCustomTools()

        Application.onPageUpdate += self.__onPageUpdate


    @property
    def toolsMenu (self):
        return self.__htmlMenu


    def onClose (self, event):
        Application.onPageUpdate -= self.__onPageUpdate

        if self._htmlPanelName in self.mainWindow.toolbars:
            self.mainWindow.toolbars.destroyToolBar (self._htmlPanelName)

        super (HtmlPagePanel, self).onClose (event)


    def __onPageUpdate (self, sender):
        if sender == self._currentpage:
            self.__updatePageConfigTools()
            if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
                self._showHtml()


    def UpdateView (self, page):
        self.__updatePageConfigTools()
        BaseHtmlPanel.UpdateView (self, page)


    def __createPageConfigTools (self):
        """
        Создать кнопки и пункты меню, отображающие настройки страницы
        """
        self.addCheckTool (self.__htmlMenu, 
                "ID_AUTOLINEWRAP", 
                self.__onAutoLineWrap, 
                _(u"Auto Line Wrap"), 
                _(u"Auto Line Wrap"), 
                os.path.join (self.imagesDir, "linewrap.png"),
                alwaysEnabled = True,
                fullUpdate=False,
                panelname="html")

        self.__updatePageConfigTools()


    def __updatePageConfigTools (self):
        if self._currentpage != None:
            self.checkTools ("ID_AUTOLINEWRAP", self._currentpage.autoLineWrap)


    def __onAutoLineWrap (self, event):
        if self._currentpage != None:
            self._currentpage.autoLineWrap = event.Checked()
            self.__updatePageConfigTools()


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

        self.__createPageConfigTools ()
        self._addRenderTools()

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
        self.__addOtherTools()

        self.mainWindow.Thaw()

        self.mainWindow.mainMenu.Insert (self.__HTML_MENU_INDEX, self.__htmlMenu, _(u"H&tml"))


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        self.addTool (self.__fontMenu, 
                "ID_BOLD", 
                lambda event: self.codeEditor.turnText (u"<b>", u"</b>"), 
                _(u"Bold\tCtrl+B"), 
                _(u"Bold (<b>…</b>)"), 
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__fontMenu, 
                "ID_ITALIC", 
                lambda event: self.codeEditor.turnText (u"<i>", u"</i>"), 
                _(u"Italic\tCtrl+I"), 
                _(u"Italic (<i>…</i>)"), 
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__fontMenu, 
                "ID_UNDERLINE", 
                lambda event: self.codeEditor.turnText (u"<u>", u"</u>"), 
                _(u"Underline\tCtrl+U"), 
                _(u"Underline (<u>…</u>)"), 
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__fontMenu, 
                "ID_STRIKE", 
                lambda event: self.codeEditor.turnText (u"<strike>", u"</strike>"), 
                _(u"Strikethrough\tCtrl+K"), 
                _(u"Strikethrough (<strike>…</strike>)"), 
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__fontMenu, 
                "ID_SUBSCRIPT", 
                lambda event: self.codeEditor.turnText (u"<sub>", u"</sub>"), 
                _(u"Subscript\tCtrl+="), 
                _(u"Subscript (<sub>…</sub>)"), 
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__fontMenu, 
                "ID_SUPERSCRIPT", 
                lambda event: self.codeEditor.turnText (u"<sup>", u"</sup>"), 
                _(u"Superscript\tCtrl++"), 
                _(u"Superscript (<sup>…</sup>)"), 
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False,
                panelname="html")

    
    def __addAlignTools (self):
        self.addTool (self.__alignMenu, 
                "ID_ALIGN_LEFT", 
                lambda event: self.codeEditor.turnText (u'<div align="left">', u'</div>'), 
                _(u"Left align\tCtrl+Alt+L"), 
                _(u"Left align"), 
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__alignMenu, 
                "ID_ALIGN_CENTER", 
                lambda event: self.codeEditor.turnText (u'<div align="center">', u'</div>'), 
                _(u"Center align\tCtrl+Alt+C"), 
                _(u"Center align"), 
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__alignMenu, 
                "ID_ALIGN_RIGHT", 
                lambda event: self.codeEditor.turnText (u'<div align="right">', u'</div>'), 
                _(u"Right align\tCtrl+Alt+R"), 
                _(u"Right align"), 
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False,
                panelname="html")
    
        self.addTool (self.__alignMenu, 
                "ID_ALIGN_JUSTIFY", 
                lambda event: self.codeEditor.turnText (u'<div align="justify">', u'</div>'), 
                _(u"Justify align\tCtrl+Alt+J"), 
                _(u"Justify align"), 
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False,
                panelname="html")


    def __addTableTools (self):
        """
        Добавить инструменты, связанные с таблицами
        """
        self.addTool (self.__tableMenu, 
                "ID_TABLE", 
                lambda event: self.codeEditor.turnText (u'<table>', u'</table>'), 
                _(u"Table\tCtrl+Q"), 
                _(u"Table (<table>…</table>)"), 
                os.path.join (self.imagesDir, "table.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__tableMenu, 
                "ID_TABLE_TR", 
                lambda event: self.codeEditor.turnText (u'<tr>',u'</tr>'), 
                _(u"Table row\tCtrl+W"), 
                _(u"Table row (<tr>…</tr>)"), 
                os.path.join (self.imagesDir, "table_insert_row.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__tableMenu, 
                "ID_TABLE_TD", 
                lambda event: self.codeEditor.turnText (u'<td>', u'</td>'), 
                _(u"Table cell\tCtrl+Y"), 
                _(u"Table cell (<td>…</td>)"), 
                os.path.join (self.imagesDir, "table_insert_cell.png"),
                fullUpdate=False,
                panelname="html")

    
    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        self.addTool (self.__listMenu, 
                "ID_MARK_LIST", 
                lambda event: self.codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'), 
                _(u"Bullets list\tCtrl+G"), 
                _(u"Bullets list (<ul>…</ul>)"), 
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__listMenu, 
                "ID_NUMBER_LIST", 
                lambda event: self.codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'), 
                _(u"Numbers list\tCtrl+J"), 
                _(u"Numbers list (<ul>…</ul>)"), 
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False,
                panelname="html")
    

    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        self.addTool (self.__headingMenu, 
                "ID_H1", 
                lambda event: self.codeEditor.turnText (u"<h1>", u"</h1>"), 
                _(u"H1\tCtrl+1"), 
                _(u"H1 (<h1>…</h1>)"), 
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H2", 
                lambda event: self.codeEditor.turnText (u"<h2>", u"</h2>"), 
                _(u"H2\tCtrl+2"), 
                _(u"H2 (<h2>…</h2>)"), 
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False,
                panelname="html")
        
        self.addTool (self.__headingMenu, 
                "ID_H3", 
                lambda event: self.codeEditor.turnText (u"<h3>", u"</h3>"), 
                _(u"H3\tCtrl+3"), 
                _(u"H3 (<h3>…</h3>)"), 
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H4", 
                lambda event: self.codeEditor.turnText (u"<h4>", u"</h4>"), 
                _(u"H4\tCtrl+4"), 
                _(u"H4 (<h4>…</h4>)"), 
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H5", 
                lambda event: self.codeEditor.turnText (u"<h5>", u"</h5>"), 
                _(u"H5\tCtrl+5"), 
                _(u"H5 (<h5>…</h5>)"), 
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__headingMenu, 
                "ID_H6", 
                lambda event: self.codeEditor.turnText (u"<h6>", u"</h6>"), 
                _(u"H6\tCtrl+6"), 
                _(u"H6 (<h6>…</h6>)"), 
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False,
                panelname="html")
    

    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        self.addTool (self.__htmlMenu, 
                "ID_IMAGE", 
                lambda event: self.codeEditor.turnText (u'<img src="', u'"/>'), 
                _(u'Image\tCtrl+M'), 
                _(u'Image (<img src="…"/>'), 
                os.path.join (self.imagesDir, "image.png"),
                fullUpdate=False,
                panelname="html")

        self.addTool (self.__htmlMenu, 
                "ID_LINK", 
                self.__onInsertLink, 
                _(u"Link\tCtrl+L"), 
                _(u'Link (<a href="…">…</a>)'), 
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__htmlMenu, 
                "ID_ANCHOR", 
                lambda event: self.codeEditor.turnText (u'<a name="', u'"></a>'), 
                _(u"Anchor\tCtrl+Alt+L"), 
                _(u'Anchor (<a name="…">…</a>)'), 
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__htmlMenu, 
                "ID_HORLINE", 
                lambda event: self.codeEditor.replaceText (u'<hr>'), 
                _(u"Horizontal line\tCtrl+H"), 
                _(u"Horizontal line (<hr>)"), 
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__formatMenu, 
                "ID_CODE", 
                lambda event: self.codeEditor.turnText (u"<code>", u"</code>"), 
                _(u"Code\tCtrl+Alt+D"), 
                _(u"Code (<code>…</code>)"), 
                os.path.join (self.imagesDir, "code.png"),
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__formatMenu, 
                "ID_PREFORMAT", 
                lambda event: self.codeEditor.turnText (u"<pre>", u"</pre>"), 
                _(u"Preformat\tCtrl+Alt+F"), 
                _(u"Preformat (<pre>…</pre>)"), 
                None,
                fullUpdate=False,
                panelname="html")


        self.addTool (self.__formatMenu, 
                "ID_BLOCKQUOTE", 
                lambda event: self.codeEditor.turnText (u"<blockquote>", u"</blockquote>"), 
                _(u"Quote\tCtrl+Alt+Q"), 
                _(u"Quote (<blockquote>…</blockquote>)"), 
                os.path.join (self.imagesDir, "quote.png"),
                fullUpdate=False,
                panelname="html")


        self.__htmlMenu.AppendSeparator()

        self.addTool (self.__htmlMenu, 
                "ID_ESCAPEHTML", 
                self.codeEditor.escapeHtml, 
                _(u"Convert HTML Symbols"), 
                _(u"Convert HTML Symbols"), 
                None,
                fullUpdate=False,
                panelname="html")


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


    def __onInsertLink (self, event):
        linkController = LinkDialogContoller (self, self.codeEditor.GetSelectedText())

        if linkController.showDialog() == wx.ID_OK:
            text = u'<a href="{link}">{comment}</a>'.format (comment=linkController.comment, 
                    link=linkController.link)

            self.codeEditor.replaceText (text)

