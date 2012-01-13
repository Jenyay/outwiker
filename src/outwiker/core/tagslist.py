#!/usr/bin/python
# -*- coding: UTF-8 -*-

class TagsList (object):
    def __init__ (self):
        # Список, содержащий кортежи: метка, количество записей с такой меткой.
        self.__tags = []


    def __iter__ (self):
        return iter (self.__tags)


    def __len__ (self):
        return len (self.__tags)


    def __getitem__ (self, index):
        return self.__tags[index]


    def addTag (self, tagname, count):
        self.__tags.append ((tagname, count))
        self.__tags.sort (self.__compareTags)


    def getMaxCount (self):
        count = 0
        for tag in self.__tags:
            if tag[1] > count:
                count = tag[1]

        return count


    def __compareTags (self, tag1, tag2):
        """
        Функция для сравнения экземпляров класса Tag
        """
        name1 = tag1[0].lower()
        name2 = tag2[0].lower()

        if name1 < name2:
            return -1

        if name1 > name2:
            return 1

        return 0
