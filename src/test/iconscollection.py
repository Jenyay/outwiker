# -*- coding: UTF-8 -*-

import os
import unittest

from outwiker.core.iconscollection import IconsCollection, DuplicateGroupError
from test.utils import removeDir


class IconsCollectionTest (unittest.TestCase):
    def setUp (self):
        self.tempDir1 = u"../test/testIcons1"
        self.tempDir2 = u"../test/testIcons2"
        self.imagesDir = u"../test/images"


    def tearDown (self):
        removeDir (self.tempDir1)
        removeDir (self.tempDir2)


    def testEmpty_01 (self):
        collection = IconsCollection ([u"../test/icons/Без иконок"])

        self.assertEqual (collection.getAll(), [])
        self.assertEqual (collection.getIcons(""), [])
        self.assertEqual (collection.getGroups(), [])
        self.assertRaises (KeyError, collection.getIcons, u"Группа")
        self.assertRaises (KeyError, collection.getGroupCover, u"Группа")
        self.assertIsNone (collection.getRootCover())


    def testEmpty_02 (self):
        collection = IconsCollection ([u"../test/icons/Без иконок"])

        self.assertEqual (collection.getAll(), [])
        self.assertEqual (collection.getIcons(None), [])
        self.assertEqual (collection.getGroups(), [])
        self.assertRaises (KeyError, collection.getIcons, u"Группа")
        self.assertRaises (KeyError, collection.getGroupCover, u"Группа")
        self.assertIsNone (collection.getRootCover())


    def testSingleRoot (self):
        collection = IconsCollection ([u"../test/icons/Без групп"])

        self.assertEqual (len (collection.getIcons(None)), 4)
        self.assertEqual (len (collection.getAll()), 4)
        self.assertEqual (collection.getGroups(), [])
        self.assertTrue (collection.getRootCover().endswith (u"__cover.png"))


    def testSingleRoot_clone (self):
        collection = IconsCollection ([u"../test/icons/Без групп", u"../test/icons/Без групп"])

        self.assertEqual (len (collection.getIcons(u"")), 8)
        self.assertEqual (len (collection.getAll()), 8)
        self.assertEqual (collection.getGroups(), [])
        self.assertTrue (collection.getRootCover().endswith (u"__cover.png"))


    def testGroups_01 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы"])

        self.assertEqual (len (collection.getIcons(None)), 4)
        self.assertEqual (len (collection.getAll()), 11)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertTrue (collection.getRootCover().endswith (u"gy.png"))
        self.assertTrue (collection.getGroupCover(u"Группа 1").endswith (u"__cover.png"))
        self.assertTrue (collection.getGroupCover(u"Группа 2").endswith (u"tg.png"))


    def testGroups_02 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы", u"../test/icons/Иконки и группы"])

        self.assertEqual (len (collection.getIcons(u"")), 8)
        self.assertEqual (len (collection.getAll()), 22)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 6)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 8)
        self.assertTrue (collection.getRootCover().endswith (u"gy.png"))


    def testGroups_03 (self):
        collection = IconsCollection ([u"../test/icons/Только группы"])

        self.assertEqual (len (collection.getIcons(None)), 0)
        self.assertEqual (len (collection.getAll()), 7)
        self.assertEqual (collection.getGroups(), [u"Группа 3", u"Группа 4"])
        self.assertEqual (len (collection.getIcons (u"Группа 3")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 4")), 4)
        self.assertIsNone (collection.getRootCover())


    def testGroups_04 (self):
        collection = IconsCollection ([u"../test/icons/Без групп", u"../test/icons/Иконки и группы"])

        self.assertEqual (len (collection.getIcons(u"")), 8)
        self.assertEqual (len (collection.getAll()), 15)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertTrue (collection.getRootCover().endswith (u"__cover.png"))


    def testGroups_05 (self):
        collection = IconsCollection ([u"../test/icons/Без групп", u"../test/icons/Только группы"])

        self.assertEqual (len (collection.getIcons(u"")), 4)
        self.assertEqual (len (collection.getAll()), 11)
        self.assertEqual (collection.getGroups(), [u"Группа 3", u"Группа 4"])
        self.assertEqual (len (collection.getIcons (u"Группа 3")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 4")), 4)
        self.assertIsNotNone (collection.getRootCover())


    def testGroups_06 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы", u"../test/icons/Только группы"])

        self.assertEqual (len (collection.getIcons(None)), 4)
        self.assertEqual (len (collection.getAll()), 18)
        self.assertEqual (collection.getGroups(), [u"Группа 1", u"Группа 2", u"Группа 3", u"Группа 4"])
        self.assertEqual (len (collection.getIcons (u"Группа 1")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 2")), 4)
        self.assertEqual (len (collection.getIcons (u"Группа 3")), 3)
        self.assertEqual (len (collection.getIcons (u"Группа 4")), 4)
        self.assertTrue (collection.getRootCover().endswith (u"gy.png"))


    def testGroups_07 (self):
        collection = IconsCollection ([u"../test/icons/Иконки и группы", u"../test/icons/Без групп"])

        self.assertEqual (len (collection.getIcons(None)), 8)
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


    def testRemoveGroup_01 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Другая группа", 1)

        collection.removeGroup (u"Новая группа", 0)
        self.assertEqual (collection.getGroups(), [u"Другая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [])
        self.assertEqual (newcollection2.getGroups(), [u"Другая группа"])


    def testRemoveGroup_02 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Другая группа", 1)

        collection.removeGroup (u"Другая группа", -1)
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [u"Новая группа"])
        self.assertEqual (newcollection2.getGroups(), [])


    def testRemoveGroup_03 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Другая группа", 1)

        collection.removeGroup (u"Другая группа")
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [u"Новая группа"])
        self.assertEqual (newcollection2.getGroups(), [])


    def testRemoveGroup_04 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Новая группа", 1)

        collection.removeGroup (u"Новая группа")
        self.assertEqual (collection.getGroups(), [u"Новая группа"])

        newcollection1 = IconsCollection ([self.tempDir1])
        newcollection2 = IconsCollection ([self.tempDir2])
        self.assertEqual (newcollection1.getGroups(), [u"Новая группа"])
        self.assertEqual (newcollection2.getGroups(), [])


    def testRemoveGroup_05 (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа")

        collection.removeGroup (u"Новая группа")
        self.assertEqual (collection.getGroups(), [])


    def testRemoveGroup_06_invalid (self):
        os.mkdir (self.tempDir1)
        os.mkdir (self.tempDir2)

        collection = IconsCollection ([self.tempDir1, self.tempDir2])
        collection.addGroup (u"Новая группа", 0)
        collection.addGroup (u"Другая группа", 1)

        self.assertRaises (
            KeyError,
            collection.removeGroup,
            u"Абырвалг")

        self.assertRaises (
            KeyError,
            collection.removeGroup,
            u"Новая группа",
            1)

        self.assertRaises (
            KeyError,
            collection.removeGroup,
            u"")


    def testAddIcons_01_empty (self):
        files = []
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (u"Новая группа", 0)

        collection.addIcons (u"Новая группа", fullPaths)
        self.assertEqual (collection.getIcons (u"Новая группа"), [])


    def testAddIcons_02_empty (self):
        files = []
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (u"Новая группа", 0)

        collection.addIcons (u"Новая группа", fullPaths, 0)
        self.assertEqual (collection.getIcons (u"Новая группа"), [])


    def testAddIcons_03_empty (self):
        files = []
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        collection.addIcons (u"", fullPaths, 0)
        self.assertEqual (collection.getIcons (None), [])


    def testAddIcons_04_invalid (self):
        files = [u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        self.assertRaises (
            KeyError,
            collection.addIcons,
            u"Другая группа",
            fullPaths,
            0)


    def testAddIcons_05 (self):
        files = [u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        collection.addIcons (u"", fullPaths, 0)

        icons = collection.getIcons (None)
        self.assertIn (u"new.png", icons[0])


    def testAddIcons_06 (self):
        files = [u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        collection.addIcons (None, fullPaths, 0)

        icons = collection.getIcons (None)
        self.assertIn (u"new.png", icons[0])


    def testAddIcons_07 (self):
        files = [u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        collection.addIcons (None, fullPaths, -1)

        icons = collection.getIcons (None)
        self.assertIn (u"new.png", icons[0])


    def testAddIcons_08 (self):
        files = [u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        collection.addIcons (None, fullPaths)

        icons = collection.getIcons (None)
        self.assertIn (u"new.png", icons[0])


    def testAddIcons_09 (self):
        files = [u"new.png", u"image_01.JPG"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])

        collection.addIcons (None, fullPaths)

        icons = sorted (collection.getIcons (None))
        self.assertIn (u"image_01.png", icons[0])
        self.assertIn (u"new.png", icons[1])


    def testAddIcons_10 (self):
        files = [u"new.png", u"image_01.JPG"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 2)
        self.assertIn (u"image_01.png", icons[0])
        self.assertIn (u"new.png", icons[1])


    def testAddIcons_11 (self):
        files = [u"new.png", u"image_01.JPG", u"__init__.py"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 2)
        self.assertIn (u"image_01.png", icons[0])
        self.assertIn (u"new.png", icons[1])


    def testAddIcons_12_not_exists (self):
        files = [u"new.png", u"image_01.JPG", u"notexists.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 2)
        self.assertIn (u"image_01.png", icons[0])
        self.assertIn (u"new.png", icons[1])


    def testAddIcons_13 (self):
        files = [u"new.png", u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 2)
        self.assertIn (u"new.png", icons[0])
        self.assertIn (u"new_(1).png", icons[1])


    def testAddIcons_14 (self):
        files = [u"new.png", u"new.png", u"new.png", u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 4)
        self.assertIn (u"new.png", icons[0])
        self.assertIn (u"new_(1).png", icons[1])
        self.assertIn (u"new_(2).png", icons[2])
        self.assertIn (u"new_(3).png", icons[3])


    def testAddIcons_15 (self):
        files = [u"__sample.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 1)
        self.assertNotIn (u"__sample.png", icons[0])
        self.assertIn (u"sample.png", icons[0])


    def testAddIcons_16 (self):
        files = [u"______sample.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 1)
        self.assertNotIn (u"______sample.png", icons[0])
        self.assertNotIn (u"__sample.png", icons[0])
        self.assertIn (u"sample.png", icons[0])


    def testAddIcons_17 (self):
        files = [u"______sample.png", "__sample.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 2)
        self.assertNotIn (u"__sample.png", icons[0])
        self.assertIn (u"sample.png", icons[0])
        self.assertIn (u"sample_(1).png", icons[1])


    def testAddIcons_18_invalid (self):
        files = [u"invalid.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 0)


    def testAddIcons_19_invalid (self):
        files = [u"invalid.png", u"new.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 1)
        self.assertIn (u"new.png", icons[0])


    def testAddIcons_20_invalid (self):
        files = [u"new.png", u"invalid.png"]
        fullPaths = [os.path.join (self.imagesDir, fname) for fname in files]

        groupname = u"Новая группа"

        os.mkdir (self.tempDir1)
        collection = IconsCollection ([self.tempDir1])
        collection.addGroup (groupname)

        collection.addIcons (groupname, fullPaths)

        icons = sorted (collection.getIcons (groupname))
        self.assertEqual (len (icons), 1)
        self.assertIn (u"new.png", icons[0])
