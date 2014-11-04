# -*- coding: UTF-8 -*-

import os
import unittest

from outwiker.core.iconscollection import IconsCollection, DuplicateGroupError
from test.utils import removeDir


class IconsCollectionTest (unittest.TestCase):
    def setUp (self):
        self.tempDir1 = u"../test/testIcons1"
        self.tempDir2 = u"../test/testIcons2"


    def tearDown (self):
        removeDir (self.tempDir1)
        removeDir (self.tempDir2)


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


    def testAddGroup_01 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа")
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])

        self.assertEqual (newcollection1.getGroups(), [])
        self.assertEqual (newcollection2.getGroups(), [u"Новая группа"])


    def testAddGroup_02 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа", -1)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])

        self.assertEqual (newcollection1.getGroups(), [])
        self.assertEqual (newcollection2.getGroups(), [u"Новая группа"])


    def testAddGroup_03 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа", 1)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])

        self.assertEqual (newcollection1.getGroups(), [])
        self.assertEqual (newcollection2.getGroups(), [u"Новая группа"])


    def testAddGroup_04 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])

        self.assertEqual (newcollection1.getGroups(), [u"Новая группа"])
        self.assertEqual (newcollection2.getGroups(), [])


    def testAddGroup_05_invalid (self):
        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        self.assertRaises (ValueError, collection.addGroup, u"Абырвалг\\Абырвалг")
        self.assertRaises (ValueError, collection.addGroup, u"Абырвалг/Абырвалг")
        self.assertRaises (ValueError, collection.addGroup, u"")


    def testAddGroup_06 (self):
        os.mkdir (self.tempDir1)

        collection = IconsCollection ([self.tempDir1])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection = IconsCollection ([self.tempDir1])
        self.assertEqual (newcollection.getGroups(), [u"Новая группа"])


    def testAddGroup_07 (self):
        os.mkdir (self.tempDir1)

        collection = IconsCollection ([self.tempDir1])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Новая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection = IconsCollection ([self.tempDir1])
        self.assertEqual (newcollection.getGroups(), [u"Новая группа"])


    def testAddGroup_08 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (collection.getGroups(), [])

        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Новая группа", 1)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])

        self.assertEqual (newcollection1.getGroups(), [u"Новая группа"])
        self.assertEqual (newcollection2.getGroups(), [u"Новая группа"])


    def testRenameGroup_01 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", -1)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        collection.renameGroup (u"Новая группа", u"Переименованная группа")
        self.assertEqual (collection.getGroups(), [u"Переименованная группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [])
        self.assertEqual (newcollection2.getGroups(), [u"Переименованная группа"])


    def testRenameGroup_02 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", -1)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        collection.renameGroup (u"Новая группа", u"Переименованная группа", -1)
        self.assertEqual (collection.getGroups(), [u"Переименованная группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [])
        self.assertEqual (newcollection2.getGroups(), [u"Переименованная группа"])


    def testRenameGroup_03 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        collection.renameGroup (u"Новая группа", u"Переименованная группа", 0)
        self.assertEqual (collection.getGroups(), [u"Переименованная группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [u"Переименованная группа"])
        self.assertEqual (newcollection2.getGroups(), [])


    def testRenameGroup_04_invalid (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)

        self.assertRaises (
            ValueError,
            collection.renameGroup,
            u"Новая группа",
            u"",
            0)

        self.assertRaises (
            ValueError,
            collection.renameGroup,
            u"Новая группа",
            u"Абырвалг/Абырвалг",
            0)

        self.assertRaises (
            ValueError,
            collection.renameGroup,
            u"Новая группа",
            u"Абырвалг\\Абырвалг",
            0)


    def testRenameGroup_05_invalid (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)

        self.assertRaises (
            KeyError,
            collection.renameGroup,
            u"Новая группа",
            u"Абырвалг",
            1)

        self.assertRaises (
            KeyError,
            collection.renameGroup,
            u"Абырвалг",
            u"123",
            0)


    def testRenameGroup_06_self (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)

        collection.renameGroup (u"Новая группа", u"Новая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (newcollection.getGroups(), [u"Новая группа"])


    def testRenameGroup_07_invalid (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Абырвалг", 0)

        self.assertRaises (
            DuplicateGroupError,
            collection.renameGroup,
            u"Новая группа",
            u"Абырвалг",
            0)


    def testRenameGroup_08 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Другая группа", 1)

        collection.renameGroup (u"Новая группа", u"Другая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Другая группа"])

        newcollection = IconsCollection ([self.tempDir1, self.tempDir2])
        self.assertEqual (newcollection.getGroups(), [u"Другая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [u"Другая группа"])
        self.assertEqual (newcollection2.getGroups(), [u"Другая группа"])