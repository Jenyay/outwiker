# -*- coding: utf-8 -*-

from tempfile import mkdtemp
import unittest
from os.path import join, exists

from PIL import Image

from outwiker.core.iconmaker import IconMaker
from outwiker.tests.utils import removeDir
from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT


class IconMakerTest(unittest.TestCase):
    """Tests for IconMaker class"""

    def setUp(self):
        self._tempDir = mkdtemp()

    def tearDown(self):
        removeDir(self._tempDir)

    def test_no_resize_png(self):
        fname_in = 'testdata/images/icon.png'
        fname_out = join(self._tempDir, 'result.png')

        iconmaker = IconMaker()
        iconmaker.create(fname_in, fname_out)

        self.assertTrue(exists(fname_out))

        img = Image.open(fname_out)
        self.assertEqual(img.size, (ICON_WIDTH, ICON_HEIGHT))

    def test_overwrite(self):
        fname_in = 'testdata/images/icon.png'
        fname_out = join(self._tempDir, 'result.png')

        iconmaker = IconMaker()
        iconmaker.create(fname_in, fname_out)
        iconmaker.create(fname_in, fname_out)

        img = Image.open(fname_out)

        self.assertTrue(exists(fname_out))
        self.assertEqual(img.size, (ICON_WIDTH, ICON_HEIGHT))

    def test_resize(self):
        fnames_in = [
            'testdata/images/16x16.png',
            'testdata/images/16x8.png',
            'testdata/images/8x8.png',
            'testdata/images/8x16.png',
            'testdata/images/16x15.png',
            'testdata/images/16x17.png',
            'testdata/images/15x16.png',
            'testdata/images/17x16.png',
            'testdata/images/15x15.png',
            'testdata/images/17x17.png',
            'testdata/images/first.png',
            'testdata/images/first_vertical.png',
        ]

        fname_out = join(self._tempDir, 'result.png')
        iconmaker = IconMaker()

        for fname in fnames_in:
            iconmaker.create(fname, fname_out)
            img = Image.open(fname_out)

            self.assertTrue(exists(fname_out), fname)
            self.assertEqual(img.size, (ICON_WIDTH, ICON_HEIGHT), fname)
