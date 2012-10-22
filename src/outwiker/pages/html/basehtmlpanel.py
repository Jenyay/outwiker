#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from abc import ABCMeta, abstractmethod, abstractproperty

import wx

from outwiker.core.application import Application
from outwiker.core.commands import MessageBox, setStatusText
from outwiker.core.system import getTemplatesDir, getImagesDir
from outwiker.core.attachment import Attachment
from outwiker.gui.basetextpanel import BaseTextPanel
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.htmlrenderfactory import getHtmlRender


class BaseHtmlPanel(BaseTextPanel):
    __metaclass__ = ABCMeta
    
    def __init__(self, parent, *args, **kwds):
        super (BaseHtmlPanel, self).__init__ (parent, *args, **kwds)

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
            fullUpdate=True,
            panelname="plugins"):
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
        super (BaseHtmlPanel, self).addTool (menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled,
            fullUpdate,
            panelname)
        
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
            fullUpdate=True,
            panelname="plugins"):
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
        super (BaseHtmlPanel, self).addCheckTool (menu, 
            idstring, 
            func, 
            menuText, 
            buttonText, 
            image, 
            alwaysEnabled,
            fullUpdate,
            panelname)

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
        
        status_item = 0

        setStatusText (_(u"Page rendered. Please wait…"), status_item)
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

        setStatusText (u"", status_item)
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
        self.mainWindow.UpdateAuiManager()
        
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
                _(u"Code / Preview") + "\tF4", 
                _(u"Code / Preview"), 
                os.path.join (self.imagesDir, "render.png"),
                True,
                False,
                panelname=self.mainWindow.GENERAL_TOOLBAR_STR)

        self.toolsMenu.AppendSeparator()


    def __switchView (self, event):
        if self._currentpage == None:
            return

        if self.notebook.GetSelection() == self.CODE_PAGE_INDEX:
            self.notebook.SetSelection (self.RESULT_PAGE_INDEX)
        else:
            self.notebook.SetSelection (self.CODE_PAGE_INDEX)

