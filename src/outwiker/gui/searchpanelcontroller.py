#!/usr/bin/env python
# -*- coding: UTF-8 -*-

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

        self._searcher = LocalSearcher()

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


    def replace (self):
        """
        Сделать замену
        Возвращает True, если удалось сделать замену
        """
        phrase = self.getSearchPhrase()
        searchResult = SearchResult (self.editor.GetSelectionStart(), 
                self.editor.GetSelectedText())

        if (len (phrase) > 0 and self._searcher.inResult (searchResult) ):
            self.editor.replaceText (self.getReplacePhrase())
            self.nextSearch()
            return True

        return False


    def replaceAll (self):
        """
        Заменить все
        """
        self.nextSearch()
        while (self.replace()):
            pass
    

    def startSearch (self):
        """
        Начать поиск
        """
        phrase = self.editor.GetSelectedText()

        if len (phrase) == 0:
            phrase = SearchPanelController._recentSearch
            self.panel.phraseTextCtrl.SetValue (phrase)

        self.setSearchPhrase (phrase)
        self.panel.phraseTextCtrl.SetSelection (-1, -1)
        self.panel.phraseTextCtrl.SetFocus ()


    def enterSearchPhrase (self):
        self._searchTo (self._findNextOnEnter)


    def show (self):
        if not self.panel.IsShown():
            self.panel.Show()
            self.panel.GetParent().Layout()


    def setSearchPhrase (self, phrase):
        """
        В панели поиска установить искомую фразу. При этом сразу начинается поиск
        """
        self.panel.phraseTextCtrl.SetValue (phrase)


    def getSearchPhrase (self):
        """
        Возвращает искомую фразу из панели
        """
        return self.panel.phraseTextCtrl.GetValue()


    def setReplacePhrase (self, phrase):
        self.panel.replaceTextCtrl.SetValue (phrase)


    def getReplacePhrase (self):
        return self.panel.replaceTextCtrl.GetValue()


    def switchToSearchMode (self):
        """
        Переключиться в режим поиска
        """
        self.panel.Close()
        self.panel.setReplaceGuiVisible (False)
        self.show()


    def switchToReplaceMode (self):
        """
        Переключиться в режим поиска
        """
        self.panel.Close()
        # Если редактор находится в режиме "только для чтения", 
        # то не показывать GUI предназначенный для замены
        self.panel.setReplaceGuiVisible (not self.editor.GetReadOnly())
        self.show()
    

    def _searchTo (self, direction):
        """
        Поиск фразы в нужном направлении (вперед / назад)
        direction - функция, которая ищет текст в нужном направлении (_findNext / _findPrev)
        """
        self.panel.phraseTextCtrl.SetFocus ()
        phrase = self.getSearchPhrase ()

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
        self._searcher.search (text, phrase)

        currpos = self.editor.GetCurrentPosition()

        result = None

        for currResult in self._searcher.result:
            if currResult.position >= currpos:
                result = currResult
                break

        if result == None and len (self._searcher.result) > 0:
            result = self._searcher.result[0]

        return result


    def _findPrev (self, text, phrase):
        """
        Найти предыдущее вхождение
        """
        self._searcher.search (text, phrase)

        currpos = self.editor.GetSelectionStart()

        result = None

        for currResult in self._searcher.result:
            if currResult.position < currpos:
                result = currResult

        if result == None and len (self._searcher.result) > 0:
            result = self._searcher.result[-1]

        return result


    def _findNextOnEnter (self, text, phrase):
        """
        Найти следующее вхождение, но начиная с начала выделения текста
        """
        self._searcher.search (text, phrase)

        currpos = self.editor.GetSelectionStart()

        result = None

        for currResult in self._searcher.result:
            if currResult.position >= currpos:
                result = currResult
                break

        if result == None and len (self._searcher.result) > 0:
            result = self._searcher.result[0]

        return result



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
    """
    Класс для поиска по странице
    """
    def __init__ (self):
        self._result = []


    @property
    def result (self):
        return self._result


    def search (self, text, phrase):
        self._result = []

        text_lower = text.lower()
        phrase_lower = phrase.lower()

        index = text_lower.find (phrase_lower)

        while index != -1:
            self._result.append (SearchResult (index, phrase_lower) )
            index = text_lower.find (phrase_lower, index + len (phrase_lower))


    def inResult (self, testResult):
        """
        testResult - экземпляр класса SearchResult
        Функция возвращает True, если в self._result есть результат поиска, соответствующий testResult

        Эта функция используется для того, чтобы проверять выделенный в редакторе фрагмент на соответствие поисковой фразе
        """
        for resultItem in self._result:
            if (testResult.position == resultItem.position and
                    testResult.phrase.lower() == resultItem.phrase.lower()):
                return True

        return False
