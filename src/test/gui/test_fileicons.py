# -*- coding: utf-8 -*-

import os
from unittest import skipIf, TestCase

from outwiker.gui.fileicons import UnixFileIcons, WindowsFileIcons
from test.basetestcases import BaseOutWikerGUIMixin


class FileIconsTestUnix(TestCase, BaseOutWikerGUIMixin):
    """
    Тесты классов для отображения иконок прикрепленных файлов
    """
    def setUp(self):
        self.initApplication()

    def tearDown(self):
        self.destroyApplication()

    def testInit_unix(self):
        fi = UnixFileIcons()
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 0)

    def testExt_unix(self):
        fi = UnixFileIcons()
        index = fi.getFileImage("/file.bmp")
        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

        index = fi.getFileImage("/file.gif")
        self.assertEqual(fi.dictSize, 2)
        self.assertEqual(fi.imageListCount, 4)
        self.assertEqual(index, 3)

        index = fi.getFileImage("/other_file.bmp")
        self.assertEqual(fi.dictSize, 2)
        self.assertEqual(fi.imageListCount, 4)
        self.assertEqual(index, 2)

    def test_invalid_icon_unix(self):
        fi = UnixFileIcons()
        fname = "c:\\file.abyrvalg"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 0)

    def test_folder_unix(self):
        fi = UnixFileIcons()
        fname = "../test/samplefiles"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 1)

    def test_clear_unix(self):
        fi = UnixFileIcons()
        index = fi.getFileImage("c:\\file.bmp")
        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

        fi.clear()
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 0)

    def test_clear_after_unix(self):
        fi = UnixFileIcons()
        fi.clear()
        index = fi.getFileImage("c:\\file.bmp")

        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

    def test_clear_after_invalid_unix(self):
        fi = UnixFileIcons()
        fi.clear()
        index = fi.getFileImage("c:\\file.abyrvalg")

        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 0)


@skipIf(os.name != "nt", 'Test executed under Windows only')
class FileIconsTestWindows(TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

    def tearDown(self):
        self.destroyApplication()

    def test_clear_after_folder_win(self):
        fi = WindowsFileIcons()
        fi.clear()
        index = fi.getFileImage("../test/samplefiles")

        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 1)

    def test_clear_after_folder_unix(self):
        fi = UnixFileIcons()
        fi.clear()
        index = fi.getFileImage("../test/samplefiles")

        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 1)

    def testInit_win(self):
        fi = WindowsFileIcons()
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 0)

    def testExt_win(self):
        fi = WindowsFileIcons()
        index = fi.getFileImage("c:\\file.bmp")
        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

        index = fi.getFileImage("c:\\file.gif")
        self.assertEqual(fi.dictSize, 2)
        self.assertEqual(fi.imageListCount, 4)
        self.assertEqual(index, 3)

        index = fi.getFileImage("c:\\other_file.bmp")
        self.assertEqual(fi.dictSize, 2)
        self.assertEqual(fi.imageListCount, 4)
        self.assertEqual(index, 2)

    def testExe_win(self):
        fi = WindowsFileIcons()
        fname = "..\\test\\samplefiles\\example.exe"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

    def testExe_invalid_win(self):
        fi = WindowsFileIcons()
        fname = "..\\test\\samplefiles\\invalid.exe"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 0)

    def testExe_invalid2_win(self):
        fi = WindowsFileIcons()
        fname = "..\\test\\samplefiles\\invalid_none.exe"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 0)

    def test_invalid_icon_win(self):
        fi = WindowsFileIcons()
        fname = "c:\\file.abyrvalg"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 0)

    def test_folder_win(self):
        fi = WindowsFileIcons()
        fname = "../test/samplefiles"
        index = fi.getFileImage(fname)
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 1)

    def test_clear_win(self):
        fi = WindowsFileIcons()
        index = fi.getFileImage("c:\\file.bmp")
        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

        fi.clear()
        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 0)

    def test_clear_after_win(self):
        fi = WindowsFileIcons()
        fi.clear()
        index = fi.getFileImage("c:\\file.bmp")

        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

    def test_clear_after_exe_win(self):
        fi = WindowsFileIcons()
        fi.clear()
        index = fi.getFileImage("..\\test\\samplefiles\\example.exe")

        self.assertEqual(fi.dictSize, 1)
        self.assertEqual(fi.imageListCount, 3)
        self.assertEqual(index, 2)

    def test_clear_after_invalid_win(self):
        fi = WindowsFileIcons()
        fi.clear()
        index = fi.getFileImage("c:\\file.abyrvalg")

        self.assertEqual(fi.dictSize, 0)
        self.assertEqual(fi.imageListCount, 2)
        self.assertEqual(index, 0)
