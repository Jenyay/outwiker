# -*- coding: UTF-8 -*-
"""
Классы для работы с историей открытия страниц
"""

class HistoryEmptyException (Exception):
    """
    Вызывается при попытке вернуться назад, если история возврата пустая (и аналогично с историей вперед)
    """
    pass


class History (object):
    """
    Класс для работы с историей открытия страниц на вкладке
    """
    def __init__ (self):
        # Список страниц для возврата (для перехода "назад")
        self._back = []

        # Список страниц для перехода "вперед"
        self._forward = []

        # Текущая открытая страница
        self._currentPage = None


    @property
    def backLength (self):
        return len (self._back)


    @property
    def forwardLength (self):
        return len (self._forward)


    def goto (self, newCurrentPage):
        """
        Произошел переход на новую страницу
        """
        if (self._currentPage == None and
                len (self._back) == 0 and
                len (self._forward) == 0 ):
            # В первый раз открыли какую-то страницу
            self._currentPage = newCurrentPage
            return

        if self._currentPage == newCurrentPage:
            # Если повторно открываем ту же самую страницу, то ничего не делаем
            return

        self._back.append (self._currentPage)
        self._forward = []

        self._currentPage = newCurrentPage


    def back (self):
        if self.backLength == 0:
            raise HistoryEmptyException()

        self._forward.append (self._currentPage)
        self._currentPage = self._back.pop()

        if self._currentPage != None and self._currentPage.isRemoved:
            self._currentPage = None

        return self._currentPage


    def forward (self):
        if self.forwardLength == 0:
            raise HistoryEmptyException()

        self._back.append (self._currentPage)
        self._currentPage = self._forward.pop()

        if self._currentPage != None and self._currentPage.isRemoved:
            self._currentPage = None

        return self._currentPage


    @property
    def currentPage (self):
        return self._currentPage


    def clear (self):
        self._back = []
        self._forward = []
        self._currentPage = None
