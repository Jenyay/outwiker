# -*- coding: utf-8 -*-

import unittest
import os
import os.path
from pathlib import Path
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


class AttachmentTest(unittest.TestCase):
    def setUp(self):
        self._application = Application()
        # Количество срабатываний особытий при обновлении страницы
        self.pageUpdateCount = 0
        self.pageUpdateSender = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        self.page = self.wikiroot["Страница 1"]

        self.filesPath = "testdata/samplefiles/"
        self.files = ["accept.png",
                      "add.png",
                      "anchor.png",
                      "файл с пробелами.tmp",
                      "dir"]
        self.fullFilesPath = [os.path.join(self.filesPath, fname)
                              for fname in self.files]

        self._application.wikiroot = self.wikiroot

    def tearDown(self):
        removeDir(self.path)

    def onAttachListChanged(self, sender, params):
        self.pageUpdateCount += 1
        self.pageUpdateSender = sender

    def testAttachPath1(self):
        attach = Attachment(self.page)
        self.assertEqual(attach.getAttachPath(),
                         os.path.join(self.page.path, PAGE_ATTACH_DIR))

    def testAttachPath2(self):
        attach = Attachment(self.page)

        # Получить путь до прикрепленных файлов, не создавая ее
        path = attach.getAttachPath()
        # Вложенных файлов еще нет, поэтому нет и папки
        self.assertFalse(os.path.exists(path))

    def testAttachPath3(self):
        attach = Attachment(self.page)

        # Получить путь до прикрепленных файлов, не создавая ее
        path = attach.getAttachPath(create=False)
        # Вложенных файлов еще нет, поэтому нет и папки
        self.assertFalse(os.path.exists(path))

    def testAttachPath4(self):
        attach = Attachment(self.page)

        # Получить путь до прикрепленных файлов, создав ее
        path = attach.getAttachPath(create=True)
        self.assertTrue(os.path.exists(path))

    def testEvent(self):
        self.pageUpdateCount = 0

        self._application.onAttachListChanged += self.onAttachListChanged

        attach = Attachment(self.page)

        # Прикрепим к двум страницам файлы
        attach.attach(self.fullFilesPath[: 2])

        self.assertEqual(self.pageUpdateCount, 1)
        self.assertEqual(self.pageUpdateSender, self.page)

        attach.attach(self.fullFilesPath[2:])

        self.assertEqual(self.pageUpdateCount, 2)
        self.assertEqual(self.pageUpdateSender, self.page)

        self._application.onAttachListChanged -= self.onAttachListChanged

    def testAttachFull1(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertEqual(len(attach.attachmentFull),
                         len(self.fullFilesPath))

        attachBasenames = [os.path.basename(path)
                           for path in attach.attachmentFull]

        for path in self.fullFilesPath:
            self.assertTrue(os.path.basename(path) in attachBasenames, path)

        for path in attach.attachmentFull:
            self.assertTrue(os.path.exists(path))

    def testAttachFull2(self):
        attach = Attachment(self.page)
        attach2 = Attachment(self.page)

        attach.attach(self.fullFilesPath)

        self.assertTrue(attach != attach2)
        self.assertEqual(len(attach2.attachmentFull),
                         len(self.fullFilesPath))

        attachBasenames = [os.path.basename(path)
                           for path in attach2.attachmentFull]

        for path in self.fullFilesPath:
            self.assertTrue(os.path.basename(path) in attachBasenames, path)

    def testAttachFull3(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        attach2 = Attachment(self.page)
        self.assertTrue(attach != attach2)
        self.assertEqual(len(attach2.attachmentFull), len(self.fullFilesPath))

        attachBasenames = [os.path.basename(path)
                           for path in attach2.attachmentFull]

        for path in self.fullFilesPath:
            self.assertTrue(os.path.basename(path) in attachBasenames, path)

    def testAttachSubfolder1(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        attachBasenames = [os.path.basename(path)
                           for path in attach.getAttachFull('dir')]

        expected_files = ['subdir', 'attach.png', 'dir.xxx']
        for fname in expected_files:
            self.assertTrue(fname in attachBasenames)

    def testAttachSubfolder2(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        attachBasenames = [os.path.basename(path)
                           for path in attach.getAttachFull('dir/subdir/subdir2/')]

        expected_files = ['image.png', 'картинка с пробелами.png',
                          'application.py', 'файл с пробелами.tmp']
        for fname in expected_files:
            self.assertTrue(fname in attachBasenames)

    def testAttachBasename(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertEqual(len(attach.getAttachRelative()), len(self.files))

        attachBasenames = attach.getAttachRelative()

        for fname in self.files:
            self.assertTrue(fname in attachBasenames, fname)

    def testRemoveAttachesEvent(self):
        attach = Attachment(self.page)

        attach.attach(self.fullFilesPath)

        self._application.onAttachListChanged += self.onAttachListChanged

        attach.removeAttach([self.files[0]])

        self.assertEqual(len(attach.attachmentFull),
                         len(self.fullFilesPath) - 1)
        self.assertEqual(self.pageUpdateCount, 1)
        self.assertEqual(self.pageUpdateSender, self.page)

        attach.removeAttach([self.files[1], self.files[2]])

        self.assertEqual(len(attach.attachmentFull),
                         len(self.fullFilesPath) - 3)
        self.assertEqual(self.pageUpdateCount, 2)
        self.assertEqual(self.pageUpdateSender, self.page)

        self._application.onAttachListChanged -= self.onAttachListChanged

    def testRemoveAttaches1(self):
        attach = Attachment(self.page)

        attach.attach(self.fullFilesPath)

        attach.removeAttach([self.files[0]])

        self.assertEqual(len(attach.attachmentFull),
                         len(self.fullFilesPath[1:]))

        attachBasenames = [os.path.basename(path)
                           for path in attach.attachmentFull]

        for path in self.fullFilesPath[1:]:
            self.assertTrue(os.path.basename(path) in attachBasenames, path)

        for path in attach.attachmentFull:
            self.assertTrue(os.path.exists(path))

    def testRemoveAttaches2(self):
        attach = Attachment(self.page)
        attach2 = Attachment(self.page)

        attach.attach(self.fullFilesPath)

        attach.removeAttach([self.files[0]])

        self.assertEqual(len(attach2.attachmentFull),
                         len(self.fullFilesPath[1:]))

        attachBasenames = [os.path.basename(path)
                           for path in attach2.attachmentFull]

        for path in self.fullFilesPath[1:]:
            self.assertTrue(os.path.basename(path) in attachBasenames, path)

    def testRemoveAttaches3(self):
        attach = Attachment(self.page)
        attach2 = Attachment(self.page)

        attach.attach(self.fullFilesPath)

        attach2.removeAttach([self.files[0]])

        self.assertEqual(len(attach.attachmentFull),
                         len(self.fullFilesPath[1:]))
        self.assertEqual(len(attach2.attachmentFull),
                         len(self.fullFilesPath[1:]))

        attachBasenames = [os.path.basename(path)
                           for path in attach.attachmentFull]

        for path in self.fullFilesPath[1:]:
            self.assertTrue(os.path.basename(path) in attachBasenames, path)

    def testRemoveAttachDir1(self):
        attach = Attachment(self.page)

        attach.attach(self.fullFilesPath)

        attach.removeAttach(["dir"])

        self.assertEqual(len(attach.attachmentFull),
                         len(self.fullFilesPath[1:]))

    def testInvalidRemoveAttaches(self):
        """
        Попытка удалить прикрепления, которого нет
        """
        attach = Attachment(self.page)
        files = ["accept_111.png", "add.png_111", "anchor.png_111"]

        self.assertRaises(IOError, attach.removeAttach, files)
        self.assertRaises(IOError, attach.removeAttach, ["dir_111"])

    def testSortByName(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("testdata/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        attach2 = Attachment(self.page)
        files_list = [os.path.basename(fname)
                      for fname in attach2.attachmentFull]
        files_list.sort(key=str.lower)

        self.assertEqual(files_list[0], "add.png")
        self.assertEqual(files_list[1], "add.png2")
        self.assertEqual(files_list[2], "Anchor.png")
        self.assertEqual(files_list[3], "filename")
        self.assertEqual(files_list[4], "image.png")
        self.assertEqual(files_list[5], "image2.png")
        self.assertEqual(files_list[6], "файл с пробелами.tmp")

    def testSortByExt(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("testdata/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        attach2 = Attachment(self.page)
        files_list = [os.path.basename(fname)
                      for fname in attach2.attachmentFull]
        files_list.sort(key=Attachment.sortByExt)

        self.assertEqual(files_list[0], "filename")
        self.assertEqual(files_list[1], "add.png")
        self.assertEqual(files_list[2], "Anchor.png")
        self.assertEqual(files_list[3], "image.png")
        self.assertEqual(files_list[4], "image2.png")
        self.assertEqual(files_list[5], "add.png2")
        self.assertEqual(files_list[6], "файл с пробелами.tmp")

    def testSortByDate(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("testdata/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        files_list = attach.attachmentFull
        files_list.sort(key=str.lower)

        os.utime(files_list[3], (1000000000, 1000000000))
        os.utime(files_list[0], (1000000000, 1100000000))
        os.utime(files_list[2], (1000000000, 1200000000))
        os.utime(files_list[6], (1000000000, 1300000000))
        os.utime(files_list[4], (1000000000, 1400000000))
        os.utime(files_list[5], (1000000000, 1500000000))
        os.utime(files_list[1], (1000000000, 1600000000))

        Attachment(self.page)
        files_list2 = attach.attachmentFull
        files_list2.sort(key=Attachment.sortByDate)

        for n in range(1, len(files)):
            self.assertTrue(os.stat(files_list2[n - 1]).st_mtime <=
                            os.stat(files_list2[n]).st_mtime)

    def testSortByDateRelative(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("testdata/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        files_list = attach.attachmentFull
        files_list.sort(key=str.lower)

        os.utime(files_list[3], (1000000000, 1000000000))
        os.utime(files_list[0], (1000000000, 1100000000))
        os.utime(files_list[2], (1000000000, 1200000000))
        os.utime(files_list[6], (1000000000, 1300000000))
        os.utime(files_list[4], (1000000000, 1400000000))
        os.utime(files_list[5], (1000000000, 1500000000))
        os.utime(files_list[1], (1000000000, 1600000000))

        attach2 = Attachment(self.page)
        files_list2 = attach.getAttachRelative()
        files_list2.sort(key=attach2.sortByDateRelative)

        for n in range(1, len(files)):
            self.assertTrue(os.stat(attach2.getFullPath(files_list2[n - 1])).st_mtime <=
                            os.stat(attach2.getFullPath(files_list2[n])).st_mtime)

    def testSortBySize(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("testdata/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)
        attach.attach([os.path.join("testdata/samplefiles", "dir")])

        attach2 = Attachment(self.page)
        files_list = attach2.attachmentFull
        files_list.sort(key=Attachment.sortBySize)

        for n in range(1, len(files_list)):
            self.assertTrue(os.stat(files_list[n - 1]).st_size <=
                            os.stat(files_list[n]).st_size)

    def testSortBySizeRelative(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("testdata/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)
        attach.attach([os.path.join("testdata/samplefiles", "dir")])

        attach2 = Attachment(self.page)
        files_list = attach2.getAttachRelative()
        files_list.sort(key=attach2.sortBySizeRelative)

        for n in range(1, len(files_list)):
            self.assertTrue(os.stat(attach2.getFullPath(files_list[n - 1])).st_size <=
                            os.stat(attach2.getFullPath(files_list[n])).st_size)

    def testGetFullPath1(self):
        attach = Attachment(self.page)
        fname = "Имя файла.ext"

        path_full = attach.getFullPath(fname, create=False)
        path_right = os.path.join(attach.getAttachPath(), fname)

        self.assertFalse(os.path.exists(attach.getAttachPath()))
        self.assertEqual(path_full, path_right)

    def testGetFullPath2(self):
        attach = Attachment(self.page)
        fname = "Имя файла.ext"

        path_full = attach.getFullPath(fname)
        path_right = os.path.join(attach.getAttachPath(), fname)

        self.assertFalse(os.path.exists(attach.getAttachPath()))
        self.assertEqual(path_full, path_right)

    def testGetFullPath3(self):
        attach = Attachment(self.page)
        fname = "Имя файла.ext"

        path_full = attach.getFullPath(fname, create=True)
        path_right = os.path.join(attach.getAttachPath(), fname)

        self.assertTrue(os.path.exists(attach.getAttachPath()))
        self.assertEqual(path_full, path_right)

    def testGetAttachRelative1(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        attach_right = set(self.files)

        attach_names = set(attach.getAttachRelative())
        self.assertEqual(attach_right, attach_names)

    def testGetAttachRelative2(self):
        attach = Attachment(self.page)
        attach_right = set([])

        attach_names = set(attach.getAttachRelative())
        self.assertEqual(attach_right, attach_names)

    def testGetAttachRelative3(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        attach_right = set(self.files)

        attach_names = set(attach.getAttachRelative())
        self.assertEqual(attach_right, attach_names)

    def testGetAttachRelative4(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        attach_right = set(["attach.png", "dir.xxx", "subdir"])

        attach_names = set(attach.getAttachRelative("dir"))
        self.assertEqual(attach_right, attach_names)

    def testGetAttachRelative5(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertRaises(OSError, attach.getAttachRelative, "invaliddir")

    def testAttachSubdir(self):
        subdir = 'dir/subdir/subdir2/'
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertEqual(len(attach.getAttachFull(subdir)), 4)

        new_file = os.path.join(self.filesPath, 'dir.png')
        attach.attach([new_file], subdir)

        self.assertEqual(len(attach.getAttachFull(subdir)), 5)

    def testAttachNewSubdir(self):
        subdir = 'new_subdir'
        attach = Attachment(self.page)

        new_file = os.path.join(self.filesPath, 'dir.png')
        attach.attach([new_file], subdir=subdir)
        self.assertTrue(Path(attach.getAttachPath(), subdir).exists())

    def testFixSubdirRootNotExists(self):
        attach = Attachment(self.page)
        expected = None

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False),
                                    self.page.currentAttachSubdir)

        self.assertEqual(result, expected)
        self.assertFalse(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, '')

    def testFixSubdirRootNotExistsSubdir(self):
        subdir = 'invalid'
        self.page.currentAttachSubdir = subdir

        attach = Attachment(self.page)
        expected = None

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False),
                                    self.page.currentAttachSubdir)

        self.assertEqual(result, expected)
        self.assertFalse(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, '')

    def testFixSubdir_01(self):
        subdir = 'invalid'
        self.page.currentAttachSubdir = subdir

        attach = Attachment(self.page)
        expected = attach.getAttachPath(create=True)

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False),
                                    self.page.currentAttachSubdir)

        self.assertTrue(os.path.samefile(result, expected))
        self.assertTrue(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, '')

    def testFixSubSubdir_1(self):
        subdir = 'sub1/sub2'
        self.page.currentAttachSubdir = subdir

        attach = Attachment(self.page)
        expected = attach.getAttachPath(create=True)

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False),
                                    self.page.currentAttachSubdir)

        self.assertTrue(os.path.samefile(result, expected))
        self.assertTrue(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, '')

    def testFixSubSubdir_2(self):
        subdir = 'sub1/sub2'
        self.page.currentAttachSubdir = subdir

        attach = Attachment(self.page)
        root = attach.getAttachPath(create=True)

        expected = os.path.join(root, 'sub1')
        os.mkdir(expected)

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False), 'sub1')

        self.assertTrue(os.path.samefile(result, expected))
        self.assertTrue(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, 'sub1')

    def testFixSubSubdir_3_Ok(self):
        subdir = 'sub1/sub2'
        self.page.currentAttachSubdir = subdir

        attach = Attachment(self.page)
        root = attach.getAttachPath(create=True)

        expected = os.path.join(root, subdir)
        os.makedirs(expected)

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False), subdir)

        self.assertTrue(os.path.samefile(result, expected))
        self.assertTrue(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, subdir)

    def testFixSubSubdir_4(self):
        subdir = 'sub1/sub2/sub3'
        self.page.currentAttachSubdir = subdir

        attach = Attachment(self.page)
        root = attach.getAttachPath(create=True)

        expected = os.path.join(root, 'sub1/sub2')
        os.makedirs(expected)

        result = attach.fixCurrentSubdir()
        current_path = os.path.join(attach.getAttachPath(create=False), 'sub1/sub2')

        self.assertTrue(os.path.samefile(result, expected))
        self.assertTrue(os.path.exists(current_path))
        self.assertEqual(self.page.currentAttachSubdir, 'sub1/sub2')

    def testCreateSubdirSimple(self):
        subdir = 'subdir'
        attach = Attachment(self.page)

        result = Path(attach.createSubdir(subdir)).resolve()
        path_expected = Path(attach.getAttachPath(create=False), subdir).resolve()

        self.assertEqual(result, path_expected)
        self.assertTrue(path_expected.exists())
        self.assertTrue(path_expected.is_dir())

    def testCreateNestedDir(self):
        subdir = Path('subdir1', 'subdir2')
        attach = Attachment(self.page)

        result = Path(attach.createSubdir(subdir)).resolve()
        path_expected = Path(attach.getAttachPath(create=False), subdir).resolve()

        self.assertEqual(result, path_expected)
        self.assertTrue(path_expected.exists())
        self.assertTrue(path_expected.is_dir())

    def testCreateSubdir(self):
        subdir1 = 'subdir1'
        subdir2 = Path(subdir1, 'subdir2')

        attach = Attachment(self.page)

        attach.createSubdir(subdir1)
        result = Path(attach.createSubdir(subdir2)).resolve()
        path_expected = Path(attach.getAttachPath(create=False), subdir2).resolve()

        self.assertEqual(result, path_expected)
        self.assertTrue(path_expected.exists())
        self.assertTrue(path_expected.is_dir())

    def testCreateSubdirReadonly(self):
        subdir = 'subdir'
        self.page.readonly = True
        attach = Attachment(self.page)

        self.assertRaises(ReadonlyException, attach.createSubdir, subdir)

    def testCreateSubdirWithParentPath_01(self):
        subdir = '../subdir'
        attach = Attachment(self.page)

        self.assertRaises(OSError, attach.createSubdir, subdir)

    def testCreateSubdirWithParentPath_02(self):
        subdir = '..'
        attach = Attachment(self.page)

        self.assertRaises(OSError, attach.createSubdir, subdir)

    def testAttachExists(self):
        attach = Attachment(self.page)
        attach.attach(self.fullFilesPath)

        self.assertTrue(attach.exists('accept.png'))
        self.assertFalse(attach.exists('invalid.png'))

        self.assertTrue(attach.exists('attach.png', subdir='dir'))
        self.assertFalse(attach.exists('invalid.png', subdir='dir'))

        self.assertTrue(attach.exists('dir/attach.png'))
        self.assertFalse(attach.exists('dir/invalid.png'))
