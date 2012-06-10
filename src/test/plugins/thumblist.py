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

        dirlist = [u"../plugins/thumblist"]

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

        validResult = u"""Бла-бла-бла  бла-бла-бла"""

        result = self.parser.toHtml (text)
        self.assertEqual (validResult, result)


    def testAttachFull1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        бла-бла-бла"""

        files = [u"first.jpg"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (os.path.exists (os.path.join (self.testPage.path, "__attach", "__thumb") ) )


    def testAttachThumbListFull2 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u"image_01.JPG" in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


    def testAttachGalleryFull2 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"__thumb" in result)
        self.assertTrue (u"_first.jpg" in result)

        self.assertTrue (u"image_01.JPG" in result)
        self.assertTrue (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


    def testAttachEmpty1 (self):
        text = u"""Бла-бла-бла 
        (:thumblist:) 
        (:thumblistend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertFalse (u"first.jpg" in result)
        self.assertFalse (u"__thumb" in result)
        self.assertFalse (u"_first.jpg" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


    def testAttachGalleryEmpty1 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery:) 
        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertFalse (u"first.jpg" in result)
        self.assertFalse (u"__thumb" in result)
        self.assertFalse (u"_first.jpg" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


    def testAttachGallerySize1 (self):
        text = u"""Бла-бла-бла 
        (:thumbgallery maxsize=100:) 

            Attach:first.jpg


            Attach:particle_01.PNG


        (:thumbgalleryend:) 
        бла-бла-бла"""

        files = [u"first.jpg", u"image_01.JPG", u"particle_01.PNG", u"image.png", u"html.txt"]
        fullpath = [os.path.join (self.filesPath, fname) for fname in files]
        Attachment(self.testPage).attach (fullpath)

        result = self.parser.toHtml (text)

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)


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

        self.assertTrue (u"first.jpg" in result)
        self.assertTrue (u"maxsize_100_first.jpg" in result)
        self.assertTrue (u"__thumb" in result)

        self.assertTrue (u"particle_01.PNG" in result)
        self.assertTrue ("maxsize_100_particle_01.PNG" in result)

        self.assertFalse (u"image_01.JPG" in result)
        self.assertFalse (u"maxsize_100_image_01.JPG" in result)

        self.assertFalse (u"html.txt" in result)
