# -*- coding: UTF-8 -*-

import os
import os.path
import unittest

from outwiker.core.thumbmakerpil import ThumbmakerPil
from outwiker.core.thumbexception import ThumbException
from test.utils import getImageSize


class ThumbmakerPilTest (unittest.TestCase):
    """
    Тесты для создателя превьюшек с помощью ThumbmakerPil
    """
    def testWxThumbWidthJpeg (self):
        self.fname_in = "../test/images/first.jpg"
        self.fname_out = "../test/images/first_th.jpg"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newwidth = 250
        newheight = 182

        self.thumbmaker.thumbByWidth (self.fname_in, newwidth, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbWidthPng (self):
        self.fname_in = "../test/images/outwiker_1.1.0_02.png"
        self.fname_out = "../test/images/outwiker_1.1.0_02_th.png"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newwidth = 250
        newheight = 215

        self.thumbmaker.thumbByWidth (self.fname_in, newwidth, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbWidthPngJpg (self):
        self.fname_in = "../test/images/outwiker_1.1.0_02.png"
        self.fname_out = "../test/images/outwiker_1.1.0_02_th.jpeg"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newwidth = 250
        newheight = 215

        self.thumbmaker.thumbByWidth (self.fname_in, newwidth, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbWidthTiff (self):
        self.fname_in = "../test/images/outwiker_1.1.0_02.tiff"
        self.fname_out = "../test/images/outwiker_1.1.0_02_th.png"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newwidth = 250
        newheight = 215

        self.thumbmaker.thumbByWidth (self.fname_in, newwidth, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbHeightJpeg (self):
        self.fname_in = "../test/images/first.jpg"
        self.fname_out = "../test/images/first_th.jpg"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newheight = 180
        newwidth = 246

        self.thumbmaker.thumbByHeight (self.fname_in, newheight, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbHeightJpegPng (self):
        self.fname_in = "../test/images/first.jpg"
        self.fname_out = "../test/images/first_th.png"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newheight = 180
        newwidth = 246

        self.thumbmaker.thumbByHeight (self.fname_in, newheight, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbMaxSizeJpeg1 (self):
        self.fname_in = "../test/images/first.jpg"
        self.fname_out = "../test/images/first_th.jpg"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newsize = 250

        newwidth = 250
        newheight = 182

        self.thumbmaker.thumbByMaxSize (self.fname_in, newsize, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testWxThumbMaxSizeJpeg2 (self):
        self.fname_in = "../test/images/first_vertical.jpeg"
        self.fname_out = "../test/images/first_vertical_th.jpg"

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)

        self.thumbmaker = ThumbmakerPil()
        newsize = 250

        newwidth = 182
        newheight = 250

        self.thumbmaker.thumbByMaxSize (self.fname_in, newsize, self.fname_out)
        (width, height) = getImageSize (self.fname_out)

        self.assertEqual (width, newwidth)
        self.assertEqual (height, newheight)

        if os.path.exists (self.fname_out):
            os.remove (self.fname_out)


    def testwxThumbRaises (self):
        self.fname_in = "../test/images/first_vertical_error.jpeg"
        self.fname_out = "../test/images/first_vertical_error_th.jpg"
        newsize = 250

        self.thumbmaker = ThumbmakerPil()

        self.assertRaises (ThumbException, self.thumbmaker.thumbByWidth, self.fname_in, newsize, self.fname_out)
        self.assertRaises (ThumbException, self.thumbmaker.thumbByHeight, self.fname_in, newsize, self.fname_out)
        self.assertRaises (ThumbException, self.thumbmaker.thumbByMaxSize, self.fname_in, newsize, self.fname_out)
