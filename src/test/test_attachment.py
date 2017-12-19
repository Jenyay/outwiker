# -*- coding: UTF-8 -*-

import unittest
import os.path
from tempfile import mkdtemp
from functools import cmp_to_key

from outwiker.core.attachment import Attachment
from .utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.core.application import Application
from outwiker.core.events import PAGE_UPDATE_ATTACHMENT
from outwiker.core.defines import PAGE_ATTACH_DIR


class AttachmentTest(unittest.TestCase):
    def setUp(self):
        # Количество срабатываний особытий при обновлении страницы
        self.pageUpdateCount = 0
        self.pageUpdateSender = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        TextPageFactory().create(self.wikiroot, "Страница 1", [])
        self.page = self.wikiroot["Страница 1"]

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png",
                      "add.png",
                      "anchor.png",
                      "файл с пробелами.tmp",
                      "dir"]
        self.fullFilesPath = [os.path.join(filesPath, fname)
                              for fname in self.files]

        self.prev_kwargs = None
        Application.wikiroot = self.wikiroot

    def tearDown(self):
        removeDir(self.path)

    def onPageUpdate(self, sender, **kwargs):
        self.pageUpdateCount += 1
        self.pageUpdateSender = sender
        self.prev_kwargs = kwargs

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
        # Вложенных файлов еще нет, поэтому нет и папки
        self.assertTrue(os.path.exists(path))

    def testEvent(self):
        self.pageUpdateCount = 0

        Application.onPageUpdate += self.onPageUpdate

        attach = Attachment(self.page)

        # Прикрепим к двум страницам файлы
        attach.attach(self.fullFilesPath[: 2])

        self.assertEqual(self.pageUpdateCount, 1)
        self.assertEqual(self.pageUpdateSender, self.page)
        self.assertEqual(self.prev_kwargs['change'], PAGE_UPDATE_ATTACHMENT)

        attach.attach(self.fullFilesPath[2:])

        self.assertEqual(self.pageUpdateCount, 2)
        self.assertEqual(self.pageUpdateSender, self.page)

        Application.onPageUpdate -= self.onPageUpdate

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

        Application.onPageUpdate += self.onPageUpdate

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

        Application.onPageUpdate -= self.onPageUpdate

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

        fullFilesPath = [os.path.join("../test/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        attach2 = Attachment(self.page)
        files_list = [os.path.basename(fname)
                      for fname in attach2.attachmentFull]
        files_list.sort(key=cmp_to_key(Attachment.sortByName))

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

        fullFilesPath = [os.path.join("../test/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        attach2 = Attachment(self.page)
        files_list = [os.path.basename(fname)
                      for fname in attach2.attachmentFull]
        files_list.sort(key=cmp_to_key(Attachment.sortByExt))

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

        fullFilesPath = [os.path.join("../test/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        files_list = attach.attachmentFull
        files_list.sort(key=cmp_to_key(Attachment.sortByName))

        os.utime(files_list[3], (1000000000, 1000000000))
        os.utime(files_list[0], (1000000000, 1100000000))
        os.utime(files_list[2], (1000000000, 1200000000))
        os.utime(files_list[6], (1000000000, 1300000000))
        os.utime(files_list[4], (1000000000, 1400000000))
        os.utime(files_list[5], (1000000000, 1500000000))
        os.utime(files_list[1], (1000000000, 1600000000))

        Attachment(self.page)
        files_list2 = attach.attachmentFull
        files_list2.sort(key=cmp_to_key(Attachment.sortByDate))

        for n in range(1, len(files)):
            self.assertTrue(os.stat(files_list2[n - 1]).st_mtime <=
                            os.stat(files_list2[n]).st_mtime)

    def testSortByDateRelative(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("../test/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)

        files_list = attach.attachmentFull
        files_list.sort(key=cmp_to_key(Attachment.sortByName))

        os.utime(files_list[3], (1000000000, 1000000000))
        os.utime(files_list[0], (1000000000, 1100000000))
        os.utime(files_list[2], (1000000000, 1200000000))
        os.utime(files_list[6], (1000000000, 1300000000))
        os.utime(files_list[4], (1000000000, 1400000000))
        os.utime(files_list[5], (1000000000, 1500000000))
        os.utime(files_list[1], (1000000000, 1600000000))

        attach2 = Attachment(self.page)
        files_list2 = attach.getAttachRelative()
        files_list2.sort(key=cmp_to_key(attach2.sortByDateRelative))

        for n in range(1, len(files)):
            self.assertTrue(os.stat(attach2.getFullPath(files_list2[n - 1])).st_mtime <=
                            os.stat(attach2.getFullPath(files_list2[n])).st_mtime)

    def testSortBySize(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("../test/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)
        attach.attach([os.path.join("../test/samplefiles", "dir")])

        attach2 = Attachment(self.page)
        files_list = attach2.attachmentFull
        files_list.sort(key=cmp_to_key(Attachment.sortBySize))

        for n in range(1, len(files_list)):
            self.assertTrue(os.stat(files_list[n - 1]).st_size <=
                            os.stat(files_list[n]).st_size)

    def testSortBySizeRelative(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [os.path.join("../test/samplefiles/for_sort", fname)
                         for fname in files]

        attach = Attachment(self.page)
        attach.attach(fullFilesPath)
        attach.attach([os.path.join("../test/samplefiles", "dir")])

        attach2 = Attachment(self.page)
        files_list = attach2.getAttachRelative()
        files_list.sort(key=cmp_to_key(attach2.sortBySizeRelative))

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
