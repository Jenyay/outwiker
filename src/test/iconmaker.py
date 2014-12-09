# -*- coding: UTF-8 -*-

from tempfile import mkdtemp
import unittest
from os.path import join, exists

from PIL import Image

from outwiker.core.iconmaker import IconMaker
from test.utils import removeDir
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT


class IconMakerTest (unittest.TestCase):
    """Tests for IconMaker class"""
    def setUp (self):
        self._tempDir = mkdtemp()


    def tearDown (self):
        removeDir (self._tempDir)


    def test_no_resize_png (self):
        fname_in = u'../test/images/icon.png'
        fname_out = join (self._tempDir, u'result.png')

        iconmaker = IconMaker()
        iconmaker.create (fname_in, fname_out)

        self.assertTrue (exists (fname_out))

        img = Image.open (fname_out)
        self.assertEqual (img.size, (ICON_WIDTH, ICON_HEIGHT))


    def test_overwrite (self):
        fname_in = u'../test/images/icon.png'
        fname_out = join (self._tempDir, u'result.png')

        iconmaker = IconMaker()
        iconmaker.create (fname_in, fname_out)
        iconmaker.create (fname_in, fname_out)

        img = Image.open (fname_out)

        self.assertTrue (exists (fname_out))
        self.assertEqual (img.size, (ICON_WIDTH, ICON_HEIGHT))


    def test_resize (self):
        fnames_in = [
            '../test/images/16x16.png',
            '../test/images/16x8.png',
            '../test/images/8x8.png',
            '../test/images/8x16.png',
            '../test/images/16x15.png',
            '../test/images/16x17.png',
            '../test/images/15x16.png',
            '../test/images/17x16.png',
            '../test/images/15x15.png',
            '../test/images/17x17.png',
            '../test/images/first.png',
            '../test/images/first_vertical.png',
        ]

        fname_out = join (self._tempDir, u'result.png')
        iconmaker = IconMaker()

        for fname in fnames_in:
            iconmaker.create (fname, fname_out)
            img = Image.open (fname_out)

            self.assertTrue (exists (fname_out), fname)
            self.assertEqual (img.size, (ICON_WIDTH, ICON_HEIGHT), fname)
