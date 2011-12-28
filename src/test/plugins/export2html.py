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
        os.mkdir (self.outputdir)


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
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "memorial.gif") ) )
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
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "memorial.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "wall.gif") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "image.tif") ) )


    def testLinkChangeHtml (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на HTML-странице
        """

        pagename = u"Страница 1"

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<img src="{pagename}/add.png" />'.format (pagename=pagename) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>.'.format (pagename=pagename) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)


    def testLinkChangeWiki (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """

        fullpagename = u"Типы страниц/wiki-страница"
        pagename = u"wiki-страница"

        self.loader[self.pluginname].exportPage (page=self.root[fullpagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<img src="{pagename}/add.png" />'.format (pagename=pagename) in text)
        self.assertTrue (u'<a href="{pagename}/wall1.gif">ссылка на файл</a>'.format (pagename=pagename) in text)
        self.assertTrue (u'А этот __attach/ содержится в тексте' in text)


    def testFilesExportTextPage (self):
        """
        Экспорт текстовой страницы
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        self.loader[self.pluginname].exportPage (page=self.root[fullpagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.isfile (os.path.join (self.outputdir, pagename + ".html") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename) ) )
        self.assertTrue (os.path.isdir (os.path.join (self.outputdir, pagename) ) )


    def testAttachesExportTextPage (self):
        """
        Экспорт текстовой страницы
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        self.loader[self.pluginname].exportPage (page=self.root[fullpagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "anchor.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "application.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "box.png") ) )


    def testHtmlFromTextPage (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """

        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        self.loader[self.pluginname].exportPage (page=self.root[fullpagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'&lt;a href="http://jenyay.net"&gt;bla-bla-bla&lt;/a&gt;' in text)


    def testTextTemplate (self):
        """
        Тест на то, что ссылки на прикрепленные файлы изменяютcя.
        Проверка на вики-странице
        """

        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        self.loader[self.pluginname].exportPage (page=self.root[fullpagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        text = u""

        with open (os.path.join (self.outputdir, pagename + ".html") ) as fp:
            text = unicode (fp.read(), "utf8")

        self.assertTrue (u'<head>' in text)
        self.assertTrue (u'</head>' in text)
        self.assertTrue (u'<body>' in text)
        self.assertTrue (u'</body>' in text)
        self.assertTrue (u'<pre>' in text)
        self.assertTrue (u'</pre>' in text)
        self.assertTrue (u'Текстовая страница' in text)


    def testAttachesImagesExportTextPage (self):
        """
        Экспорт текстовой страницы
        """
        fullpagename = u"Типы страниц/Текстовая страница"
        pagename = u"Текстовая страница"

        self.loader[self.pluginname].exportPage (page=self.root[fullpagename], 
                outdir = self.outputdir,
                imagesonly=True,
                ignoreerrors=False)

        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "__init__.py") ) )
        self.assertFalse (os.path.exists (os.path.join (self.outputdir, pagename, "source.py") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "anchor.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "application.png") ) )
        self.assertTrue (os.path.exists (os.path.join (self.outputdir, pagename, "box.png") ) )


    def testFileExists (self):
        """
        Тест на то, что создаваемый файл уже может существовать
        """
        pagename = u"Страница 1"

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.assertRaises (BaseException, 
                self.loader[self.pluginname].exportPage, 
                page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=True)

    
    def testDirExists (self):
        """
        Тест на то, что директория с прикрепленными файлами уже существует
        """
        raise NotImplementedError


    def testInvalidFormat (self):
        """
        Проверка на попытку экспортировать страницу, которая не может быть сохранена в HTML (страница поиска)
        """
        pagename = u"Типы страниц/Страница поиска"

        self.assertRaises (BaseException, 
                self.loader[self.pluginname].exportPage, 
                page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=False)

        self.loader[self.pluginname].exportPage (page=self.root[pagename], 
                outdir = self.outputdir,
                imagesonly=False,
                ignoreerrors=True)


    def testHtmlNotFound (self):
        """
        Проверка на случай, если нет сформированного HTML-а
        """
