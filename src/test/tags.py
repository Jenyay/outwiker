#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tagslist import TagsList

class TagsListTest (unittest.TestCase):
    def setUp(self):
        pass


    def testEmpty (self):
        tagslist = TagsList()
        self.assertEqual (len (tagslist), 0)


    def testAppend (self):
        tagslist = TagsList()
        tagslist.addTag (u"Тег 2", 1)
        self.assertEqual (len (tagslist), 1)

        tagslist.addTag (u"Тег 1", 10)
        self.assertEqual (len (tagslist), 2)

        self.assertEqual (tagslist[0][0], u"Тег 1")
        self.assertEqual (tagslist[1][0], u"Тег 2")

        for taginfo in tagslist:
            self.assertTrue (taginfo[0] == u"Тег 2" or taginfo[0] == u"Тег 1")


    def testMaxCount (self):
        tagslist = TagsList()
        self.assertEqual (tagslist.getMaxCount(), 0)

        tagslist.addTag (u"Тег 2", 1)
        self.assertEqual (tagslist.getMaxCount(), 1)

        tagslist.addTag (u"Тег 1", 10)
        self.assertEqual (tagslist.getMaxCount(), 10)
