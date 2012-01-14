#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Классы для глобального поиска по вики
"""
import os.path

from outwiker.core.attachment import Attachment


class AllTagsSearchStrategy (object):
    """
    Стратегия проверки тегов, когда все теги должны быть найдены
    """
    @staticmethod
    def testTags (tags, page):
        result = True

        page_tags = [tag.lower() for tag in page.tags]

        for tag in tags:
            if tag not in page_tags:
                result = False
                break

        return result


class AnyTagSearchStrategy (object):
    """
    Стратегия проверки тегов, когда достаточно найти один гет
    """
    @staticmethod
    def testTags (tags, page):
        if len (tags) == 0:
            return True

        result = False

        page_tags = [tag.lower() for tag in page.tags]

        for tag in tags:
            if tag in page_tags:
                result = True
                break

        return result


class Searcher (object):
    def __init__ (self, phrase, tags, tagsStrategy):
        """
        phrase -- строка поиска (неразобранная)
        tags -- список тегов, по которым ищем страницы
        tagsStrategy -- стратегия поиска по тегам
        """
        self.phrase = phrase
        self.tags = [tag.lower() for tag in tags]
        self.tagsStrategy = tagsStrategy
    

    def find (self, root):
        """
        Найти подходящие по условию поиска страницы
        """
        result = []

        for page in root.children:
            if (self.tagsStrategy.testTags (self.tags, page) and 
                    self.__testFullContent(page) ):
                result.append (page)

            result += self.find (page)

        return result


    def __testFullContent (self, page):
        """
        Поиск искомого текста в разных частях заметки (содержимом, заголовке, тегах)
        """
        return (self.__testTitle (page) or 
                self.__testContent (page) or 
                self.__testTagsContent (page) or
                self.__testAttachment (page) )


    def __testTitle (self, page):
        title = page.title.lower()

        if len (self.phrase) == 0 or self.phrase.lower() in title:
            return True

        return False


    def __testContent (self, page):
        """
        Проверить, что искомая фраза встречается в контексте страницы.
        Также возвращает True, если контент пуст
        """
        content = page.textContent.lower()
        if len (self.phrase) == 0 or self.phrase.lower() in content:
            return True

        return False


    def __testTagsContent (self, page):
        """
        Проверить, встречается ли в тексте меток искомая фраза
        """
        lowerPhrase = self.phrase.lower()
        tags = filter (lambda tag: lowerPhrase in tag.lower(), page.tags)
        return len (tags) != 0


    def __testAttachment (self, page):
        attach = Attachment (page)
        if not os.path.exists (attach.getAttachPath()):
            return False

        lowerPhrase = self.phrase.lower()

        for root, subfolders, files in os.walk(attach.getAttachPath()):
            filterfiles = (filter (lambda fname: lowerPhrase in fname.lower(), files) )
            filterdirs = (filter (lambda dirname: lowerPhrase in dirname.lower(), 
                        subfolders))

            if (len (filterfiles) != 0 or len (filterdirs) != 0 ):
                return True

        return False
