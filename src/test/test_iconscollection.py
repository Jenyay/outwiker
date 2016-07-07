# -*- coding: UTF-8 -*-

import os
import unittest

from outwiker.core.iconscollection import IconsCollection, DuplicateGroupError
from test.utils import removeDir, getImageSize


class IconsCollectionTest(unittest.TestCase):
    def setUp(self):
        self.tempDir1 = u'../test/testIcons1'
        self.imagesDir = u'../test/images'


    def tearDown(self):
        removeDir(self.tempDir1)


    def testEmpty_01(self):
        collection = IconsCollection(u'../test/icons/Без иконок')

        self.assertEqual(collection.getIcons(''), [])
        self.assertEqual(collection.getGroups(), [])
        self.assertRaises(KeyError, collection.getIcons, u'Группа')
        self.assertRaises(KeyError, collection.getCover, u'Группа')
        self.assertIsNone(collection.getCover(None))


    def testEmpty_02(self):
        collection = IconsCollection(u'../test/icons/Без иконок')

        self.assertEqual(collection.getIcons(None), [])
        self.assertEqual(collection.getGroups(), [])
        self.assertRaises(KeyError, collection.getIcons, u'Группа')
        self.assertRaises(KeyError, collection.getCover, u'Группа')
        self.assertIsNone(collection.getCover(u''))


    def testSingleRoot(self):
        collection = IconsCollection(u'../test/icons/Без групп')

        self.assertEqual(len(collection.getIcons(None)), 4)
        self.assertEqual(collection.getGroups(), [])
        self.assertTrue(collection.getCover(None).endswith(u'__cover.png'))


    def testGroups_01(self):
        collection = IconsCollection(u'../test/icons/Иконки и группы')

        self.assertEqual(len(collection.getIcons(None)), 4)
        self.assertEqual(collection.getGroups(), [u'Группа 1', u'Группа 2'])
        self.assertEqual(len(collection.getIcons(u'Группа 1')), 3)
        self.assertEqual(len(collection.getIcons(u'Группа 2')), 4)
        self.assertIsNone(collection.getCover(None))
        self.assertTrue(
            collection.getCover(u'Группа 1').endswith(u'__cover.png'))
        self.assertIsNone(collection.getCover(u'Группа 2'))


    def testGroups_02(self):
        collection = IconsCollection(u'../test/icons/Только группы')

        self.assertEqual(len(collection.getIcons(None)), 0)
        self.assertEqual(collection.getGroups(), [u'Группа 3', u'Группа 4'])
        self.assertEqual(len(collection.getIcons(u'Группа 3')), 3)
        self.assertEqual(len(collection.getIcons(u'Группа 4')), 4)
        self.assertIsNone(collection.getCover(None))


    def testAddGroup_01(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        self.assertEqual(collection.getGroups(), [])

        collection.addGroup(u'Новая группа')
        self.assertEqual(collection.getGroups(), [u'Новая группа'])

        newcollection1 = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection1.getGroups(), [u'Новая группа'])


    def testAddGroup_02_invalid(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        self.assertRaises(ValueError,
                          collection.addGroup,
                          u'Абырвалг\\Абырвалг')
        self.assertRaises(ValueError,
                          collection.addGroup,
                          u'Абырвалг/Абырвалг')
        self.assertRaises(ValueError, collection.addGroup, u'')


    def testAddGroup_03(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        self.assertEqual(collection.getGroups(), [])

        collection.addGroup(u'Новая группа')
        collection.addGroup(u'Вторая группа')
        self.assertEqual(collection.getGroups(),
                         [u'Вторая группа', u'Новая группа'])

        newcollection = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection.getGroups(),
                         [u'Вторая группа', u'Новая группа'])


    def testRenameGroup_01(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')
        self.assertEqual(collection.getGroups(), [u'Новая группа'])

        collection.renameGroup(u'Новая группа', u'Переименованная группа')
        self.assertEqual(collection.getGroups(), [u'Переименованная группа'])

        newcollection1 = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection1.getGroups(),
                         [u'Переименованная группа'])


    def testRenameGroup_02_invalid(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')

        self.assertRaises(
            ValueError,
            collection.renameGroup,
            u'Новая группа',
            u'')

        self.assertRaises(
            ValueError,
            collection.renameGroup,
            u'Новая группа',
            u'Абырвалг/Абырвалг')

        self.assertRaises(
            ValueError,
            collection.renameGroup,
            u'Новая группа',
            u'Абырвалг\\Абырвалг')


    def testRenameGroup_03_self(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')

        collection.renameGroup(u'Новая группа', u'Новая группа')
        self.assertEqual(collection.getGroups(), [u'Новая группа'])

        newcollection = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection.getGroups(), [u'Новая группа'])


    def testRenameGroup_04_self(self):
        files = [u'new.png', u'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')
        collection.addIcons(u'Новая группа', fullPaths)

        collection.renameGroup(u'Новая группа', u'Новая группа')
        self.assertEqual(collection.getGroups(), [u'Новая группа'])
        self.assertEqual(len(collection.getIcons(u'Новая группа')), 2)

        newcollection = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection.getGroups(), [u'Новая группа'])
        self.assertEqual(len(newcollection.getIcons(u'Новая группа')), 2)


    def testRenameGroup_04_invalid(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')
        collection.addGroup(u'Абырвалг')

        self.assertRaises(
            DuplicateGroupError,
            collection.renameGroup,
            u'Новая группа',
            u'Абырвалг')


    def testRemoveGroup_01(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')
        collection.addGroup(u'Другая группа')

        collection.removeGroup(u'Новая группа')
        self.assertEqual(collection.getGroups(), [u'Другая группа'])

        newcollection1 = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection1.getGroups(), [u'Другая группа'])


    def testRemoveGroup_02(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')

        collection.removeGroup(u'Новая группа')
        self.assertEqual(collection.getGroups(), [])


    def testRemoveGroup_03_invalid(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')

        self.assertRaises(
            KeyError,
            collection.removeGroup,
            u'Абырвалг')

        self.assertRaises(
            KeyError,
            collection.removeGroup,
            u'')


    def testRemoveGroup_04(self):
        files = [u'new.png', u'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')
        collection.addIcons(u'Новая группа', fullPaths)

        collection.removeGroup(u'Новая группа')
        self.assertEqual(collection.getGroups(), [])


    def testAddIcons_01_empty(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')

        collection.addIcons(u'Новая группа', fullPaths)
        self.assertEqual(collection.getIcons(u'Новая группа'), [])


    def testAddIcons_02_empty(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(u'Новая группа')

        collection.addIcons(u'Новая группа', fullPaths)
        self.assertEqual(collection.getIcons(u'Новая группа'), [])


    def testAddIcons_03_empty(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons(u'', fullPaths)
        self.assertEqual(collection.getIcons(None), [])


    def testAddIcons_04_invalid(self):
        files = [u'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        self.assertRaises(
            KeyError,
            collection.addIcons,
            u'Другая группа',
            fullPaths)


    def testAddIcons_05(self):
        files = [u'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons(u'', fullPaths)

        icons = collection.getIcons(None)
        self.assertIn(u'new.png', icons[0])
        self.assertIsNone(collection.getCover(None))


    def testAddIcons_06(self):
        files = [u'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons(None, fullPaths)

        icons = collection.getIcons(None)
        self.assertIn(u'new.png', icons[0])


    def testAddIcons_07(self):
        files = [u'new.png', u'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons(None, fullPaths)

        icons = sorted(collection.getIcons(None))
        self.assertIn(u'image_01.png', icons[0])
        self.assertIn(u'new.png', icons[1])


    def testAddIcons_08(self):
        files = [u'new.png', u'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn(u'image_01.png', icons[0])
        self.assertIn(u'new.png', icons[1])
        self.assertIsNone(collection.getCover(u'Новая группа'))


    def testAddIcons_09(self):
        files = [u'new.png', u'image_01.JPG', u'__init__.py']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn(u'image_01.png', icons[0])
        self.assertIn(u'new.png', icons[1])


    def testAddIcons_10_not_exists(self):
        files = [u'new.png', u'image_01.JPG', u'notexists.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn(u'image_01.png', icons[0])
        self.assertIn(u'new.png', icons[1])


    def testAddIcons_11(self):
        files = [u'new.png', u'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn(u'new.png', icons[0])
        self.assertIn(u'new_(1).png', icons[1])


    def testAddIcons_12(self):
        files = [u'new.png', u'new.png', u'new.png', u'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 4)
        self.assertIn(u'new.png', icons[0])
        self.assertIn(u'new_(1).png', icons[1])
        self.assertIn(u'new_(2).png', icons[2])
        self.assertIn(u'new_(3).png', icons[3])


    def testAddIcons_13(self):
        files = [u'__sample.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertNotIn(u'__sample.png', icons[0])
        self.assertIn(u'sample.png', icons[0])


    def testAddIcons_14(self):
        files = [u'______sample.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertNotIn(u'______sample.png', icons[0])
        self.assertNotIn(u'__sample.png', icons[0])
        self.assertIn(u'sample.png', icons[0])


    def testAddIcons_15(self):
        files = [u'______sample.png', '__sample.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertNotIn(u'__sample.png', icons[0])
        self.assertIn(u'sample.png', icons[0])
        self.assertIn(u'sample_(1).png', icons[1])


    def testAddIcons_16_invalid(self):
        files = [u'invalid.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 0)


    def testAddIcons_17_invalid(self):
        files = [u'invalid.png', u'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertIn(u'new.png', icons[0])


    def testAddIcons_18_invalid(self):
        files = [u'new.png', u'invalid.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertIn(u'new.png', icons[0])


    def testAddIcons_19_resize(self):
        files = [u'16x16.png',
                 u'16x15.png',
                 u'16x17.png',
                 u'15x16.png',
                 u'17x16.png',
                 u'17x17.png',
                 u'15x15.png',
                 u'8x8.png',
                 u'8x16.png',
                 u'16x8.png',
                 u'first.png',
                 u'first_vertical.png']

        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addIcons(None, fullPaths)

        icons = sorted(collection.getIcons(None))
        self.assertEqual(len(icons), 12)

        icons = {fname: os.path.join(self.tempDir1, fname) for fname in files}

        for fname in files:
            self.assertEqual(getImageSize(icons[fname]), (16, 16))


    def testAddCover_01_group(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)
        collection.addIcons(groupname, fullPaths)

        coverpath = os.path.join(self.imagesDir, u'icon.png')

        newCoverPath = os.path.join(self.tempDir1,
                                    groupname,
                                    IconsCollection.COVER_FILE_NAME)

        collection.setCover(groupname, coverpath)
        self.assertTrue(os.path.exists(newCoverPath))
        self.assertEqual(os.path.abspath(newCoverPath),
                         os.path.abspath(collection.getCover(groupname)))

        collection.setCover(groupname, coverpath)
        self.assertTrue(os.path.exists(os.path.join(
            self.tempDir1,
            groupname,
            IconsCollection.COVER_FILE_NAME))
        )


    def testAddCover_02_root(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        coverpath = os.path.join(self.imagesDir, u'icon.png')

        newCoverPath = os.path.join(self.tempDir1,
                                    IconsCollection.COVER_FILE_NAME)

        collection.setCover(None, coverpath)
        self.assertTrue(os.path.exists(newCoverPath))
        self.assertEqual(os.path.abspath(newCoverPath),
                         os.path.abspath(collection.getCover(None)))

        collection.setCover(None, coverpath)
        self.assertTrue(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )


    def testAddCover_03_root(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        coverpath = os.path.join(self.imagesDir, u'icon.png')

        newCoverPath = os.path.join(self.tempDir1,
                                    IconsCollection.COVER_FILE_NAME)

        collection.setCover(u'', coverpath)
        self.assertTrue(os.path.exists(newCoverPath))
        self.assertEqual(os.path.abspath(newCoverPath),
                         os.path.abspath(collection.getCover(None)))

        collection.setCover(u'', coverpath)
        self.assertTrue(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )


    def testAddCover_04_root_invalid(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        coverpath = os.path.join(self.imagesDir, u'invalid.png')

        collection.setCover(u'', coverpath)
        self.assertFalse(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )


    def testAddCover_05_root(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        coverpath = os.path.join(self.imagesDir, u'first.jpg')

        collection.setCover(None, coverpath)
        self.assertTrue(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )

        self.assertEqual(self.__getMaxImageSize(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME)), 16)


    def testAddCover_06_group(self):
        files = [u'new.png', '8x8.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = u'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)
        collection.addIcons(groupname, fullPaths)

        coverpath = os.path.join(self.imagesDir, u'icon.png')

        newCoverPath = os.path.join(self.tempDir1,
                                    groupname,
                                    IconsCollection.COVER_FILE_NAME)

        collection.setCover(groupname, coverpath)
        self.assertTrue(os.path.exists(newCoverPath))
        self.assertEqual(
            os.path.abspath(newCoverPath),
            os.path.abspath(collection.getCover(groupname))
        )


    def __getMaxImageSize(self, fname):
        (width, height) = getImageSize(fname)
        return max(width, height)
