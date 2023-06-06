# -*- coding: utf-8 -*-

import os
import os.path
from tempfile import mkdtemp
from unittest import TestCase

from outwiker.api.core.tree import createNotesTree
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerMixin


class ParserThumbTest(BaseOutWikerMixin, TestCase):
    def setUp(self):
        self.initApplication()
        self.encoding = "utf8"

        self.filesPath = "testdata/samplefiles/"
        self.__createWiki()

        factory = ParserFactory()
        self.__wikiconfig = WikiConfig(self.application.config)
        self.__wikiconfig.thumbSizeOptions.value = WikiConfig.THUMB_SIZE_DEFAULT

        self.parser = factory.make(self.testPage, self.application.config)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница 2", [])

        files = ["accept.png", "add.png", "anchor.png",
                 "картинка с пробелами.png",
                 "image.jpg", "image.jpeg", "image.png", "image.tif",
                 "image.tiff", "image.gif", "image_01.JPG", "dir",
                 "dir.png", "particle_01.PNG"]

        fullFilesPath = [os.path.join(self.filesPath, fname)
                         for fname in files]

        self.__attach = Attachment(self.testPage)
        self.__attach.attach(fullFilesPath)

    def tearDown(self):
        self.destroyApplication()
        self.__wikiconfig.thumbSizeOptions.value = WikiConfig.THUMB_SIZE_DEFAULT
        removeDir(self.path)

    def testThumbSimple(self):
        text = '% width = 100 px % Attach:image.jpg %%'
        path = os.path.join("__attach", "__thumb", "th_width_100_image.jpg")

        result_expected = '<a href="__attach/image.jpg"><img src="{path}"/></a>'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(self.__attach.getAttachPath(),
                                       '__thumb', 'th_width_100_image.jpg')

        self.assertEqual(result, result_expected, result)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbSubdirDoubleQuotes(self):
        text = '% width = 100 px % Attach:"dir/attach.png" %%'
        path = os.path.join("__attach", "__thumb", "dir",
                            "th_width_100_attach.png")

        result_expected = '<a href="__attach/dir/attach.png"><img src="{path}"/></a>'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(self.__attach.getAttachPath(),
                                       '__thumb', 'dir', 'th_width_100_attach.png')

        self.assertEqual(result, result_expected, result)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbSubdirSingleQuotes(self):
        text = "% width = 100 px % Attach:'dir/attach.png' %%"
        path = os.path.join("__attach", "__thumb", "dir",
                            "th_width_100_attach.png")

        result_expected = '<a href="__attach/dir/attach.png"><img src="{path}"/></a>'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(self.__attach.getAttachPath(),
                                       '__thumb', 'dir', 'th_width_100_attach.png')

        self.assertEqual(result, result_expected, result)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbWidthJpg(self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_width_100_image.jpg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_width_100_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbWidthJpg2(self):
        text = 'бла-бла-бла \nкхм % thumb width = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_width_100_image.jpg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_width_100_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbWidthJpeg(self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_width_100_image.jpeg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpeg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            '__thumb', 'th_width_100_image.jpeg')

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbWidthGif(self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_width_100_image.png")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_width_100_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbWidthPng(self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_width_100_image.png")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_width_100_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbHeightJpg(self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_height_100_image.jpg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_height_100_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbHeightJpg2(self):
        text = 'бла-бла-бла \nкхм % thumb height = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_height_100_image.jpg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_height_100_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbHeightJpeg(self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_height_100_image.jpeg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpeg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_height_100_image.jpeg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbHeightGif(self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_height_100_image.png")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_height_100_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbHeightPng(self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_height_100_image.png")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_height_100_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbJpg(self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_250_image.jpg")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_maxsize_250_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbJpeg(self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_250_image.jpeg")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpeg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_maxsize_250_image.jpeg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbPng(self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_250_image.png")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_maxsize_250_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbCapitalizeExtension(self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:particle_01.PNG %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join(
            "__attach", "__thumb", "th_maxsize_250_particle_01.PNG")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/particle_01.PNG"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_maxsize_250_particle_01.PNG")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbGif(self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_250_image.png")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_maxsize_250_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbMaxSizeJpg(self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_300_image.jpg")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_maxsize_300_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbMaxSizeJpg2(self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_300_image.jpg")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_maxsize_300_image.jpg")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbMaxSizePng(self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_300_image.png")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_maxsize_300_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbMaxSizeGif(self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_300_image.png")
        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb", "th_maxsize_300_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))

    def testThumbGifDefaultThumb(self):
        self.__wikiconfig.thumbSizeOptions.value = 333
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join("__attach", "__thumb", "th_maxsize_333_image.png")

        result_expected = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(
            path=path.replace("\\", "/"))

        result = self.parser.toHtml(text)

        thumb_path_full = os.path.join(
            self.__attach.getAttachPath(),
            "__thumb/th_maxsize_333_image.png")

        self.assertEqual(result, result_expected)
        self.assertTrue(os.path.exists(thumb_path_full))
