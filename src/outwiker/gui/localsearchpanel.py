# -*- coding: utf-8 -*-

import codecs
import os.path

import wx
from outwiker.core.system import getImagesDir

class LocalSearchPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        self.imagesDir = getImagesDir()

        kwds["style"] = wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.phraseTextCtrl = wx.SearchCtrl (self, -1, "", style=wx.TE_PROCESS_ENTER)
        self.phraseTextCtrl.ShowCancelButton(True)
        self.nextSearchBtn = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join (self.imagesDir, "arrow_down.png"), wx.BITMAP_TYPE_ANY))
        self.prevSearchBtn = wx.BitmapButton(self, -1, wx.Bitmap(os.path.join (self.imagesDir, "arrow_up.png"), wx.BITMAP_TYPE_ANY))
        self.resultLabel = wx.StaticText(self, -1, "")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.onCloseClick, self.phraseTextCtrl)
        self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.onNextSearch, self.phraseTextCtrl)
        self.Bind(wx.EVT_TEXT_ENTER, self.onNextSearch, self.phraseTextCtrl)
        self.Bind(wx.EVT_TEXT, self.onTextEnter, self.phraseTextCtrl)
        self.Bind(wx.EVT_BUTTON, self.onNextSearch, self.nextSearchBtn)
        self.Bind(wx.EVT_BUTTON, self.onPrevSearch, self.prevSearchBtn)

        self.nextSearchBtn.SetToolTipString (_(u"Find Next") )
        self.prevSearchBtn.SetToolTipString (_(u"Find Previous") )

        self.Bind (wx.EVT_CLOSE, self.onClose)
        self.phraseTextCtrl.Bind (wx.EVT_KEY_DOWN, self.onKeyDown)


    def __set_properties(self):
        self.phraseTextCtrl.SetMinSize((250, -1))
        self.nextSearchBtn.SetSize(self.nextSearchBtn.GetBestSize())
        self.prevSearchBtn.SetSize(self.prevSearchBtn.GetBestSize())

    def __do_layout(self):
        mainSizer = wx.FlexGridSizer(1, 0, 0, 0)
        mainSizer.Add(self.phraseTextCtrl, 0, wx.ALL|wx.EXPAND|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self.nextSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self.prevSearchBtn, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        mainSizer.Add(self.resultLabel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)
        mainSizer.AddGrowableRow(0)
        mainSizer.AddGrowableCol(0)
    

    def onNextSearch(self, event): 
        self.nextSearch()

    
    def onPrevSearch(self, event):
        self.prevSearch()

    
    def onTextEnter(self, event):
        self.enterSearchPhrase()

    
    def nextSearch (self):
        """
        Искать следующее вхождение фразы
        """
        pass


    def prevSearch (self):
        """
        Искать предыдущее вхождение фразы
        """
        pass
    

    def startSearch (self):
        """
        Начать поиск
        """
        pass
    

    def enterSearchPhrase (self):
        pass
    

    def onClose(self, event):
        self.Hide()
        self.GetParent().Layout()
    

    def onKeyDown (self, event):
        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:
            self.Close()

        event.Skip()


    def onCloseClick(self, event):
        self.Close()



class SearchResult (object):
    """
    Результат поиска по странице
    """
    def __init__ (self, position, phrase):
        """
        position -- начало найденного текста
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
            #print index

        return result

