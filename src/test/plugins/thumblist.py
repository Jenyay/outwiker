#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.htmlgenerator import HtmlGenerator
from test.utils import removeWiki


class ThumbListPluginTest (unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.encoding = "utf8"

        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/thumbgallery"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        
        self.factory = ParserFactory()
        self.parser = self.factory.make (self.testPage, Application.config)
    

    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]
        

    def tearDown(self):
        removeWiki (self.path)
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual ( len (self.loader), 1)


    def testContentParseEmpty (self):
        text = u"""Бла-бла-бла (:thumblist:) бла-бла-бла"""

        validResult = u"""Бла-бла-бла <div class="thumblist"></div> бла-бла-бла"""

        result = self.parser.toHtml (text)
        self.assertEqual (validResult, result)
        self.assertTrue (u"<table" not in result)


    def testAttachFull1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        бла-бла-бла"""

        files = [u"first.jpg"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (os.path.exists (os.path.join (self.testPage.path, "__attach", "__thumb") ) )
        self.assertTrue (u"<table" not in result)


    def testAttachThumbListFull2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGalleryFull2 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachEmpty1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertFalse (u'<A HREF="__attach/first.jpg">' in result)
        self.assertFalse (u"__thumb" in result)
        self.assertFalse (u"_first.jpg" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGalleryEmpty1 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 
        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertFalse (u'<A HREF="__attach/first.jpg">' in result)
        self.assertFalse (u"__thumb" in result)
        self.assertFalse (u"_first.jpg" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachList1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
            first.jpg
            particle_01.PNG
        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachList2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
            Attach:first.jpg
            Attach:particle_01.PNG
        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGalleryList2 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 
            Attach:first.jpg
            Attach:particle_01.PNG
        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachList3 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGallery3 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGallerySpaces1 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 

            Attach:first.jpg


            Attach:картинка с пробелами.png


        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt", u"картинка с пробелами.png"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"картинка с пробелами.png" in result)
        self.assertTrue (u"_картинка с пробелами.png" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGallerySpaces2 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 

            Attach:first.jpg


            картинка с пробелами.png


        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt", u"картинка с пробелами.png"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"картинка с пробелами.png" in result)
        self.assertTrue (u"_картинка с пробелами.png" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGallerySize1 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery maxsize=100:) 

            Attach:first.jpg


            Attach:particle_01.PNG
            Attach:картинка с пробелами.png

        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt", u"картинка с пробелами.png"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertTrue (u"картинка с пробелами.png" in result)
        self.assertTrue (u"maxsize_100_картинка с пробелами.png" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachGallerySize2 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery px=100:) 

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachListSize1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist maxsize=100:) 

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachListSize2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist px=100:) 

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachListComments1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist px=100:) 

            Attach:first.jpg    | Первый


            Attach:particle_01.PNG|Комментарий к картинке


        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testAttachListComments2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
            Attach:first.jpg    | Первый
            Attach:particle_01.PNG|Комментарий к картинке
        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertFalse (u'<A HREF="__attach/image_01.JPG">' in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testTable1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist cols=2:)
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)

        self.assertFalse (u"html.txt" in result)

        self.assertTrue (u"<table" in result)

        # В таблице две строки
        self.assertEqual (len (result.split ("<tr") ), 2 + 1)


    def testTable2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist cols=1:)
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u'<A HREF="__attach/particle_01.PNG">' in result)
        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)

        self.assertFalse (u"html.txt" in result)

        self.assertTrue (u"<table" in result)

        # В таблице две строки
        self.assertEqual (len (result.split ("<tr") ), 4 + 1)


    def testInvalidCols1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist cols:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testInvalidCols2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist cols=:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)


    def testInvalidCols3 (self):
        text = u"""Бла-бла-бла 
        (:thumblist cols=abyrvalg:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u'<A HREF="__attach/first.jpg">' in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u'<A HREF="__attach/image_01.JPG">' in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
        self.assertTrue (u"<table" not in result)

