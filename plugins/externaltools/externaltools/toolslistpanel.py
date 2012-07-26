#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import os.path

import wx

from outwiker.core.system import getOS

from .scrolledpanel import ScrolledPanel


class ToolsListPanel (ScrolledPanel):
    """
    Окно со списком всех добавленных инструментов
    """
    def __init__ (self, parent):
        super (ToolsListPanel, self).__init__ (parent, style=wx.BORDER_THEME)
        
        # Список инструментов (экземпляры класса ToolsInfo)
        self._tools = []

        # Интерфейсные элементы для инструментов (экземпляры класса ToolsItemCtrl)
        self._toolsGuiElements = []

        self._mainSizer = wx.FlexGridSizer (rows=0, cols=1)
        self._mainSizer.AddGrowableCol (0)
        self.SetSizer (self._mainSizer)
        self.SetAutoLayout(1)


    @property
    def tools (self):
        return self._tools


    @tools.setter
    def tools (self, newtools):
        self._tools = newtools[:]
        self.__updateGui()


    def __updateGui (self):
        self._mainSizer.Clear (True)
        self._toolsGuiElements = []

        for toolsItem in self._tools:
            self.addTool (toolsItem)

        # self.SetupScrolling()
        # self.Layout()


    def addTool (self, toolsItem=None):
        """
        Добавить новый элемент для инструмента
        toolsItem - экземпляр класса ToolsInfo или None, если нужно создать новый инструмент
        """
        toolGuiElement = ToolsItemCtrl (self, toolsItem)
        self._toolsGuiElements.append (toolGuiElement)
        self._mainSizer.Add (toolGuiElement, 1, wx.EXPAND | wx.ALL, border=2)

        self.SetupScrolling(scrollToTop=False)
        self.ScrollChildIntoView (toolGuiElement)
        # toolGuiElement.SetFocus()



class ToolsItemCtrl (wx.Panel):
    """
    Контрол для выбора одного инструмента
    """
    def __init__ (self, parent, toolItem):
        """
        parent - родительское окно
        toolItem - экземпляр класса ToolsInfo
        """
        super (ToolsItemCtrl, self).__init__ (parent, style=wx.BORDER_THEME | wx.TAB_TRAVERSAL)

        self._BROWSE_ID = wx.NewId()
        self._REMOVE_ID = wx.NewId()

        self._toolItem = toolItem

        if self._toolItem == None:
            self._pathTextCtrl = wx.TextCtrl (self, -1, u"")
        else:
            self._pathTextCtrl = wx.TextCtrl (self, -1, toolItem.command)

        browseBitmap = wx.Bitmap (self.__getImagePath ("browse.png"))
        self._browseButton = wx.BitmapButton (self, 
                self._BROWSE_ID, 
                browseBitmap)

        removeBitmap = wx.Bitmap (self.__getImagePath ("cross.png"))
        self.removeButton = wx.BitmapButton (self, 
                self._REMOVE_ID, 
                removeBitmap)

        self._browseButton.Bind(wx.EVT_BUTTON, self.__onBrowse)

        self.__layout()


    def __onBrowse (self, event):
        if os.name == "nt":
            wildcard = _(u"Executables (*.exe)|*.exe|All Files|*.*")
        else:
            wildcard = _(u"All Files|*.*")

        dlg = wx.FileDialog (self,
                wildcard=wildcard,
                style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self._pathTextCtrl.Value = dlg.Path

        dlg.Destroy()


    def __getImagePath (self, fname):
        return unicode (os.path.join (os.path.dirname (__file__), "images", fname),
                getOS().filesEncoding)


    def __layout (self):
        sizer = wx.FlexGridSizer (1, 3)
        sizer.AddGrowableCol (0)
        sizer.Add (self._pathTextCtrl, 1, wx.EXPAND | wx.ALL, border=2)
        sizer.Add (self._browseButton, 1, wx.RIGHT | wx.TOP | wx.BOTTOM, border=2)
        sizer.Add (self.removeButton, 1, wx.ALL, border=2)

        self.SetSizer (sizer)
        self.Layout()


    @property
    def toolsPath (self):
        return self._pathTextCtrl.Value


    @property
    def toolItem (self):
        command = self._pathTextCtrl.Value.strip()
        title = os.path.basename (command)

        if self._toolItem == None:
            return ToolsInfo (command, title, wx.NewId())
        else:
            return ToolsInfo (command, title, self._toolItem.toolsid)
