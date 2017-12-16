# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.parser.pagethumbmaker import PageThumbmaker
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeDir, getImageSize


class PageThumbmakerTest(unittest.TestCase):
    def setUp(self):
        self.thumbmaker = PageThumbmaker()

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

    def tearDown(self):
        removeDir(self.path)

    def testThumbByWidthJpeg(self):
        images_dir = "../test/images"

        fname_in = "first.jpg"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        newwidth = 250
        newheight = 182

        thumb_fname = self.thumbmaker.createThumbByWidth(page,
                                                         fname_in,
                                                         newwidth)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)

    def testThumbByWidthPng(self):
        images_dir = "../test/images"

        fname_in = "outwiker_1.1.0_02.png"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        newwidth = 250
        newheight = 215

        thumb_fname = self.thumbmaker.createThumbByWidth(page,
                                                         fname_in,
                                                         newwidth)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)

    def testThumbByHeightJpeg(self):
        images_dir = "../test/images"

        fname_in = "first.jpg"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        newwidth = 249
        newheight = 182

        thumb_fname = self.thumbmaker.createThumbByHeight(page,
                                                          fname_in,
                                                          newheight)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)

    def testThumbByHeightPng(self):
        images_dir = "../test/images"

        fname_in = "outwiker_1.1.0_02.png"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        newwidth = 249
        newheight = 215

        thumb_fname = self.thumbmaker.createThumbByHeight(page,
                                                          fname_in,
                                                          newheight)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)

    def testThumbByMaxSizeJpeg1(self):
        images_dir = "../test/images"

        fname_in = "first.jpg"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        maxsize = 250

        newwidth = 250
        newheight = 182

        thumb_fname = self.thumbmaker.createThumbByMaxSize(page,
                                                           fname_in,
                                                           maxsize)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)

    def testThumbByMaxSizeJpeg2(self):
        images_dir = "../test/images"

        fname_in = "first_vertical.jpeg"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        maxsize = 250

        newwidth = 182
        newheight = 250

        thumb_fname = self.thumbmaker.createThumbByMaxSize(page,
                                                           fname_in,
                                                           maxsize)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)

    def testThumbByMaxSizePng(self):
        images_dir = "../test/images"

        fname_in = "outwiker_1.1.0_02.png"
        page = self.wikiroot["Страница 1"]

        Attachment(page).attach([os.path.join(images_dir, fname_in)])

        maxsize = 250

        newwidth = 250
        newheight = 215

        thumb_fname = self.thumbmaker.createThumbByMaxSize(page,
                                                           fname_in,
                                                           maxsize)
        thumb_path = os.path.join(page.path, thumb_fname)

        (width, height) = getImageSize(thumb_path)

        self.assertTrue(os.path.exists(thumb_path), thumb_path)
        self.assertEqual(width, newwidth)
        self.assertEqual(height, newheight)
