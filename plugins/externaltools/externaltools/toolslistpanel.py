# -*- coding: utf-8 -*-

import os
import os.path

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from .toolsinfo import ToolsInfo
from .i18n import get_


# Событие, вызываемое при удалении инструмента
RemoveToolEvent, EVT_REMOVE_TOOL = wx.lib.newevent.NewEvent()


class ToolsListPanel(ScrolledPanel):
    """
    Окно со списком всех добавленных инструментов
    """
    def __init__(self, parent):
        super(ToolsListPanel, self).__init__(parent)

        global _
        _ = get_()

        # Интерфейсные элементы для инструментов
        # (экземпляры класса ToolsItemCtrl)
        self._toolsGuiElements = []

        self._mainSizer = wx.FlexGridSizer(rows=0, cols=1, vgap=0, hgap=0)
        self._mainSizer.AddGrowableCol(0)
        self.SetSizer(self._mainSizer)
        self.SetupScrolling()

        self.Bind(EVT_REMOVE_TOOL, handler=self.__onRemoveTools)

    @property
    def tools(self):
        return [toolGuiElement.toolItem for
                toolGuiElement in self._toolsGuiElements
                if len(toolGuiElement.toolItem.command.strip()) != 0]

    @tools.setter
    def tools(self, newtools):
        self.__updateGui(newtools)

    def __onRemoveTools(self, event):
        assert event.EventObject in self._toolsGuiElements

        self._toolsGuiElements.remove(event.EventObject)
        self._mainSizer.Detach(event.EventObject)
        event.EventObject.Destroy()

        self.SetupScrolling(scrollToTop=False)

    def __updateGui(self, newtools):
        self._mainSizer.Clear(True)
        self._toolsGuiElements = []

        for toolsItem in newtools:
            self.addTool(toolsItem)

        self.Layout()
        self.SetupScrolling()

    def addTool(self, toolsItem=None):
        """
        Добавить новый элемент для инструмента
        toolsItem - экземпляр класса ToolsInfo или None,
        если нужно создать новый инструмент
        """
        toolGuiElement = ToolsItemCtrl(self, toolsItem)
        self._toolsGuiElements.append(toolGuiElement)
        self._mainSizer.Add(toolGuiElement, 1, wx.EXPAND | wx.ALL, border=2)


class ToolsItemCtrl(wx.Panel):
    """
    Контрол для выбора одного инструмента
    """
    def __init__(self, parent, toolItem):
        """
        parent - родительское окно
        toolItem - экземпляр класса ToolsInfo
        """
        super(ToolsItemCtrl, self).__init__(
            parent,
            style=wx.BORDER_NONE | wx.TAB_TRAVERSAL)

        self._BROWSE_ID = wx.NewId()
        self._REMOVE_ID = wx.NewId()

        self._toolItem = toolItem

        if self._toolItem is None:
            self._pathTextCtrl = wx.TextCtrl(self, -1, u"")
        else:
            self._pathTextCtrl = wx.TextCtrl(self, -1, toolItem.command)

        browseBitmap = wx.Bitmap(self.__getImagePath("browse.png"))
        self._browseButton = wx.BitmapButton(self,
                                             self._BROWSE_ID,
                                             browseBitmap)
        self._browseButton.SetToolTip(_(u"Open file dialog..."))

        removeBitmap = wx.Bitmap(self.__getImagePath("cross.png"))
        self._removeButton = wx.BitmapButton(self,
                                             self._REMOVE_ID,
                                             removeBitmap)
        self._removeButton.SetToolTip(_(u"Remove tool"))

        self._browseButton.Bind(wx.EVT_BUTTON, self.__onBrowse)
        self._removeButton.Bind(wx.EVT_BUTTON, self.__onRemove)

        self.__layout()

    def __onBrowse(self, event):
        if os.name == "nt":
            wildcard = _(u"Executables (*.exe)|*.exe|All Files|*.*")
        else:
            wildcard = _(u"All Files|*")

        dlg = wx.FileDialog(self,
                            wildcard=wildcard,
                            style=wx.FD_OPEN)

        if dlg.ShowModal() == wx.ID_OK:
            self._pathTextCtrl.Value = dlg.Path

        dlg.Destroy()

    def __onRemove(self, event):
        removeEvent = RemoveToolEvent()
        removeEvent.SetEventObject(self)
        wx.PostEvent(self.GetParent(), removeEvent)

    def __getImagePath(self, fname):
        return os.path.join(os.path.dirname(__file__), "images", fname)

    def __layout(self):
        sizer = wx.FlexGridSizer(1, 3, 0, 0)
        sizer.AddGrowableCol(0)
        sizer.Add(self._pathTextCtrl, 1, wx.EXPAND | wx.ALL, border=2)
        sizer.Add(self._browseButton, 1, wx.RIGHT | wx.TOP | wx.BOTTOM,
                  border=2)
        sizer.Add(self._removeButton, 1, wx.ALL, border=2)

        self.SetSizer(sizer)
        self.Layout()

    @property
    def toolsPath(self):
        return self._pathTextCtrl.Value

    @property
    def toolItem(self):
        command = self._pathTextCtrl.Value.strip()
        title = os.path.basename(command)

        if self._toolItem is None:
            return ToolsInfo(command, title, wx.NewId())
        else:
            return ToolsInfo(command, title, self._toolItem.toolsid)
