#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from .localsearchpanel import LocalSearcher


class SearchPanelController (object):
    _recentSearch = u""

    def __init__ (self, searchPanel, editor):
        """
        searchPanel - панель со строкой поиска
        editor - текстовый редактор (экземпляр класса textEditor)
        """
        # Панель со строкой поиска
        self.panel = searchPanel
        self.editor = editor

        self.panel.phraseTextCtrl.SetValue (SearchPanelController._recentSearch)


    def nextSearch (self):
        """
        Искать следующее вхождение фразы
        """
        self._searchTo (self._findNext)


    def prevSearch (self):
        """
        Искать предыдущее вхождение фразы
        """
        self._searchTo (self._findPrev)
        self.editor.SetFocus()
    

    def startSearch (self):
        """
        Начать поиск
        """
        phrase = self.editor.GetSelectedText()

        if len (phrase) == 0:
            phrase = SearchPanelController._recentSearch
            self.panel.phraseTextCtrl.SetValue (phrase)

        self.panel.phraseTextCtrl.SetValue (phrase)
        self.panel.phraseTextCtrl.SetSelection (-1, -1)
        self.panel.phraseTextCtrl.SetFocus ()


    def enterSearchPhrase (self):
        self._searchTo (self._findNextOnEnter)


    def show (self):
        if not self.panel.IsShown():
            self.panel.Show()
            self.panel.GetParent().Layout()
    

    def _searchTo (self, direction):
        """
        Поиск фразы в нужном направлении (вперед / назад)
        direction - функция, которая ищет текст в нужном направлении (_findNext / _findPrev)
        """
        self.panel.phraseTextCtrl.SetFocus ()
        phrase = self.panel.phraseTextCtrl.GetValue ()

        SearchPanelController._recentSearch = phrase

        if len (phrase) == 0:
            return

        text = self.editor.GetText()
        result = direction (text, phrase)
        if result != None:
            self.panel.resultLabel.SetLabel (u"")
            self.editor.SetSelection (result.position, result.position + len (result.phrase) )
        else:
            self.panel.resultLabel.SetLabel (_(u"Not found"))

        self.panel.Layout()

    
    def _findNext (self, text, phrase):
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


    def _findPrev (self, text, phrase):
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


    def _findNextOnEnter (self, text, phrase):
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
