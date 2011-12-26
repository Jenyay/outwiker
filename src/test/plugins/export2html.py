#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import os.path
import shutil

from outwiker.core.tree import WikiDocument
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class Export2HtmlTest (unittest.TestCase):
    def setUp(self):
        self.outputdir = "../test/temp"
        self.pluginname = u"Export to HTML"

        self.path = u"../test/samplewiki"
        self.root = WikiDocument.load (self.path)
        
        dirlist = [u"../plugins/export2html"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.__removeTempDir()


    def tearDown (self):
        self.__removeTempDir()


    def __removeTempDir (self):
        if os.path.exists (self.outputdir):
            shutil.rmtree (self.outputdir)


    def testLoading (self):
        self.assertEqual (len (self.loader), 1)
        self.loader[self.pluginname]


    def testExportSinglePage (self):
        """
        Тест на создание файлов и страниц
        """
        pagename = u"Страница 1"

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.isfile (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename) ) )
        self.assertTrue (os.path.isdir (os.path.join (self.outputdir, pagename) ) )

    
    def testAttachesSinglePage (self):
        """
        Тест на то, что прикрепленные файлы копируются
        """
        pagename = u"Страница 1"

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "add.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "memirial.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "wall.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "image.tif") ) )


    def testAttachesImagesSinglePage (self):
        """
        Тест на то, что копируются только прикрепленные картинки
        """
        pagename = u"Страница 1"

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "add.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "memirial.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "wall.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "image.tif") ) )


    def testLinkChange (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя
        """

        pagename = u"Страница 1"

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = fp.read()

        self.assertTrue (u'<img src="{pagename}/add.png">'.format (pagename=pagename) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>.'.format (pagename=pagename) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)


    def testFileExists (self):
        """
        Тест на то, что создаваемый файл уже может существовать
        """
        raise NotImplementedError

    
    def testDirExists (self):
        """
        Тест на то, что директория с прикрепленными файлами уже существует
        """
        raise NotImplementedError
