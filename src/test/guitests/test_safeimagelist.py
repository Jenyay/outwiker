# -*- coding: utf-8 -*-

import wx

from outwiker.gui.controls.safeimagelist import SafeImageList
from test.basetestcases import BaseOutWikerGUITest


class SafeImageListTest(BaseOutWikerGUITest):
    def setUp(self):
        self.initApplication()
        self.width = 16
        self.height = 16
        self.imagelist = SafeImageList(self.width, self.height)

    def tearDown(self):
        self.destroyApplication()

    def _addImage(self, fname):
        bitmap = wx.Bitmap(fname)
        self.imagelist.Add(bitmap)

    def test_16x16(self):
        self._addImage('../test/images/16x16.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_15x15(self):
        self._addImage('../test/images/15x15.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_15x16(self):
        self._addImage('../test/images/15x16.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_16x15(self):
        self._addImage('../test/images/16x15.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_17x16(self):
        self._addImage('../test/images/17x16.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_16x17(self):
        self._addImage('../test/images/16x17.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)

    def test_17x17(self):
        self._addImage('../test/images/17x17.png')
        size = self.imagelist.GetSize(0)
        self.assertEqual(size[0], self.width)
        self.assertEqual(size[1], self.height)
