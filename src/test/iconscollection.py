# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.iconscollection import IconsCollection


class IconsCollectionTest (unittest.TestCase):
    def testEmpty (self):
        collection = IconsCollection ([u"../test/icons/Без иконок"])

        self.assertEqual (collection.getAll(), [])
        self.assertEqual (collection.getRoot(), [])
        self.assertEqual (collection.getGroups(), [])
        self.assertRaises (KeyError, collection.getIcons, u"Группа")
        self.assertRaises (KeyError, collection.getGroupCover, u"Группа")
        self.assertIsNone (collection.getRootCover())


    def testSingleRoot (self):
        collection = IconsCollection ([u"../test/icons/Без групп"])

        self.assertEqual (len (collection.getRoot()), 4)
        self.assertEqual (len (collection.getAll()), 4)
        self.assertEqual (collection.getGroups(), [])
        self.assertTrue (collection.getRootCover().endswith (u"__cover.png"))


    def testSingleRoot_clone (self):
        collection = IconsCollection ([u"../test/icons/Без групп", u"../test/icons/Без групп"])

        self.assertEqual (len (collection.getRoot()), 8)
        self.assertEqual (len (collection.getAll()), 8)
        self.assertEqual (collection.getGroups(), [])
        self.assertTrue (collection.getRootCover().endswith (u"__cover.png"))


    def testGroups_01 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы"])

        self.assertEqual (len (collection.getRoot()), 4)
        self.assertEqual (len (collection.getAll()), 11)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertTrue (collection.getRootCover().endswith (u"gy.png"))
        self.assertTrue (collection.getGroupCover(u"Группа 1").endswith (u"__cover.png"))
        self.assertTrue (collection.getGroupCover(u"Группа 2").endswith (u"tg.png"))


    def testGroups_02 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы", u"../test/icons/Иконки и группы"])

        self.assertEqual (len (collection.getRoot()), 8)
        self.assertEqual (len (collection.getAll()), 22)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 6)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 8)
        self.assertTrue (collection.getRootCover().endswith (u"gy.png"))


    def testGroups_03 (self):
        collection = IconsCollection ([u"../test/icons/Только группы"])

        self.assertEqual (len (collection.getRoot()), 0)
        self.assertEqual (len (collection.getAll()), 7)
        self.assertEqual (collection.getGroups(), [u"Группа 3", u"Группа 4"])
        self.assertEqual (len (collection.getIcons (u"Группа 3")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 4")), 4)
        self.assertIsNone (collection.getRootCover())


    def testGroups_04 (self):
        collection = IconsCollection ([u"../test/icons/Без групп", u"../test/icons/Иконки и группы"])

        self.assertEqual (len (collection.getRoot()), 8)
        self.assertEqual (len (collection.getAll()), 15)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertTrue (collection.getRootCover().endswith (u"__cover.png"))


    def testGroups_05 (self):
        collection = IconsCollection ([u"../test/icons/Без групп", u"../test/icons/Только группы"])

        self.assertEqual (len (collection.getRoot()), 4)
        self.assertEqual (len (collection.getAll()), 11)
        self.assertEqual (collection.getGroups(), [u"Группа 3", u"Группа 4"])
        self.assertEqual (len (collection.getIcons (u"Группа 3")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 4")), 4)
        self.assertIsNotNone (collection.getRootCover())


    def testGroups_06 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы", u"../test/icons/Только группы"])

        self.assertEqual (len (collection.getRoot()), 4)
        self.assertEqual (len (collection.getAll()), 18)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2", u"Группа 3", u"Группа 4"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertEqual (len (collection.getIcons (u"Группа 3")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 4")), 4)
        self.assertTrue (collection.getRootCover().endswith (u"gy.png"))


    def testGroups_07 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы", u"../test/icons/Без групп"])

        self.assertEqual (len (collection.getRoot()), 8)
        self.assertEqual (len (collection.getAll()), 15)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertIsNotNone (collection.getRootCover())
