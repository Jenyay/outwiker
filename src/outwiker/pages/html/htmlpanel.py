# -*- coding: utf-8 -*-

import os
import re
from abc import ABCMeta, abstractmethod, abstractproperty

import wx

from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import getTemplatesDir, getImagesDir
from outwiker.core.style import Style

from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmlrenderfactory import getHtmlRender
from outwiker.gui.htmltexteditor import HtmlTextEditor


class HtmlPanel(BaseTextPanel):
    __metaclass__ = ABCMeta
    
    def __init__(self, parent, *args, **kwds):
        BaseTextPanel.__init__ (self, parent, *args, **kwds)

        self._htmlFile = "__content.html"
        self.currentHtmlFile = None

        # Номера страниц-вкладок
        self.CODE_PAGE_INDEX = 0
        self.RESULT_PAGE_INDEX = 1

        self.imagesDir = getImagesDir()

        self.notebook = wx.Notebook(self, -1, style=wx.NB_BOTTOM)
        self.codeEditor = self.GetTextEditor()(self.notebook)
        self.htmlWindow = getHtmlRender (self.notebook)

        self.__do_layout()

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.onTabChanged, self.notebook)
        self.Bind (wx.EVT_CLOSE, self.onClose)


    @abstractproperty
    def toolsMenu (self):
        pass


    def addTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled=False,
            fullUpdate=True):
        """
        Добавить пункт меню и кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        """
        BaseTextPanel.addTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled,
            fullUpdate)
        
        tool = self._tools[idstring]
        self.enableTool (tool, self._isEnabledTool (tool))


    def addCheckTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled = False,
            fullUpdate=True):
        """
        Добавить пункт меню с галкой и залипающую кнопку на панель
        menu -- меню для добавления элемента
        id -- идентификатор меню и кнопки
        func -- обработчик
        menuText -- название пунта меню
        buttonText -- подсказка для кнопки
        image -- имя файла с картинкой
        alwaysEnabled -- Кнопка должна быть всегда активна
        """
        BaseTextPanel.addCheckTool (self, 
            menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled,
            fullUpdate)

        tool = self._tools[idstring]
        self.enableTool (tool, self._isEnabledTool (tool))


    def Print (self):
        currpanel = self.notebook.GetCurrentPage()
        if currpanel != None:
            currpanel.Print()


    def GetTextEditor(self):
        return HtmlTextEditor

    
    def onPreferencesDialogClose (self, prefDialog):
        self.codeEditor.setDefaultSettings()

    
    def onClose (self, event):
        self.htmlWindow.Close()


    def onAttachmentPaste (self, fnames):
        text = self._getAttachString (fnames)
        self.codeEditor.AddText (text)
        self.codeEditor.SetFocus()

    
    def UpdateView (self, page):
        self.Freeze()

        try:
            self.htmlWindow.page = self._currentpage

            self.codeEditor.SetReadOnly (False)
            self.codeEditor.SetText (self._currentpage.content)
            self.codeEditor.EmptyUndoBuffer()
            self.codeEditor.SetReadOnly (page.readonly)

            self._showHtml()
            self._openDefaultPage()
        finally:
            self.Thaw()


    def GetContentFromGui(self):
        return self.codeEditor.GetText()
    
    
    def __do_layout(self):
        self.notebook.AddPage(self.codeEditor, _("HTML"))
        self.notebook.AddPage(self.htmlWindow, _("Preview"))

        mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
        mainSizer.Add(self.notebook, 1, wx.EXPAND, 0)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)

        self.SetSizer(mainSizer)
        self.Layout()


    @abstractmethod
    def generateHtml (self, page):
        pass


    def getHtmlPath (self, path):
        """
        Получить путь до результирующего файла HTML
        """
        path = os.path.join (self._currentpage.path, self._htmlFile)
        return path


    def _openDefaultPage(self):
        assert self._currentpage != None

        if (len (self._currentpage.content) > 0 or 
                len (Attachment (self._currentpage).attachmentFull) > 0):
            self.notebook.SetSelection (self.RESULT_PAGE_INDEX)
        else:
            self.notebook.SetSelection (self.CODE_PAGE_INDEX)
            self.codeEditor.SetFocus()


    def onTabChanged(self, event):
        if self._currentpage == None:
            return

        if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
            self._onSwitchToPreview()
        else:
            self._onSwitchToCode()


    def _onSwitchToCode (self):
        """
        Обработка события при переключении на код страницы
        """
        self.checkForExternalEditAndSave()
        self._enableAllTools ()
        self.codeEditor.SetFocus()


    def _onSwitchToPreview (self):
        """
        Обработка события при переключении на просмотр страницы
        """
        self.Save()
        self._enableAllTools ()
        self.htmlWindow.SetFocus()
        self.htmlWindow.Update()
        self._showHtml()


    def _showHtml (self):
        """
        Подготовить и показать HTML текущей страницы
        """
        assert self._currentpage != None

        setStatusText (_(u"Page rendered. Please wait…") )
        Application.onHtmlRenderingBegin (self._currentpage, self.htmlWindow)

        try:
            self.currentHtmlFile = self.generateHtml (self._currentpage)
            self.htmlWindow.LoadPage (self.currentHtmlFile)
        except IOError as e:
            # TODO: Проверить под Windows
            MessageBox (_(u"Can't save file %s") % (unicode (e.filename)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)
        except OSError as e:
            MessageBox (_(u"Can't save HTML-file\n\n%s") % (unicode (e)), 
                    _(u"Error"), 
                    wx.ICON_ERROR | wx.OK)

        setStatusText (u"")
        Application.onHtmlRenderingEnd (self._currentpage, self.htmlWindow)
    

    def _enableAllTools (self):
        """
        Активировать или дезактивировать инструменты (пункты меню и кнопки) в зависимости от текущей выбранной вкладки
        """
        self.mainWindow.Freeze()

        for tool in self.allTools:
            self.enableTool (tool, self._isEnabledTool (tool))

        # Отдельно проверим возможность работы поиска по странице
        # Поиск не должен работать только на странице просмотра
        searchEnabled = self.notebook.GetSelection() != self.RESULT_PAGE_INDEX
        self.enableTool (self._tools[u"ID_BASE_SEARCH"], searchEnabled)
        self.enableTool (self._tools[u"ID_BASE_SEARCH_PREV"], searchEnabled)
        self.enableTool (self._tools[u"ID_BASE_SEARCH_NEXT"], searchEnabled)
        self.mainWindow.mainToolbar.UpdateAuiManager()
        
        self.mainWindow.Thaw()


    def _isEnabledTool (self, tool):
        if "notebook" not in dir (self):
            return True

        assert self.notebook != None
        assert self.notebook.GetSelection() != -1

        enabled = (tool.alwaysEnabled or
                self.notebook.GetSelection() == self.CODE_PAGE_INDEX)

        return enabled


    def GetSearchPanel (self):
        if self.notebook.GetSelection() == self.CODE_PAGE_INDEX:
            return self.codeEditor.searchPanel

        return None


    def _addRenderTools (self):
        self.addTool (self.toolsMenu, 
                "ID_RENDER", 
                self.__switchView, 
                _(u"Code / Preview\tF4"), 
                _(u"Code / Preview"), 
                os.path.join (self.imagesDir, "render.png"),
                True,
                False)

        self.toolsMenu.AppendSeparator()


    def __switchView (self, event):
        if self._currentpage == None:
            return

        if self.notebook.GetSelection() == self.CODE_PAGE_INDEX:
            self.notebook.SetSelection (self.RESULT_PAGE_INDEX)
        else:
            self.notebook.SetSelection (self.CODE_PAGE_INDEX)



# end of class HtmlPanel

class HtmlPagePanel (HtmlPanel):
    def __init__ (self, parent, *args, **kwds):
        HtmlPanel.__init__ (self, parent, *args, **kwds)

        self.__HTML_MENU_INDEX = 7
        self.__createCustomTools()

        Application.onPageUpdate += self.__onPageUpdate


    @property
    def toolsMenu (self):
        return self.__htmlMenu


    def onClose (self, event):
        Application.onPageUpdate -= self.__onPageUpdate
        HtmlPanel.onClose (self, event)


    def __onPageUpdate (self, sender):
        if sender == self._currentpage:
            self.__updatePageConfigTools()
            if self.notebook.GetSelection() == self.RESULT_PAGE_INDEX:
                self._showHtml()


    def UpdateView (self, page):
        self.__updatePageConfigTools()
        HtmlPanel.UpdateView (self, page)


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
                fullUpdate=False)

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
        
        self.mainWindow.Freeze()

        self.__createPageConfigTools ()
        self._addRenderTools()
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
        self.addTool (self.__htmlMenu, 
                "ID_BOLD", 
                lambda event: self.codeEditor.turnText (u"<b>", u"</b>"), 
                _(u"Bold\tCtrl+B"), 
                _(u"Bold (<b>…</b>)"), 
                os.path.join (self.imagesDir, "text_bold.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_ITALIC", 
                lambda event: self.codeEditor.turnText (u"<i>", u"</i>"), 
                _(u"Italic\tCtrl+I"), 
                _(u"Italic (<i>…</i>)"), 
                os.path.join (self.imagesDir, "text_italic.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_UNDERLINE", 
                lambda event: self.codeEditor.turnText (u"<u>", u"</u>"), 
                _(u"Underline\tCtrl+U"), 
                _(u"Underline (<u>…</u>)"), 
                os.path.join (self.imagesDir, "text_underline.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_STRIKE", 
                lambda event: self.codeEditor.turnText (u"<strike>", u"</strike>"), 
                _(u"Strikethrough\tCtrl+K"), 
                _(u"Strikethrough (<strike>…</strike>)"), 
                os.path.join (self.imagesDir, "text_strikethrough.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_SUBSCRIPT", 
                lambda event: self.codeEditor.turnText (u"<sub>", u"</sub>"), 
                _(u"Subscript\tCtrl+="), 
                _(u"Subscript (<sub>…</sub>)"), 
                os.path.join (self.imagesDir, "text_subscript.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_SUPERSCRIPT", 
                lambda event: self.codeEditor.turnText (u"<sup>", u"</sup>"), 
                _(u"Superscript\tCtrl++"), 
                _(u"Superscript (<sup>…</sup>)"), 
                os.path.join (self.imagesDir, "text_superscript.png"),
                fullUpdate=False)

    
    def __addAlignTools (self):
        self.addTool (self.__htmlMenu, 
                "ID_ALIGN_LEFT", 
                lambda event: self.codeEditor.turnText (u'<div align="left">', u'</div>'), 
                _(u"Left align\tCtrl+Alt+L"), 
                _(u"Left align"), 
                os.path.join (self.imagesDir, "text_align_left.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_ALIGN_CENTER", 
                lambda event: self.codeEditor.turnText (u'<div align="center">', u'</div>'), 
                _(u"Center align\tCtrl+Alt+C"), 
                _(u"Center align"), 
                os.path.join (self.imagesDir, "text_align_center.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_ALIGN_RIGHT", 
                lambda event: self.codeEditor.turnText (u'<div align="right">', u'</div>'), 
                _(u"Right align\tCtrl+Alt+R"), 
                _(u"Right align"), 
                os.path.join (self.imagesDir, "text_align_right.png"),
                fullUpdate=False)
    
        self.addTool (self.__htmlMenu, 
                "ID_ALIGN_JUSTIFY", 
                lambda event: self.codeEditor.turnText (u'<div align="justify">', u'</div>'), 
                _(u"Justify align\tCtrl+Alt+J"), 
                _(u"Justify align"), 
                os.path.join (self.imagesDir, "text_align_justify.png"),
                fullUpdate=False)


    def __addTableTools (self):
        """
        Добавить инструменты, связанные с таблицами
        """
        self.addTool (self.__htmlMenu, 
                "ID_TABLE", 
                lambda event: self.codeEditor.turnText (u'<table>', u'</table>'), 
                _(u"Table\tCtrl+Q"), 
                _(u"Table (<table>…</table>)"), 
                os.path.join (self.imagesDir, "table.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_TABLE_TR", 
                lambda event: self.codeEditor.turnText (u'<tr>',u'</tr>'), 
                _(u"Table row\tCtrl+W"), 
                _(u"Table row (<tr>…</tr>)"), 
                os.path.join (self.imagesDir, "table_insert_row.png"),
                fullUpdate=False)


        self.addTool (self.__htmlMenu, 
                "ID_TABLE_TD", 
                lambda event: self.codeEditor.turnText (u'<td>', u'</td>'), 
                _(u"Table cell\tCtrl+Y"), 
                _(u"Table cell (<td>…</td>)"), 
                os.path.join (self.imagesDir, "table_insert_cell.png"),
                fullUpdate=False)

    
    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        self.addTool (self.__htmlMenu, 
                "ID_MARK_LIST", 
                lambda event: self.codeEditor.turnList (u'<ul>\n', u'</ul>', u'<li>', u'</li>'), 
                _(u"Bullets list\tCtrl+G"), 
                _(u"Bullets list (<ul>…</ul>)"), 
                os.path.join (self.imagesDir, "text_list_bullets.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_NUMBER_LIST", 
                lambda event: self.codeEditor.turnList (u'<ol>\n', u'</ol>', u'<li>', u'</li>'), 
                _(u"Numbers list\tCtrl+J"), 
                _(u"Numbers list (<ul>…</ul>)"), 
                os.path.join (self.imagesDir, "text_list_numbers.png"),
                fullUpdate=False)
    

    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        self.addTool (self.__htmlMenu, 
                "ID_H1", 
                lambda event: self.codeEditor.turnText (u"<h1>", u"</h1>"), 
                _(u"H1\tCtrl+1"), 
                _(u"H1 (<h1>…</h1>)"), 
                os.path.join (self.imagesDir, "text_heading_1.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_H2", 
                lambda event: self.codeEditor.turnText (u"<h2>", u"</h2>"), 
                _(u"H2\tCtrl+2"), 
                _(u"H2 (<h2>…</h2>)"), 
                os.path.join (self.imagesDir, "text_heading_2.png"),
                fullUpdate=False)
        
        self.addTool (self.__htmlMenu, 
                "ID_H3", 
                lambda event: self.codeEditor.turnText (u"<h3>", u"</h3>"), 
                _(u"H3\tCtrl+3"), 
                _(u"H3 (<h3>…</h3>)"), 
                os.path.join (self.imagesDir, "text_heading_3.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_H4", 
                lambda event: self.codeEditor.turnText (u"<h4>", u"</h4>"), 
                _(u"H4\tCtrl+4"), 
                _(u"H4 (<h4>…</h4>)"), 
                os.path.join (self.imagesDir, "text_heading_4.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_H5", 
                lambda event: self.codeEditor.turnText (u"<h5>", u"</h5>"), 
                _(u"H5\tCtrl+5"), 
                _(u"H5 (<h5>…</h5>)"), 
                os.path.join (self.imagesDir, "text_heading_5.png"),
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_H6", 
                lambda event: self.codeEditor.turnText (u"<h6>", u"</h6>"), 
                _(u"H6\tCtrl+6"), 
                _(u"H6 (<h6>…</h6>)"), 
                os.path.join (self.imagesDir, "text_heading_6.png"),
                fullUpdate=False)
    

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
                fullUpdate=False)

        self.addTool (self.__htmlMenu, 
                "ID_LINK", 
                lambda event: self.codeEditor.turnText (u'<a href="">', u'</a>'), 
                _(u"Link\tCtrl+L"), 
                _(u'Link (<a href="…">…</a>)'), 
                os.path.join (self.imagesDir, "link.png"),
                fullUpdate=False)


        self.addTool (self.__htmlMenu, 
                "ID_ANCHOR", 
                lambda event: self.codeEditor.turnText (u'<a name="', u'"></a>'), 
                _(u"Anchor\tCtrl+Alt+L"), 
                _(u'Anchor (<a name="…">…</a>)'), 
                os.path.join (self.imagesDir, "anchor.png"),
                fullUpdate=False)


        self.addTool (self.__htmlMenu, 
                "ID_HORLINE", 
                lambda event: self.codeEditor.replaceText (u'<hr>'), 
                _(u"Horizontal line\tCtrl+H"), 
                _(u"Horizontal line (<hr>)"), 
                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                fullUpdate=False)


        self.addTool (self.__htmlMenu, 
                "ID_CODE", 
                lambda event: self.codeEditor.turnText (u"<code>", u"</code>"), 
                _(u"Code\tCtrl+Alt+D"), 
                _(u"Code (<code>…</code>)"), 
                os.path.join (self.imagesDir, "code.png"),
                fullUpdate=False)


        self.addTool (self.__htmlMenu, 
                "ID_PREFORMAT", 
                lambda event: self.codeEditor.turnText (u"<pre>", u"</pre>"), 
                _(u"Preformat\tCtrl+Alt+F"), 
                _(u"Preformat (<pre>…</pre>)"), 
                None,
                fullUpdate=False)


        self.addTool (self.__htmlMenu, 
                "ID_BLOCKQUOTE", 
                lambda event: self.codeEditor.turnText (u"<blockquote>", u"</blockquote>"), 
                _(u"Quote\tCtrl+Alt+Q"), 
                _(u"Quote (<blockquote>…</blockquote>)"), 
                os.path.join (self.imagesDir, "quote.png"),
                fullUpdate=False)


        self.__htmlMenu.AppendSeparator()

        self.addTool (self.__htmlMenu, 
                "ID_ESCAPEHTML", 
                self.codeEditor.escapeHtml, 
                _(u"Convert HTML Symbols"), 
                _(u"Convert HTML Symbols"), 
                None,
                fullUpdate=False)


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
        BaseTextPanel.removeGui (self)
        self.mainWindow.mainMenu.Remove (self.__HTML_MENU_INDEX - 1)
