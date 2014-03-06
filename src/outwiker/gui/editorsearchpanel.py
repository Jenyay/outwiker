#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .localsearchpanel import LocalSearchPanel, LocalSearcher


class EditorSearchPanel (LocalSearchPanel):
    _recentSearch = u""

    def __init__ (self, parent, editor):
        super (EditorSearchPanel, self).__init__(parent)
    
        self.editor = editor
        self.phraseTextCtrl.SetValue (EditorSearchPanel._recentSearch)


    def nextSearch (self):
        """
        Искать следующее вхождение фразы
        """
        self.searchTo (self.findNext)


    def prevSearch (self):
        """
        Искать предыдущее вхождение фразы
        """
        self.searchTo (self.findPrev)
        self.editor.SetFocus()
    

    def startSearch (self):
        """
        Начать поиск
        """
        phrase = self.editor.GetSelectedText()

        if len (phrase) == 0:
            phrase = EditorSearchPanel._recentSearch
            self.phraseTextCtrl.SetValue (phrase)

        self.phraseTextCtrl.SetValue (phrase)
        self.phraseTextCtrl.SetSelection (-1, -1)
        self.phraseTextCtrl.SetFocus ()


    def enterSearchPhrase (self):
        self.searchTo (self.findNextOnEnter)
    

    def searchTo (self, direction):
        """
        Поиск фразы в нужном направлении (вперед / назад)
        direction - функция, которая ищет текст в нужном направлении (findNext / findPrev)
        """
        self.phraseTextCtrl.SetFocus ()
        phrase = self.phraseTextCtrl.GetValue ()

        EditorSearchPanel._recentSearch = phrase

        if len (phrase) == 0:
            return

        text = self.editor.GetText()
        result = direction (text, phrase)
        if result != None:
            self.resultLabel.SetLabel (u"")
            self.editor.SetSelection (result.position, result.position + len (result.phrase) )
        else:
            self.resultLabel.SetLabel (_(u"Not found"))

        self.Layout()

    
    def findNext (self, text, phrase):
        """
        Найти следующее вхождение
        """
        searcher = LocalSearcher (text, phrase)

        currpos = self.editor.GetCurrentPosition()

        result = None

        for currResult in searcher.result:
            if currResult.position >= currpos:
                result = currResult
                break

        if result == None and len (searcher.result) > 0:
            result = searcher.result[0]

        return result


    def findPrev (self, text, phrase):
        """
        Найти предыдущее вхождение
        """
        searcher = LocalSearcher (text, phrase)

        currpos = self.editor.GetSelectionStart()

        result = None

        for currResult in searcher.result:
            if currResult.position < currpos:
                result = currResult

        if result == None and len (searcher.result) > 0:
            result = searcher.result[-1]

        return result


    def findNextOnEnter (self, text, phrase):
        """
        Найти следующее вхождение, но начиная с начала выделения текста
        """
        searcher = LocalSearcher (text, phrase)

        currpos = self.editor.GetSelectionStart()

        result = None

        for currResult in searcher.result:
            if currResult.position >= currpos:
                result = currResult
                break

        if result == None and len (searcher.result) > 0:
            result = searcher.result[0]

        return result
