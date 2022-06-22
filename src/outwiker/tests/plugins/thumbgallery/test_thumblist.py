# -*- coding: utf-8 -*-

import os.path
import unittest
from pathlib import Path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class ThumbListPluginTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница 1", [])

        self.maxDiff = None
        self.filesPath = "testdata/samplefiles/"

        dirlist = ["plugins/thumbgallery"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

        self.factory = ParserFactory()
        self.parser = self.factory.make(self.testPage, self.application.config)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def testPluginLoad(self):
        self.assertEqual(len(self.loader), 1)

    def testContentParseEmpty(self):
        text = """Бла-бла-бла (:thumblist:) бла-бла-бла"""

        validResult = """Бла-бла-бла <div class="thumblist"></div> бла-бла-бла"""

        result = self.parser.toHtml(text)
        self.assertEqual(validResult, result)
        self.assertTrue("<table" not in result)

    def testAttachFull1(self):
        text = """Бла-бла-бла
        (:thumblist:)
        бла-бла-бла"""

        files = ["first.jpg"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue(
            os.path.exists(os.path.join(self.testPage.path, "__attach", "__thumb"))
        )
        self.assertTrue("<table" not in result)

    def testAttachThumbListFull2(self):
        text = """Бла-бла-бла
        (:thumblist:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGalleryFull2(self):
        text = """Бла-бла-бла
        (:thumbgallery:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachEmpty1(self):
        text = """Бла-бла-бла
        (:thumblist:)
        (:thumblistend:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertFalse('<a href="__attach/first.jpg">' in result)
        self.assertFalse("__thumb" in result)
        self.assertFalse("_first.jpg" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGalleryEmpty1(self):
        text = """Бла-бла-бла
        (:thumbgallery:)
        (:thumbgalleryend:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertFalse('<a href="__attach/first.jpg">' in result)
        self.assertFalse("__thumb" in result)
        self.assertFalse("_first.jpg" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachList1(self):
        text = """Бла-бла-бла
        (:thumblist:)
            first.jpg
            particle_01.PNG
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachList2(self):
        text = """Бла-бла-бла
        (:thumblist:)
            Attach:first.jpg
            Attach:particle_01.PNG
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGalleryList2(self):
        text = """Бла-бла-бла
        (:thumbgallery:)
            Attach:first.jpg
            Attach:particle_01.PNG
        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachList3(self):
        text = """Бла-бла-бла
        (:thumblist:)

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallery3(self):
        text = """Бла-бла-бла
        (:thumbgallery:)

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachList4_singlequotes(self):
        text = """Бла-бла-бла
        (:thumblist:)
            Attach:'first.jpg'
            Attach:'particle_01.PNG'
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallery4_singlequotes(self):
        text = """Бла-бла-бла
        (:thumbgallery:)
            Attach:'first.jpg'
            Attach:'particle_01.PNG'
        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachList5_doublequotes(self):
        text = """Бла-бла-бла
        (:thumblist:)
            Attach:"first.jpg"
            Attach:"particle_01.PNG"
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallery5_doublequotes(self):
        text = """Бла-бла-бла
        (:thumbgallery:)
            Attach:"first.jpg"
            Attach:"particle_01.PNG"
        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallerySpaces1(self):
        text = """Бла-бла-бла
        (:thumbgallery:)

            Attach:first.jpg


            Attach:картинка с пробелами.png


        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
            "картинка с пробелами.png",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue("картинка с пробелами.png" in result)
        self.assertTrue("_картинка с пробелами.png" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallerySpaces2(self):
        text = """Бла-бла-бла
        (:thumbgallery:)

            Attach:first.jpg


            картинка с пробелами.png


        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
            "картинка с пробелами.png",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue("картинка с пробелами.png" in result)
        self.assertTrue("_картинка с пробелами.png" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallerySize1(self):
        text = """Бла-бла-бла
        (:thumbgallery maxsize=100:)

            Attach:first.jpg


            Attach:particle_01.PNG
            Attach:картинка с пробелами.png

        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
            "картинка с пробелами.png",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("maxsize_100_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("maxsize_100_particle_01.PNG" in result)

        self.assertTrue("картинка с пробелами.png" in result)
        self.assertTrue("maxsize_100_картинка с пробелами.png" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("maxsize_100_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachGallerySize2(self):
        text = """Бла-бла-бла
        (:thumbgallery px=100:)

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumbgalleryend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("maxsize_100_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("maxsize_100_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("maxsize_100_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachListSize1(self):
        text = """Бла-бла-бла
        (:thumblist maxsize=100:)

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("maxsize_100_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("maxsize_100_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("maxsize_100_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachListSize2(self):
        text = """Бла-бла-бла
        (:thumblist px=100:)

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("maxsize_100_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("maxsize_100_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("maxsize_100_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachListComments1(self):
        text = """Бла-бла-бла
        (:thumblist px=100:)

            Attach:first.jpg    | Первый


            Attach:particle_01.PNG|Комментарий к картинке


        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("maxsize_100_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("maxsize_100_particle_01.PNG" in result)

        self.assertFalse('<a href="__attach/image_01.JPG">' in result)
        self.assertFalse("maxsize_100_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachListComments2(self):
        text = """Бла-бла-бла
        (:thumblist:)
            Attach:first.jpg    | Первый
            Attach:particle_01.PNG|Комментарий к картинке
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertFalse('<a href="__attach/image_01.JPG">' in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachListComments3_single_quotes(self):
        text = """Бла-бла-бла
        (:thumblist:)
            Attach:'first.jpg'    | Первый
            Attach:'particle_01.PNG'|Комментарий к картинке
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertFalse('<a href="__attach/image_01.JPG">' in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testAttachListComments3_double_quotes(self):
        text = """Бла-бла-бла
        (:thumblist:)
            Attach:"first.jpg"    | Первый
            Attach:"particle_01.PNG"|Комментарий к картинке
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertFalse('<a href="__attach/image_01.JPG">' in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testTable1(self):
        text = """Бла-бла-бла
        (:thumblist cols=2:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue('<a href="__attach/image_01.JPG">' in result)

        self.assertFalse("html.txt" in result)

        self.assertTrue("<table" in result)

        # В таблице две строки
        self.assertEqual(len(result.split("<tr")), 2 + 1)

    def testTable2(self):
        text = """Бла-бла-бла
        (:thumblist cols=1:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "image_01.JPG",
            "particle_01.PNG",
            "image.png",
            "html.txt",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue('<a href="__attach/image_01.JPG">' in result)

        self.assertFalse("html.txt" in result)

        self.assertTrue("<table" in result)

        # В таблице две строки
        self.assertEqual(len(result.split("<tr")), 4 + 1)

    def testInvalidCols1(self):
        text = """Бла-бла-бла
        (:thumblist cols:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testInvalidCols2(self):
        text = """Бла-бла-бла
        (:thumblist cols=:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testInvalidCols3(self):
        text = """Бла-бла-бла
        (:thumblist cols=abyrvalg:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

        self.assertFalse("html.txt" in result)
        self.assertTrue("<table" not in result)

    def testInvalidThumbSizeStream(self):
        text = """Абырвалг
        (:thumblist px=abyrvalg:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)
        self.assertTrue("бла-бла-бла" in result)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

    def testInvalidThumbSizeTable(self):
        text = """Абырвалг
        (:thumblist px=abyrvalg сщды=3:)
        бла-бла-бла"""

        files = ["first.jpg", "image_01.JPG", "html.txt"]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach(fullpath)

        result = self.parser.toHtml(text)
        self.assertTrue("бла-бла-бла" in result)

        self.assertTrue('<a href="__attach/first.jpg">' in result)
        self.assertTrue("__thumb" in result)
        self.assertTrue("_first.jpg" in result)

        self.assertTrue('<a href="__attach/image_01.JPG">' in result)
        self.assertTrue("_image_01.JPG" in result)

    def testSubdir_forwardslash(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            subdir/first.jpg
            subdir/particle_01.PNG
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_forwardslash_comment(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            subdir/first.jpg | Comment
            subdir/particle_01.PNG | Comment
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_backslash(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            subdir\\first.jpg
            subdir\\particle_01.PNG
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_attach_backslash_single_quotes(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            Attach:'subdir\\first.jpg'
            Attach:'subdir\\particle_01.PNG'
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_attach_backslash_double_quotes(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            Attach:"subdir\\first.jpg"
            Attach:"subdir\\particle_01.PNG"
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_attach_forwardslash_single_quotes_comment(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            Attach:'subdir/first.jpg' | Comment
            Attach:'subdir/particle_01.PNG' | Comment
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_attach_forwardslash_single_quotes(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            Attach:'subdir/first.jpg'
            Attach:'subdir/particle_01.PNG'
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_attach_forwardslash_double_quotes(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            Attach:"subdir/first.jpg"
            Attach:"subdir/particle_01.PNG"
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def testSubdir_attach_forwardslash_double_quotes_comments(self):
        subdir = 'subdir'

        text = """Бла-бла-бла
        (:thumblist:)
            Attach:"subdir/first.jpg" | Comment
            Attach:"subdir/particle_01.PNG" | Comment
        (:thumblistend:)
        бла-бла-бла"""

        files = [
            "first.jpg",
            "particle_01.PNG",
        ]
        fullpath = [os.path.join(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.createSubdir(subdir)
        attach.attach(fullpath, subdir)

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/subdir/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/subdir/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb', subdir).exists())

    def test_mask_all_root_single_star(self):
        files = [
            "first.jpg",
            "particle_01.PNG",
            "filename.tmp",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            *
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue("filename.tmp" not in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_all_root_single_star_attach(self):
        files = [
            "first.jpg",
            "particle_01.PNG",
            "filename.tmp",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:*
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue("filename.tmp" not in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_all_root_single_star_attach_single_quotes(self):
        files = [
            "first.jpg",
            "particle_01.PNG",
            "filename.tmp",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:'*'
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue("filename.tmp" not in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_all_root_single_star_attach_double_quotes(self):
        files = [
            "first.jpg",
            "particle_01.PNG",
            "filename.tmp",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:"*"
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue("filename.tmp" not in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_all_root_double_star(self):
        files = [
            "first.jpg",
            "particle_01.PNG",
            "filename.tmp",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            *.*
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue("filename.tmp" not in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_all_root_double_star_attach(self):
        files = [
            "first.jpg",
            "particle_01.PNG",
            "filename.tmp",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:*.*
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/first.jpg">' in result, result)
        self.assertTrue("_first.jpg" in result)
        self.assertTrue("__thumb" in result)

        self.assertTrue('<a href="__attach/particle_01.PNG">' in result)
        self.assertTrue("_particle_01.PNG" in result)

        self.assertTrue("filename.tmp" not in result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_root(self):
        files = [
            "image.png",
            "image_1.png",
            "image_2.png",
            "image.jpg",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            *.png
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/image.png">' in result, result)
        self.assertTrue('<a href="__attach/image_1.png">' in result, result)
        self.assertTrue('<a href="__attach/image_2.png">' in result, result)
        self.assertTrue('<a href="__attach/image.jpg">' not in result, result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_root_attach(self):
        files = [
            "image.png",
            "image_1.png",
            "image_2.png",
            "image.jpg",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:*.png
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/image.png">' in result, result)
        self.assertTrue('<a href="__attach/image_1.png">' in result, result)
        self.assertTrue('<a href="__attach/image_2.png">' in result, result)
        self.assertTrue('<a href="__attach/image.jpg">' not in result, result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_root_attach_single_quotes(self):
        files = [
            "image.png",
            "image_1.png",
            "image_2.png",
            "image.jpg",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:'*.png'
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/image.png">' in result, result)
        self.assertTrue('<a href="__attach/image_1.png">' in result, result)
        self.assertTrue('<a href="__attach/image_2.png">' in result, result)
        self.assertTrue('<a href="__attach/image.jpg">' not in result, result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())

    def test_mask_root_attach_double_quotes(self):
        files = [
            "image.png",
            "image_1.png",
            "image_2.png",
            "image.jpg",
        ]

        fullpath = [Path(self.filesPath, fname) for fname in files]
        attach = Attachment(self.testPage)
        attach.attach(fullpath)
        text = """
        (:thumblist:)
            Attach:"*.png"
        (:thumblistend:)
        """

        result = self.parser.toHtml(text)

        self.assertTrue('<a href="__attach/image.png">' in result, result)
        self.assertTrue('<a href="__attach/image_1.png">' in result, result)
        self.assertTrue('<a href="__attach/image_2.png">' in result, result)
        self.assertTrue('<a href="__attach/image.jpg">' not in result, result)

        self.assertTrue(Path(attach.getAttachPath(), '__thumb').exists())
