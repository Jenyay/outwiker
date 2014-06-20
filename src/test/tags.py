# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.tagscommands import parseTagsList, appendTag, removeTag, tagBranch, appendTagsList, removeTagsFromBranch, renameTag

from .utils import removeWiki


class TagsListTest (unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.rootwiki, u"page 1", [u"Метка 1", u"Метка 2"])
        factory.create (self.rootwiki, u"Страница 2", [u"Метка 1", u"Метка 3"])
        factory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [u"Метка 2"])
        factory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [u"Метка 1"])
        factory.create (self.rootwiki[u"page 1"], u"page 5", [u"Метка 4"])


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

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 3)
        self.assertTrue (u"Метка 666".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 1".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 3".lower() in self.rootwiki[u"Страница 2"].tags)


    def testAppendTagsList (self):
        appendTagsList (self.rootwiki[u"Страница 2"], [u"Метка 111", u"Метка 222", u"Метка 333"])

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 5)
        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 333".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 1".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 3".lower() in self.rootwiki[u"Страница 2"].tags)


    def testCopyTags (self):
        self.assertEqual (len (self.rootwiki[u"page 1"].tags), 2)

        appendTag (self.rootwiki[u"page 1"], u"Метка 1")

        self.assertEqual (len (self.rootwiki[u"page 1"].tags), 2)


    def testTagBranch (self):
        tagBranch (self.rootwiki[u"Страница 2"], [u"Метка 111", u"Метка 222"])

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 4)
        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3"].tags), 3)
        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags), 3)

        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2/Страница 3"].tags)
        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags)

        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2/Страница 3"].tags)
        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags)


    def testTagRoot (self):
        tagBranch (self.rootwiki, [u"Метка 111", u"Метка 222"])

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 4)
        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3"].tags), 3)
        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags), 3)

        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2/Страница 3"].tags)
        self.assertTrue (u"Метка 111".lower() in self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags)

        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2"].tags)
        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2/Страница 3"].tags)
        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags)

        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"page 1"].tags)
        self.assertTrue (u"Метка 222".lower() in self.rootwiki[u"page 1/page 5"].tags)


    def testRemoveTag1 (self):
        self.assertTrue (u"Метка 3".lower() in self.rootwiki[u"Страница 2"].tags)
        removeTag (self.rootwiki[u"Страница 2"], u"Метка 3")
        self.assertTrue (u"Метка 3".lower() not in self.rootwiki[u"Страница 2"].tags)


    def testRemoveTag2 (self):
        self.assertTrue (u"Метка 3".lower() in self.rootwiki[u"Страница 2"].tags)
        removeTag (self.rootwiki[u"Страница 2"], u"МеТкА 3")
        self.assertTrue (u"Метка 3".lower() not in self.rootwiki[u"Страница 2"].tags)


    def testRemoveNotExists (self):
        self.assertTrue (u"Метка 333".lower() not in self.rootwiki[u"Страница 2"].tags)
        removeTag (self.rootwiki[u"Страница 2"], u"Метка 333")
        self.assertTrue (u"Метка 333".lower() not in self.rootwiki[u"Страница 2"].tags)


    def testAppendExists (self):
        appendTag (self.rootwiki[u"Страница 2"], u"Метка 1")
        self.assertTrue (u"Метка 1".lower() in self.rootwiki[u"Страница 2"].tags)

        removeTag (self.rootwiki[u"Страница 2"], u"Метка 1")
        self.assertTrue (u"Метка 1".lower() not in self.rootwiki[u"Страница 2"].tags)


    def testRemoveTagsFromBranch1 (self):
        removeTagsFromBranch (self.rootwiki[u"Страница 2"], [u"Метка 1"])

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 1)
        self.assertTrue (u"метка 3" in self.rootwiki[u"Страница 2"].tags)

        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3"].tags), 1)
        self.assertTrue (u"метка 2" in self.rootwiki[u"Страница 2/Страница 3"].tags)

        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags), 0)


    def testRemoveTagsFromRoot (self):
        removeTagsFromBranch (self.rootwiki, [u"МеТкА 1"])

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 1)
        self.assertTrue (u"метка 3" in self.rootwiki[u"Страница 2"].tags)

        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3"].tags), 1)
        self.assertTrue (u"метка 2" in self.rootwiki[u"Страница 2/Страница 3"].tags)

        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags), 0)


    def testRemoveTagsFromBranch2 (self):
        removeTagsFromBranch (self.rootwiki[u"Страница 2"], [u"МеТкА 1", u"Метка 1000"])

        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 1)
        self.assertTrue (u"метка 3" in self.rootwiki[u"Страница 2"].tags)

        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3"].tags), 1)
        self.assertTrue (u"метка 2" in self.rootwiki[u"Страница 2/Страница 3"].tags)

        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags), 0)


    def testRemoveTagsEmpty (self):
        removeTagsFromBranch (self.rootwiki, [])

        self.assertEqual (len (self.rootwiki[u"page 1"].tags), 2)
        self.assertEqual (len (self.rootwiki[u"page 1/page 5"].tags), 1)
        self.assertEqual (len (self.rootwiki[u"Страница 2"].tags), 2)
        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3"].tags), 1)
        self.assertEqual (len (self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags), 1)



    def testRenameTag (self):
        renameTag (self.rootwiki, u"МеТкА 1", u"Черная метка")

        tags = TagsList (self.rootwiki)

        self.assertEqual (len (tags), 4)

        self.assertEqual (len (tags[u"Метка 1"]), 0)
        self.assertEqual (len (tags[u"Черная метка"]), 3)

        self.assertTrue (self.rootwiki[u"page 1"] in tags[u"Черная метка"])
        self.assertTrue (self.rootwiki[u"Страница 2"] in tags[u"Черная метка"])
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in tags[u"Черная метка"])


    def testRenameTagBranch (self):
        renameTag (self.rootwiki[u"Страница 2"], u"МеТкА 1", u"Черная метка")

        tags = TagsList (self.rootwiki)

        self.assertEqual (len (tags[u"Метка 1"]), 1)
        self.assertEqual (len (tags[u"Черная метка"]), 2)

        self.assertTrue (self.rootwiki[u"page 1"] in tags[u"Метка 1"])
        self.assertTrue (self.rootwiki[u"Страница 2"] in tags[u"Черная метка"])
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in tags[u"Черная метка"])


    def testRenameNotExists (self):
        renameTag (self.rootwiki, u"МеТкА 666", u"Черная метка")

        tags = TagsList (self.rootwiki)

        self.assertEqual (len (tags[u"Метка 1"]), 3)
        self.assertEqual (len (tags[u"Метка 666"]), 0)

        self.assertTrue (self.rootwiki[u"page 1"] in tags[u"Метка 1"])
        self.assertTrue (self.rootwiki[u"Страница 2"] in tags[u"Метка 1"])
        self.assertTrue (self.rootwiki[u"Страница 2/Страница 3/Страница 4"] in tags[u"Метка 1"])
