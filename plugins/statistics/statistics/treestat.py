#!/usr/bin/python
# -*- coding: UTF-8 -*-

from outwiker.core.tree import WikiDocument


class TreeStat (object):
    """
    Класс для сбора статистики по дереву
    """
    def __init__ (self, root):
        """
        root - страница, которая считается корневой
        """
        self._root = root


    @property
    def pageCount (self):
        """
        Возвращает количество страниц в дереве
        """
        startcount = 0 if self._root.getTypeString() == WikiDocument.getTypeString() else 1
        return self._getChildCount (self._root) + startcount


    def _getChildCount (self, root):
        count = len (root)

        for child in root.children:
            count += self._getChildCount (child)

        return count
