# -*- coding: utf-8 -*-

import codecs
import os.path

import wx
from outwiker.core.system import getImagesDir

class LocalSearchPanel (wx.Panel):
    def __init__(self, parent):
        super (LocalSearchPanel, self).__init__(parent)

        self._controller = None

        self._createGui()
        self._bindEvents()


    def setController (self, controller):
        self._controller = controller


    @property
    def phraseTextCtrl (self):
        return self._phraseTextCtrl


    @property
    def resultLabel (self):
        return self._resultLabel


    def _bindEvents (self):
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.__onCloseClick, self._phraseTextCtrl)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.__onNextSearch, self._phraseTextCtrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.__onNextSearch, self._phraseTextCtrl)
        self.Bind(wx.EVT_TEXT, self.__onTextEnter, self._phraseTextCtrl)
        self.Bind(wx.EVT_BUTTON, self.__onNextSearch, self.nextSearchBtn)
        self.Bind(wx.EVT_BUTTON, self.__onPrevSearch, self.prevSearchBtn)
        self.Bind (wx.EVT_CLOSE, self.__onClose)
        self._phraseTextCtrl.Bind (wx.EVT_KEY_DOWN, self.__onKeyDown)


    def _createGui (self):
        imagesDir = getImagesDir()

        self._phraseTextCtrl = wx.SearchCtrl (self, -1, "", style=wx.TE_PROCESS_ENTER)
        self._phraseTextCtrl.ShowCancelButton(True)
        self._phraseTextCtrl.SetDescriptiveText (_(u"Search"))
        self._phraseTextCtrl.SetMinSize((250, -1))

        self.nextSearchBtn = wx.BitmapButton(self, 
                -1, 
                wx.Bitmap(os.path.join (imagesDir, "arrow_down.png"), 
                    wx.BITMAP_TYPE_ANY))

        self.nextSearchBtn.SetToolTipString (_(u"Find Next") )
        self.nextSearchBtn.SetSize(self.nextSearchBtn.GetBestSize())

        self.prevSearchBtn = wx.BitmapButton(self, 
                -1, 
                wx.Bitmap(os.path.join (imagesDir, "arrow_up.png"), 
                    wx.BITMAP_TYPE_ANY))

        self.prevSearchBtn.SetToolTipString (_(u"Find Previous") )
        self.prevSearchBtn.SetSize(self.prevSearchBtn.GetBestSize())

        self._resultLabel = wx.StaticText(self, -1, "")
        self._resultLabel.SetMinSize ((150, -1))

        self._layout()


    def _layout(self):
        mainSizer = wx.FlexGridSizer(1, 0, 0, 0)
        mainSizer.Add(self._phraseTextCtrl, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self.nextSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self.prevSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self._resultLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)
    

    def __onNextSearch(self, event): 
        if self._controller != None:
            self._controller.nextSearch()

    
    def __onPrevSearch(self, event):
        if self._controller != None:
            self._controller.prevSearch()

    
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



class SearchResult (object):
    """
    Результат поиска по странице
    """
    def __init__ (self, position, phrase):
        """
        position - начало найденного текста
        """
        self.position = position
        self.phrase = phrase


class LocalSearcher (object):
    def __init__ (self, text, phrase):
        self.text = text.lower()
        self.phrase = phrase.lower()
        self.result = self._findAll ()


    def _findAll (self):
        result = []
        index = self.text.find (self.phrase)

        while index != -1:
            result.append (SearchResult (index, self.phrase) )
            index = self.text.find (self.phrase, index + len (self.phrase))

        return result

