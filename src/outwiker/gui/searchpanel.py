# -*- coding: utf-8 -*-

import codecs
import os.path

import wx
from outwiker.core.system import getImagesDir

class SearchPanel (wx.Panel):
    def __init__(self, parent):
        super (SearchPanel, self).__init__(parent)

        self._controller = None

        self._createGui()
        self._bindEvents()

        # Список элементов, относящихся к замене
        self._replaceGui = [self._replaceLabel,
                self._replaceText,
                self._replaceBtn,
                self._replaceAllBtn,
                ]


    def setController (self, controller):
        self._controller = controller


    @property
    def phraseTextCtrl (self):
        return self._searchText


    @property
    def resultLabel (self):
        return self._resultLabel


    def setReplaceGuiVisible (self, visible):
        """
        Установить, нужно ли показывать элементы GUI для замены
        """
        for item in self._replaceGui:
            item.Show (visible)

        self.Layout()


    def _bindEvents (self):
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.__onCloseClick, self._searchText)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.__onNextSearch, self._searchText)
        self.Bind(wx.EVT_TEXT_ENTER, self.__onNextSearch, self._searchText)
        self.Bind(wx.EVT_TEXT, self.__onTextEnter, self._searchText)
        self.Bind(wx.EVT_BUTTON, self.__onNextSearch, self._nextSearchBtn)
        self.Bind(wx.EVT_BUTTON, self.__onPrevSearch, self._prevSearchBtn)
        self.Bind (wx.EVT_CLOSE, self.__onClose)
        self._searchText.Bind (wx.EVT_KEY_UP, self.__onKeyDown)

        self._replaceText.Bind (wx.EVT_KEY_UP, self.__onKeyDown)
        self.Bind(wx.EVT_BUTTON, self.__onReplace, self._replaceBtn)
        self.Bind(wx.EVT_BUTTON, self.__onReplaceAll, self._replaceAllBtn)


    def _createGui (self):
        self._mainSizer = wx.FlexGridSizer (cols=5)
        self._mainSizer.AddGrowableCol(1)
        self._mainSizer.AddGrowableRow(0)
        self._mainSizer.AddGrowableRow(1)

        # Элементы интерфейса, связанные с поиском
        self._findLabel = wx.StaticText(self, -1, _(u"Find what: "))

        # Поле для ввода искомой фразы
        self._searchText = wx.SearchCtrl (self, -1, u"", style=wx.TE_PROCESS_ENTER)
        self._searchText.ShowCancelButton(True)
        self._searchText.SetDescriptiveText (_(u"Search"))
        self._searchText.SetMinSize((250, -1))

        # Кнопка "Найти далее"
        self._nextSearchBtn = wx.Button (self, -1, _(u"Next"))

        # Кнопка "Найти выше"
        self._prevSearchBtn = wx.Button (self, -1, _(u"Prev"))

        # Метка с результатом поиска 
        self._resultLabel = wx.StaticText(self, -1, "")
        self._resultLabel.SetMinSize ((150, -1))


        # Элементы интерфейса, связанные с заменой
        self._replaceLabel = wx.StaticText(self, -1, _(u"Replace with: "))

        # Текст для замены
        self._replaceText = wx.TextCtrl (self, -1, u"")
        self._replaceText.SetMinSize((250, -1))

        # Кнопка "Заменить"
        self._replaceBtn = wx.Button (self, -1, _(u"Replace"))

        # Кнопка "Заменить все"
        self._replaceAllBtn = wx.Button (self, -1, _(u"Replace All"))

        self._layout()


    def _layout(self):
        # Элементы интерфейса для поиска
        self._mainSizer.Add (self._findLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._searchText, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._nextSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._prevSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._resultLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)

        # Элементы интерфейса для замены
        self._mainSizer.Add (self._replaceLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._replaceText, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._replaceBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.Add (self._replaceAllBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self._mainSizer.AddStretchSpacer()
        
        self.SetSizer (self._mainSizer)
        self.Layout()
    

    def __onNextSearch(self, event): 
        if self._controller != None:
            self._controller.nextSearch()

    
    def __onPrevSearch(self, event):
        if self._controller != None:
            self._controller.prevSearch()


    def __onReplace (self, event):
        if self._controller != None:
            self._controller.replace()


    def __onReplaceAll (self, event):
        if self._controller != None:
            self._controller.replaceAll()

    
    def __onTextEnter(self, event):
        if self._controller != None:
            self._controller.enterSearchPhrase()
    

    def __onClose(self, event):
        self.Hide()
        self.GetParent().Layout()
    

    def __onKeyDown (self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self.Close()

        event.Skip()


    def __onCloseClick(self, event):
        self.Close()
