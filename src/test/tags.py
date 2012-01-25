#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.tagscommands import parseTagsList, appendTag, removeTag

from .utils import removeWiki


class TagsListTest (unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        TextPageFactory.create (self.rootwiki, u"page 1", [u"Метка 1", u"Метка 2"])
        TextPageFactory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
        TextPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
        TextPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
        TextPageFactory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 4"])

    
    def test1 (self):
        tags = TagsList (self.rootwiki)

        self.assertEqual (len (tags), 4)

        self.assertEqual (len (tags[u"Метка 1"]), 3)
        self.assertTrue (self.rootwiki[u"page 1"] in tags[u"Метка 1"])
        self.assertTrue (self.rootwiki[u"Страница 2"] in tags[u"Метка 1"])
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in tags[u"Метка 1"])
    

    def testParseTags (self):
        tagsString = u" метка 1 , Метка 2, метка 3,, , "

        tags = parseTagsList (tagsString)

        self.assertEqual (len (tags), 3)

        self.assertTrue (u"метка 1" in tags)
        self.assertTrue (u"Метка 2" in tags)
        self.assertTrue (u"метка 3" in tags)


    def testAppendTag (self):
        appendTag (self.rootwiki[u"Страница 2"], u"Метка 666")
        self.assertTrue (u"Метка 666" in self.rootwiki[u"Страница 2"].tags)


    def testRemoveTag (self):
        self.assertTrue (u"Метка 3" in self.rootwiki[u"Страница 2"].tags)
        removeTag (self.rootwiki[u"Страница 2"], u"Метка 3")
        self.assertTrue (u"Метка 3" not in self.rootwiki[u"Страница 2"].tags)


    def testRemoveNotExists (self):
        self.assertTrue (u"Метка 333" not in self.rootwiki[u"Страница 2"].tags)
        removeTag (self.rootwiki[u"Страница 2"], u"Метка 333")
        self.assertTrue (u"Метка 333" not in self.rootwiki[u"Страница 2"].tags)


    def testAppendExists (self):
        appendTag (self.rootwiki[u"Страница 2"], u"Метка 1")
        self.assertTrue (u"Метка 1" in self.rootwiki[u"Страница 2"].tags)

        removeTag (self.rootwiki[u"Страница 2"], u"Метка 1")
        self.assertTrue (u"Метка 1" not in self.rootwiki[u"Страница 2"].tags)
