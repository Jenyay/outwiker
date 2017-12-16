# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
from tempfile import mkdtemp

from test.utils import removeDir
from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikiconfig import WikiConfig


class ParserThumbTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.filesPath = "../test/samplefiles/"

        self.pagelinks = ["Страница 1", "/Страница 1", "/Страница 2/Страница 3"]
        self.pageComments = ["Страницо 1", "Страницо 1", "Страницо 3"]

        self.__createWiki()

        factory = ParserFactory()
        self.__wikiconfig = WikiConfig (Application.config)
        self.__wikiconfig.thumbSizeOptions.value = WikiConfig.THUMB_SIZE_DEFAULT

        self.parser = factory.make (self.testPage, Application.config)


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)
        WikiPageFactory().create (self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

        files = ["accept.png", "add.png", "anchor.png", "filename.tmp",
                 "файл с пробелами.tmp", "картинка с пробелами.png",
                 "image.jpg", "image.jpeg", "image.png", "image.tif", "image.tiff", "image.gif",
                 "image_01.JPG", "dir", "dir.xxx", "dir.png", "particle_01.PNG"]

        fullFilesPath = [os.path.join (self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment (self.wikiroot["Страница 2"])

        # Прикрепим к двум страницам файлы
        Attachment (self.testPage).attach (fullFilesPath)


    def tearDown(self):
        self.__wikiconfig.thumbSizeOptions.value = WikiConfig.THUMB_SIZE_DEFAULT
        removeDir (self.path)


    def testThumbWidthJpg (self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_width_100_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbWidthJpg2 (self):
        text = 'бла-бла-бла \nкхм % thumb width = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_width_100_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbWidthJpeg (self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_width_100_image.jpeg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpeg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.jpeg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbWidthGif (self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_width_100_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbWidthPng (self):
        text = 'бла-бла-бла \nкхм % width = 100 px % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_width_100_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_width_100_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbHeightJpg (self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_height_100_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbHeightJpg2 (self):
        text = 'бла-бла-бла \nкхм % thumb height = 100 px % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_height_100_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format(path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbHeightJpeg (self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_height_100_image.jpeg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpeg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.jpeg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbHeightGif (self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_height_100_image.png")
        result = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbHeightPng (self):
        text = 'бла-бла-бла \nкхм % height = 100 px % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_height_100_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_height_100_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbJpg (self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbJpeg (self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.jpeg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.jpeg")
        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpeg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.jpeg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbPng (self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.png")
        result = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbCapitalizeExtension (self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:particle_01.PNG %% бла-бла-бла\nбла-бла-бла'

        path = os.path.join ("__attach", "__thumb", "th_maxsize_250_particle_01.PNG")

        result = 'бла-бла-бла \nкхм <a href="__attach/particle_01.PNG"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(),
                             "__thumb/th_maxsize_250_particle_01.PNG")

        self.assertTrue (os.path.exists (path), path.encode (self.encoding))

    def testThumbGif (self):
        text = 'бла-бла-бла \nкхм % thumb % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_250_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path = path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_250_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbMaxSizeJpg (self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbMaxSizeJpg2 (self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.jpg %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.jpg")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.jpg"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.jpg")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbMaxSizePng (self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.png %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.png"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbMaxSizeGif (self):
        text = 'бла-бла-бла \nкхм % maxsize = 300 % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_300_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path=path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_300_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))


    def testThumbGifDefaultThumb (self):
        self.__wikiconfig.thumbSizeOptions.value = 333

        text = 'бла-бла-бла \nкхм % thumb % Attach:image.gif %% бла-бла-бла\nбла-бла-бла'
        path = os.path.join ("__attach", "__thumb", "th_maxsize_333_image.png")

        result = 'бла-бла-бла \nкхм <a href="__attach/image.gif"><img src="{path}"/></a> бла-бла-бла\nбла-бла-бла'.format (path = path.replace ("\\", "/"))

        self.assertEqual (self.parser.toHtml (text), result, self.parser.toHtml (text).encode (self.encoding))

        path = os.path.join (self.attach_page2.getAttachPath(), "__thumb/th_maxsize_333_image.png")
        self.assertTrue (os.path.exists (path), path.encode (self.encoding))
