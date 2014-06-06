#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory, WikiWikiPage
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from test.utils import removeWiki

from outwiker.gui.htmlcontrollerie import UriIdentifierIE
from outwiker.gui.htmlcontrollerwebkit import UriIdentifierWebKit


class UriIdentifierTest (unittest.TestCase):
    """
    Базовый класс для тестов идентификации сслок разными HTML-движками
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = os.path.realpath (u"../test/testwiki")
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        # - Страница 1
        #   - # Страница 5
        #   - Страница 6
        # - Страница 2
        #   - Страница 3
        #     - # Страница 4
        WikiPageFactory.create (self.rootwiki, u"Страница 1", [])
        WikiPageFactory.create (self.rootwiki, u"Страница 2", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 2/Страница 3"], u"# Страница 4", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"# Страница 5", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1"], u"Страница 6", [])
        WikiPageFactory.create (self.rootwiki[u"Страница 1/# Страница 5"], u"Страница 7", [])

        filesPath = u"../test/samplefiles/"
        self.files = [u"accept.png", u"add.png", u"anchor.png", u"файл с пробелами.tmp", u"dir"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]

        Attachment (self.rootwiki[u"Страница 1"]).attach (self.fullFilesPath)
        Attachment (self.rootwiki[u"Страница 1/# Страница 5"]).attach (self.fullFilesPath)

        Application.wikiroot = None


    def tearDown(self):
        Application.wikiroot = None
        removeWiki (self.path)



class UriIdentifierIETest (UriIdentifierTest):
    def _getContentFile (self, page):
        """
        Возвращает путь до файла __content.html
        """
        return os.path.join (page.path, u"__content.html")

    """
    Тесты идентификации ссылок для IE
    """
    def testFindUriHttp (self):
        """
        Тест на распознавание адресов, начинающихся с http
        """
        currentpage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)
        (url, page, filename, anchor) = identifier.identify (u"http://jenyay.net")

        self.assertEqual (url, u"http://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriHttps (self):
        """
        Тест на распознавание адресов, начинающихся с https
        """
        currentpage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify (u"https://jenyay.net")

        self.assertEqual (url, u"https://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriFtp (self):
        """
        Тест на распознавание адресов, начинающихся с ftp
        """
        currentpage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify (u"ftp://jenyay.net")

        self.assertEqual (url, u"ftp://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriMailto (self):
        """
        Тест на распознавание адресов, начинающихся с mailto
        """
        currentpage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify (u"mailto://jenyay.net")

        self.assertEqual (url, u"mailto://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFullPageLink2 (self):
        """
        Тест на распознавание ссылок на страницы, когда движок IE считает, что это ссылка на файл
        """
        currentpage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify (u"x:\\Страница 2\\Страница 3\\# Страница 4")

        self.assertEqual (url, None)
        self.assertEqual (page, self.rootwiki[u"Страница 2/Страница 3/# Страница 4"])
        self.assertNotEqual (None, page)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testSubpath1 (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на файл. 
        """
        wikipage = self.rootwiki[u"Страница 1"]
        path = os.path.join (wikipage.path, u"Страница 6")
        contentfile = self._getContentFile (wikipage)

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, wikipage[u"Страница 6"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, None)


    def testSubpath2 (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на якорь
        """
        wikipage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (wikipage)

        path = u"".join ([self._getContentFile (wikipage), u"# Страница 5"])

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, wikipage[u"# Страница 5"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, u"# Страница 5")


    def testSubpath3 (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на якорь
        """
        wikipage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (wikipage)

        path = u"".join ([self._getContentFile (wikipage), u"# Страница 5", u"\\Страница 7"])

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, wikipage[u"# Страница 5/Страница 7"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, u"# Страница 5\\Страница 7")


    def testAnchor (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на якорь
        """
        wikipage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (wikipage)

        path = u"".join ([self._getContentFile (wikipage), u"# Страница 666"])

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (None, page)
        self.assertEqual (anchor, u"# Страница 666")



    def testAttachment1 (self):
        """
        Тест на распознавание ссылок на вложенные файлы
        """
        wikipage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (wikipage)
        path = os.path.join (Attachment (wikipage).getAttachPath (), u"accept.png")

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, path)
        self.assertNotEqual (None, path)
        self.assertEqual (anchor, None)


    def testLinkPath (self):
        """
        Тест на распознавание ссылок на страницы по полному пути в вики
        """
        wikipage = self.rootwiki[u"Страница 1"]
        contentfile = self._getContentFile (wikipage)
        identifier = UriIdentifierIE (wikipage, contentfile)
        (url, page, filename, anchor) = identifier.identify (wikipage.path)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, wikipage.path)
        self.assertEqual (anchor, None)


class UriIdentifierWebKitTest (UriIdentifierTest):
    """
    Тесты идентификации ссылок для WebKit
    """
    def _getBasePath (self, page):
        """
        Возвращает путь до файла __content.html
        """
        path = u"".join ([u"file://", page.path])
        if path[-1] != "/":
            path += "/"

        return path

    
    def testFindUriHttp (self):
        """
        Тест на распознавание адресов, начинающихся с http
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (u"http://jenyay.net")

        self.assertEqual (url, u"http://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriHttps (self):
        """
        Тест на распознавание адресов, начинающихся с https
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (u"https://jenyay.net")

        self.assertEqual (url, u"https://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriFtp (self):
        """
        Тест на распознавание адресов, начинающихся с ftp
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (u"ftp://jenyay.net")

        self.assertEqual (url, u"ftp://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriMailto (self):
        """
        Тест на распознавание адресов, начинающихся с mailto
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (u"mailto://jenyay.net")

        self.assertEqual (url, u"mailto://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFullPageLink2 (self):
        """
        Тест на распознавание ссылок на страницы по полному пути в вики
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (u"file:///Страница 2/Страница 3/# Страница 4")

        self.assertEqual (url, None)
        self.assertEqual (page, self.rootwiki[u"Страница 2/Страница 3/# Страница 4"])
        self.assertNotEqual (None, page)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testRelativePageLink1 (self):
        """
        При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        link = u"file://{0}".format (os.path.join (currentpage.path, u"Страница 6") )

        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage[u"Страница 6"])
        self.assertEqual (page, self.rootwiki[u"Страница 1/Страница 6"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, None)


    def testRelativePageLink2 (self):
        """
        При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
        """
        currentpage = self.rootwiki[u"Страница 2"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        link = u"file://{0}".format (os.path.join (currentpage.path, 
            u"Страница 3", u"# Страница 4") )

        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, self.rootwiki[u"Страница 2/Страница 3/# Страница 4"])
        self.assertEqual (page, currentpage[u"Страница 3/# Страница 4"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, None)


    def testAnchor (self):
        """
        При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
        """
        currentpage = self.rootwiki[u"Страница 2"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        link = u"file://{0}".format (os.path.join (currentpage.path, u"# Страница 666") )

        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, u"# Страница 666")


    def testAttachment1 (self):
        """
        Тест на распознавание ссылок на вложенные файлы
        """
        wikipage = self.rootwiki[u"Страница 1"]

        path = os.path.join (Attachment (wikipage).getAttachPath (), 
                u"accept.png")

        href = "".join ([u"file://", path] )

        identifier = UriIdentifierWebKit (wikipage, self._getBasePath (wikipage))

        (url, page, filename, anchor) = identifier.identify (href)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, path)
        self.assertEqual (anchor, None)


    def testLinkPath (self):
        """
        Тест на распознавание ссылок на страницы по полному пути в вики
        """
        currentpage = self.rootwiki[u"Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (currentpage.path)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, currentpage.path)
        self.assertEqual (anchor, None)
