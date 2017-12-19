# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.core.tagslist import TagsList
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.tagscommands import(parseTagsList,
                                       appendTag,
                                       removeTag,
                                       tagBranch,
                                       appendTagsList,
                                       removeTagsFromBranch,
                                       renameTag)

from .utils import removeDir


class TagsListTest(unittest.TestCase):
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "page 1", ["Метка 1", "Метка 2"])
        factory.create(self.wikiroot, "Страница 2", ["Метка 1", "Метка 3"])
        factory.create(self.wikiroot["Страница 2"],
                       "Страница 3",
                       ["Метка 2"])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       ["Метка 1"])
        factory.create(self.wikiroot["page 1"], "page 5", ["Метка 4"])

    def tearDown(self):
        removeDir(self.path)

    def test1(self):
        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags), 4)

        self.assertEqual(len(tags["Метка 1"]), 3)
        self.assertIn(self.wikiroot["page 1"], tags["Метка 1"])
        self.assertIn(self.wikiroot["Страница 2"], tags["Метка 1"])
        self.assertIn(self.wikiroot["Страница 2/Страница 3/Страница 4"],
                      tags["Метка 1"])

    def testParseTags(self):
        tagsString = " метка 1 , Метка 2, метка 3,, , "

        tags = parseTagsList(tagsString)

        self.assertEqual(len(tags), 3)

        self.assertIn("метка 1", tags)
        self.assertIn("Метка 2", tags)
        self.assertIn("метка 3", tags)

    def testAppendTag(self):
        appendTag(self.wikiroot["Страница 2"], "Метка 666")

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 3)
        self.assertIn("Метка 666".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 1".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 3".lower(), self.wikiroot["Страница 2"].tags)

    def testAppendTagsList(self):
        appendTagsList(self.wikiroot["Страница 2"],
                       ["Метка 111", "Метка 222", "Метка 333"])

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 5)
        self.assertIn("Метка 111".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 222".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 333".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 1".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 3".lower(), self.wikiroot["Страница 2"].tags)

    def testCopyTags(self):
        self.assertEqual(len(self.wikiroot["page 1"].tags), 2)

        appendTag(self.wikiroot["page 1"], "Метка 1")

        self.assertEqual(len(self.wikiroot["page 1"].tags), 2)

    def testTagBranch(self):
        tagBranch(self.wikiroot["Страница 2"], ["Метка 111", "Метка 222"])

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 4)
        self.assertEqual(len(self.wikiroot["Страница 2/Страница 3"].tags), 3)
        self.assertEqual(
            len(self.wikiroot["Страница 2/Страница 3/Страница 4"].tags), 3)

        self.assertIn("Метка 111".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 111".lower(),
                      self.wikiroot["Страница 2/Страница 3"].tags)
        self.assertIn("Метка 111".lower(),
                      self.wikiroot["Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn("Метка 222".lower(),
                      self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 222".lower(),
                      self.wikiroot["Страница 2/Страница 3"].tags)
        self.assertIn("Метка 222".lower(),
                      self.wikiroot["Страница 2/Страница 3/Страница 4"].tags)

    def testTagRoot(self):
        tagBranch(self.wikiroot, ["Метка 111", "Метка 222"])

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 4)
        self.assertEqual(len(self.wikiroot["Страница 2/Страница 3"].tags), 3)
        self.assertEqual(
            len(self.wikiroot["Страница 2/Страница 3/Страница 4"].tags), 3)

        self.assertIn("Метка 111".lower(), self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 111".lower(),
                      self.wikiroot["Страница 2/Страница 3"].tags)
        self.assertIn("Метка 111".lower(),
                      self.wikiroot["Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn("Метка 222".lower(),
                      self.wikiroot["Страница 2"].tags)
        self.assertIn("Метка 222".lower(),
                      self.wikiroot["Страница 2/Страница 3"].tags)
        self.assertIn("Метка 222".lower(),
                      self.wikiroot["Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn("Метка 222".lower(), self.wikiroot["page 1"].tags)
        self.assertIn("Метка 222".lower(),
                      self.wikiroot["page 1/page 5"].tags)

    def testRemoveTag1(self):
        self.assertIn("Метка 3".lower(),
                      self.wikiroot["Страница 2"].tags)
        removeTag(self.wikiroot["Страница 2"], "Метка 3")
        self.assertNotIn("Метка 3".lower(),
                         self.wikiroot["Страница 2"].tags)

    def testRemoveTag2(self):
        self.assertIn("Метка 3".lower(),
                      self.wikiroot["Страница 2"].tags)
        removeTag(self.wikiroot["Страница 2"], "МеТкА 3")
        self.assertNotIn("Метка 3".lower(),
                         self.wikiroot["Страница 2"].tags)

    def testRemoveNotExists(self):
        self.assertNotIn("Метка 333".lower(),
                         self.wikiroot["Страница 2"].tags)
        removeTag(self.wikiroot["Страница 2"], "Метка 333")
        self.assertNotIn("Метка 333".lower(),
                         self.wikiroot["Страница 2"].tags)

    def testAppendExists(self):
        appendTag(self.wikiroot["Страница 2"], "Метка 1")
        self.assertIn("Метка 1".lower(),
                      self.wikiroot["Страница 2"].tags)

        removeTag(self.wikiroot["Страница 2"], "Метка 1")
        self.assertNotIn("Метка 1".lower(),
                         self.wikiroot["Страница 2"].tags)

    def testRemoveTagsFromBranch1(self):
        removeTagsFromBranch(self.wikiroot["Страница 2"], ["Метка 1"])

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 1)
        self.assertIn("метка 3", self.wikiroot["Страница 2"].tags)

        self.assertEqual(len(self.wikiroot["Страница 2/Страница 3"].tags), 1)
        self.assertIn("метка 2", self.wikiroot["Страница 2/Страница 3"].tags)

        self.assertEqual(
            len(self.wikiroot["Страница 2/Страница 3/Страница 4"].tags), 0)

    def testRemoveTagsFromRoot(self):
        removeTagsFromBranch(self.wikiroot, ["МеТкА 1"])

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 1)
        self.assertIn("метка 3", self.wikiroot["Страница 2"].tags)

        self.assertEqual(len(self.wikiroot["Страница 2/Страница 3"].tags), 1)
        self.assertIn("метка 2", self.wikiroot["Страница 2/Страница 3"].tags)

        self.assertEqual(
            len(self.wikiroot["Страница 2/Страница 3/Страница 4"].tags), 0)

    def testRemoveTagsFromBranch2(self):
        removeTagsFromBranch(self.wikiroot["Страница 2"],
                             ["МеТкА 1", "Метка 1000"])

        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 1)
        self.assertIn("метка 3", self.wikiroot["Страница 2"].tags)

        self.assertEqual(len(self.wikiroot["Страница 2/Страница 3"].tags), 1)
        self.assertIn("метка 2", self.wikiroot["Страница 2/Страница 3"].tags)

        self.assertEqual(
            len(self.wikiroot["Страница 2/Страница 3/Страница 4"].tags), 0)

    def testRemoveTagsEmpty(self):
        removeTagsFromBranch(self.wikiroot, [])

        self.assertEqual(len(self.wikiroot["page 1"].tags), 2)
        self.assertEqual(len(self.wikiroot["page 1/page 5"].tags), 1)
        self.assertEqual(len(self.wikiroot["Страница 2"].tags), 2)
        self.assertEqual(len(self.wikiroot["Страница 2/Страница 3"].tags), 1)
        self.assertEqual(
            len(self.wikiroot["Страница 2/Страница 3/Страница 4"].tags), 1)

    def testRenameTag(self):
        renameTag(self.wikiroot, "МеТкА 1", "Черная метка")

        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags), 4)

        self.assertEqual(len(tags["Метка 1"]), 0)
        self.assertEqual(len(tags["Черная метка"]), 3)

        self.assertIn(self.wikiroot["page 1"], tags["Черная метка"])
        self.assertIn(self.wikiroot["Страница 2"], tags["Черная метка"])
        self.assertIn(self.wikiroot["Страница 2/Страница 3/Страница 4"],
                      tags["Черная метка"])

    def testRenameTagBranch(self):
        renameTag(self.wikiroot["Страница 2"], "МеТкА 1", "Черная метка")

        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags["Метка 1"]), 1)
        self.assertEqual(len(tags["Черная метка"]), 2)

        self.assertIn(self.wikiroot["page 1"], tags["Метка 1"])
        self.assertIn(self.wikiroot["Страница 2"], tags["Черная метка"])
        self.assertIn(self.wikiroot["Страница 2/Страница 3/Страница 4"],
                      tags["Черная метка"])

    def testRenameNotExists(self):
        renameTag(self.wikiroot, "МеТкА 666", "Черная метка")

        tags = TagsList(self.wikiroot)

        self.assertEqual(len(tags["Метка 1"]), 3)
        self.assertEqual(len(tags["Метка 666"]), 0)

        self.assertIn(self.wikiroot["page 1"], tags["Метка 1"])
        self.assertIn(self.wikiroot["Страница 2"], tags["Метка 1"])
        self.assertIn(self.wikiroot["Страница 2/Страница 3/Страница 4"],
                      tags["Метка 1"])
