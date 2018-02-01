# -*- coding: UTF-8 -*-

import os

from outwiker.core.iconscollection import IconsCollection, DuplicateGroupError

from .utils import removeDir, getImageSize
from .basetestcases import BaseWxTestCase


class IconsCollectionTest(BaseWxTestCase):
    def setUp(self):
        super().setUp()
        self.tempDir1 = '../test/testIcons1'
        self.imagesDir = '../test/images'

    def tearDown(self):
        super().tearDown()
        removeDir(self.tempDir1)

    def testEmpty_01(self):
        collection = IconsCollection('../test/icons/Без иконок')

        self.assertEqual(collection.getIcons(''), [])
        self.assertEqual(collection.getGroups(), [])
        self.assertRaises(KeyError, collection.getIcons, 'Группа')
        self.assertRaises(KeyError, collection.getCover, 'Группа')
        self.assertIsNone(collection.getCover(None))

    def testEmpty_02(self):
        collection = IconsCollection('../test/icons/Без иконок')

        self.assertEqual(collection.getIcons(None), [])
        self.assertEqual(collection.getGroups(), [])
        self.assertRaises(KeyError, collection.getIcons, 'Группа')
        self.assertRaises(KeyError, collection.getCover, 'Группа')
        self.assertIsNone(collection.getCover(''))

    def testSingleRoot(self):
        collection = IconsCollection('../test/icons/Без групп')

        self.assertEqual(len(collection.getIcons(None)), 4)
        self.assertEqual(collection.getGroups(), [])
        self.assertTrue(collection.getCover(None).endswith('__cover.png'))

    def testGroups_01(self):
        collection = IconsCollection('../test/icons/Иконки и группы')

        self.assertEqual(len(collection.getIcons(None)), 4)
        self.assertEqual(collection.getGroups(), ['Группа 1', 'Группа 2'])
        self.assertEqual(len(collection.getIcons('Группа 1')), 3)
        self.assertEqual(len(collection.getIcons('Группа 2')), 4)
        self.assertIsNone(collection.getCover(None))
        self.assertTrue(
            collection.getCover('Группа 1').endswith('__cover.png'))
        self.assertIsNone(collection.getCover('Группа 2'))

    def testGroups_02(self):
        collection = IconsCollection('../test/icons/Только группы')

        self.assertEqual(len(collection.getIcons(None)), 0)
        self.assertEqual(collection.getGroups(), ['Группа 3', 'Группа 4'])
        self.assertEqual(len(collection.getIcons('Группа 3')), 3)
        self.assertEqual(len(collection.getIcons('Группа 4')), 4)
        self.assertIsNone(collection.getCover(None))

    def testAddGroup_01(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        self.assertEqual(collection.getGroups(), [])

        collection.addGroup('Новая группа')
        self.assertEqual(collection.getGroups(), ['Новая группа'])

        newcollection1 = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection1.getGroups(), ['Новая группа'])

    def testAddGroup_02_invalid(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        self.assertRaises(ValueError,
                          collection.addGroup,
                          'Абырвалг\\Абырвалг')
        self.assertRaises(ValueError,
                          collection.addGroup,
                          'Абырвалг/Абырвалг')
        self.assertRaises(ValueError, collection.addGroup, '')

    def testAddGroup_03(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        self.assertEqual(collection.getGroups(), [])

        collection.addGroup('Новая группа')
        collection.addGroup('Вторая группа')
        self.assertEqual(collection.getGroups(),
                         ['Вторая группа', 'Новая группа'])

        newcollection = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection.getGroups(),
                         ['Вторая группа', 'Новая группа'])

    def testRenameGroup_01(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')
        self.assertEqual(collection.getGroups(), ['Новая группа'])

        collection.renameGroup('Новая группа', 'Переименованная группа')
        self.assertEqual(collection.getGroups(), ['Переименованная группа'])

        newcollection1 = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection1.getGroups(),
                         ['Переименованная группа'])

    def testRenameGroup_02_invalid(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')

        self.assertRaises(
            ValueError,
            collection.renameGroup,
            'Новая группа',
            '')

        self.assertRaises(
            ValueError,
            collection.renameGroup,
            'Новая группа',
            'Абырвалг/Абырвалг')

        self.assertRaises(
            ValueError,
            collection.renameGroup,
            'Новая группа',
            'Абырвалг\\Абырвалг')

    def testRenameGroup_03_self(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')

        collection.renameGroup('Новая группа', 'Новая группа')
        self.assertEqual(collection.getGroups(), ['Новая группа'])

        newcollection = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection.getGroups(), ['Новая группа'])

    def testRenameGroup_04_self(self):
        files = ['new.png', 'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')
        collection.addIcons('Новая группа', fullPaths)

        collection.renameGroup('Новая группа', 'Новая группа')
        self.assertEqual(collection.getGroups(), ['Новая группа'])
        self.assertEqual(len(collection.getIcons('Новая группа')), 2)

        newcollection = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection.getGroups(), ['Новая группа'])
        self.assertEqual(len(newcollection.getIcons('Новая группа')), 2)

    def testRenameGroup_04_invalid(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')
        collection.addGroup('Абырвалг')

        self.assertRaises(
            DuplicateGroupError,
            collection.renameGroup,
            'Новая группа',
            'Абырвалг')

    def testRemoveGroup_01(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')
        collection.addGroup('Другая группа')

        collection.removeGroup('Новая группа')
        self.assertEqual(collection.getGroups(), ['Другая группа'])

        newcollection1 = IconsCollection(self.tempDir1)
        self.assertEqual(newcollection1.getGroups(), ['Другая группа'])

    def testRemoveGroup_02(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')

        collection.removeGroup('Новая группа')
        self.assertEqual(collection.getGroups(), [])

    def testRemoveGroup_03_invalid(self):
        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')

        self.assertRaises(
            KeyError,
            collection.removeGroup,
            'Абырвалг')

        self.assertRaises(
            KeyError,
            collection.removeGroup,
            '')

    def testRemoveGroup_04(self):
        files = ['new.png', 'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)

        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')
        collection.addIcons('Новая группа', fullPaths)

        collection.removeGroup('Новая группа')
        self.assertEqual(collection.getGroups(), [])

    def testAddIcons_01_empty(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')

        collection.addIcons('Новая группа', fullPaths)
        self.assertEqual(collection.getIcons('Новая группа'), [])

    def testAddIcons_02_empty(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup('Новая группа')

        collection.addIcons('Новая группа', fullPaths)
        self.assertEqual(collection.getIcons('Новая группа'), [])

    def testAddIcons_03_empty(self):
        files = []
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons('', fullPaths)
        self.assertEqual(collection.getIcons(None), [])

    def testAddIcons_04_invalid(self):
        files = ['new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        self.assertRaises(
            KeyError,
            collection.addIcons,
            'Другая группа',
            fullPaths)

    def testAddIcons_05(self):
        files = ['new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons('', fullPaths)

        icons = collection.getIcons(None)
        self.assertIn('new.png', icons[0])
        self.assertIsNone(collection.getCover(None))

    def testAddIcons_06(self):
        files = ['new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons(None, fullPaths)

        icons = collection.getIcons(None)
        self.assertIn('new.png', icons[0])

    def testAddIcons_07(self):
        files = ['new.png', 'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        collection.addIcons(None, fullPaths)

        icons = sorted(collection.getIcons(None))
        self.assertIn('image_01.png', icons[0])
        self.assertIn('new.png', icons[1])

    def testAddIcons_08(self):
        files = ['new.png', 'image_01.JPG']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn('image_01.png', icons[0])
        self.assertIn('new.png', icons[1])
        self.assertIsNone(collection.getCover('Новая группа'))

    def testAddIcons_09(self):
        files = ['new.png', 'image_01.JPG', '__init__.py']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn('image_01.png', icons[0])
        self.assertIn('new.png', icons[1])

    def testAddIcons_10_not_exists(self):
        files = ['new.png', 'image_01.JPG', 'notexists.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn('image_01.png', icons[0])
        self.assertIn('new.png', icons[1])

    def testAddIcons_11(self):
        files = ['new.png', 'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertIn('new.png', icons[0])
        self.assertIn('new_(1).png', icons[1])

    def testAddIcons_12(self):
        files = ['new.png', 'new.png', 'new.png', 'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 4)
        self.assertIn('new.png', icons[0])
        self.assertIn('new_(1).png', icons[1])
        self.assertIn('new_(2).png', icons[2])
        self.assertIn('new_(3).png', icons[3])

    def testAddIcons_13(self):
        files = ['__sample.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertNotIn('__sample.png', icons[0])
        self.assertIn('sample.png', icons[0])

    def testAddIcons_14(self):
        files = ['______sample.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertNotIn('______sample.png', icons[0])
        self.assertNotIn('__sample.png', icons[0])
        self.assertIn('sample.png', icons[0])

    def testAddIcons_15(self):
        files = ['______sample.png', '__sample.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 2)
        self.assertNotIn('__sample.png', icons[0])
        self.assertIn('sample.png', icons[0])
        self.assertIn('sample_(1).png', icons[1])

    def testAddIcons_16_invalid(self):
        files = ['invalid.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 0)

    def testAddIcons_17_invalid(self):
        files = ['invalid.png', 'new.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertIn('new.png', icons[0])

    def testAddIcons_18_invalid(self):
        files = ['new.png', 'invalid.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)

        collection.addIcons(groupname, fullPaths)

        icons = sorted(collection.getIcons(groupname))
        self.assertEqual(len(icons), 1)
        self.assertIn('new.png', icons[0])

    def testAddIcons_19_resize(self):
        files = ['16x16.png',
                 '16x15.png',
                 '16x17.png',
                 '15x16.png',
                 '17x16.png',
                 '17x17.png',
                 '15x15.png',
                 '8x8.png',
                 '8x16.png',
                 '16x8.png',
                 'first.png',
                 'first_vertical.png']

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

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)
        collection.addIcons(groupname, fullPaths)

        coverpath = os.path.join(self.imagesDir, 'icon.png')

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

        coverpath = os.path.join(self.imagesDir, 'icon.png')

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

        coverpath = os.path.join(self.imagesDir, 'icon.png')

        newCoverPath = os.path.join(self.tempDir1,
                                    IconsCollection.COVER_FILE_NAME)

        collection.setCover('', coverpath)
        self.assertTrue(os.path.exists(newCoverPath))
        self.assertEqual(os.path.abspath(newCoverPath),
                         os.path.abspath(collection.getCover(None)))

        collection.setCover('', coverpath)
        self.assertTrue(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )

    def testAddCover_04_root_invalid(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        coverpath = os.path.join(self.imagesDir, 'invalid.png')

        collection.setCover('', coverpath)
        self.assertFalse(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )

    def testAddCover_05_root(self):
        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)

        coverpath = os.path.join(self.imagesDir, 'first.jpg')

        collection.setCover(None, coverpath)
        self.assertTrue(os.path.exists(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME))
        )

        self.assertEqual(self.__getMaxImageSize(os.path.join(
            self.tempDir1,
            IconsCollection.COVER_FILE_NAME)), 16)

    def testAddCover_06_group(self):
        files = ['new.png', '8x8.png']
        fullPaths = [os.path.join(self.imagesDir, fname) for fname in files]

        groupname = 'Новая группа'

        os.mkdir(self.tempDir1)
        collection = IconsCollection(self.tempDir1)
        collection.addGroup(groupname)
        collection.addIcons(groupname, fullPaths)

        coverpath = os.path.join(self.imagesDir, 'icon.png')

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
