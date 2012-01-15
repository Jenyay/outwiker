#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .tagscommands import parseTagsList


class TagsList (object):
    """
    Класс для хранения списка всех тегов в вики
    """
    def __init__ (self, root):
        self._root = root

        # Словарь тегов. Ключ - тег, значение - список страниц с этим тегом
        self._tags = {}

        self._findTags (root)


    @property
    def tags (self):
        return self._tags.keys()

    
    def _findTags (self, page):
        if page.parent != None:
            for tag in page.tags:
                tag_lower = tag.lower()

                if tag_lower in self._tags.keys():
                    self._tags[tag_lower].append (page)
                else:
                    self._tags[tag_lower] = [page]

        for child in page.children:
            self._findTags (child)
    

    def __len__ (self):
        return len (self._tags.keys())


    def __getitem__ (self, tag):
        return self._tags[tag.lower()]


    def __iter__ (self):
        tags = self._tags.keys()
        tags.sort()

        return iter (tags)
