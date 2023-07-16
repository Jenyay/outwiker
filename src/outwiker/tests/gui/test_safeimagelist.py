# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.core.exceptions import InvalidImageFormat
from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class SafeImageListTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.width = 16
        self.height = 16
        self.imagelist = SafeImageList(self.width, self.height)

    def tearDown(self):
        self.destroyApplication()

    def test_16x16(self):
        self.imagelist.AddFromFile('testdata/images/16x16.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_15x15(self):
        self.imagelist.AddFromFile('testdata/images/15x15.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_15x16(self):
        self.imagelist.AddFromFile('testdata/images/15x16.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_16x15(self):
        self.imagelist.AddFromFile('testdata/images/16x15.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_17x16(self):
        self.imagelist.AddFromFile('testdata/images/17x16.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_16x17(self):
        self.imagelist.AddFromFile('testdata/images/16x17.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_17x17(self):
        self.imagelist.AddFromFile('testdata/images/17x17.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_invalid_format(self):
        with self.assertRaises(InvalidImageFormat):
            self.imagelist.AddFromFile('testdata/samplefiles/filename.tmp')

    def test_svg(self):
        self.imagelist.AddFromFile('testdata/images/example.svg')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_svg_scale(self):
        imagelist = SafeImageList(self.width, self.height, scale=2)
        imagelist.AddFromFile('testdata/images/example.svg')
        size = imagelist.GetSize(0)
        self.assertEqual(size[0], self.width * 2)
        self.assertEqual(size[1], self.height * 2)
