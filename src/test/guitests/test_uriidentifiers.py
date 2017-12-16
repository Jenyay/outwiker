# -*- coding: UTF-8 -*-

import os
import os.path
from unittest import TestCase, skipIf
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.core.commands import generateLink

from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.gui.htmlcontrollerie import UriIdentifierIE
from outwiker.gui.htmlcontrollerwebkit import UriIdentifierWebKit

from test.utils import removeDir


class UriIdentifierTest (TestCase):
    """
    Базовый класс для тестов идентификации сслок разными HTML-движками
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        # - Страница 1
        #   - # Страница 5
        #   - Страница 6
        # - Страница 2
        #   - Страница 3
        #     - # Страница 4
        factory = WikiPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create (self.wikiroot["Страница 2/Страница 3"], "# Страница 4", [])
        factory.create (self.wikiroot["Страница 1"], "# Страница 5", [])
        factory.create (self.wikiroot["Страница 1"], "Страница 6", [])
        factory.create (self.wikiroot["Страница 1/# Страница 5"], "Страница 7", [])

        filesPath = "../test/samplefiles/"
        self.files = ["accept.png", "add.png", "anchor.png", "файл с пробелами.tmp", "dir"]
        self.fullFilesPath = [os.path.join (filesPath, fname) for fname in self.files]

        Attachment (self.wikiroot["Страница 1"]).attach (self.fullFilesPath)
        Attachment (self.wikiroot["Страница 1/# Страница 5"]).attach (self.fullFilesPath)

        Application.wikiroot = None


    def tearDown(self):
        Application.wikiroot = None
        removeDir (self.path)



@skipIf (os.name != "nt", 'Test executed under Windows only')
class UriIdentifierIETest (UriIdentifierTest):
    def _getContentFile (self, page):
        """
        Возвращает путь до файла __content.html
        """
        return os.path.join (page.path, PAGE_RESULT_HTML)

    """
    Тесты идентификации ссылок для IE
    """
    def testFindUriHttp (self):
        """
        Тест на распознавание адресов, начинающихся с http
        """
        currentpage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)
        (url, page, filename, anchor) = identifier.identify ("http://jenyay.net")

        self.assertEqual (url, "http://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriHttps (self):
        """
        Тест на распознавание адресов, начинающихся с https
        """
        currentpage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify ("https://jenyay.net")

        self.assertEqual (url, "https://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriFtp (self):
        """
        Тест на распознавание адресов, начинающихся с ftp
        """
        currentpage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify ("ftp://jenyay.net")

        self.assertEqual (url, "ftp://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriMailto (self):
        """
        Тест на распознавание адресов, начинающихся с mailto
        """
        currentpage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify ("mailto://jenyay.net")

        self.assertEqual (url, "mailto://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFullPageLink2 (self):
        """
        Тест на распознавание ссылок на страницы, когда движок IE считает, что это ссылка на файл
        """
        currentpage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)

        (url, page, filename, anchor) = identifier.identify ("x:\\Страница 2\\Страница 3\\# Страница 4")

        self.assertEqual (url, None)
        self.assertEqual (page, self.wikiroot["Страница 2/Страница 3/# Страница 4"])
        self.assertNotEqual (None, page)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testSubpath1 (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на файл.
        """
        wikipage = self.wikiroot["Страница 1"]
        path = os.path.join (wikipage.path, "Страница 6")
        contentfile = self._getContentFile (wikipage)

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, wikipage["Страница 6"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, None)


    def testSubpath2 (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на якорь
        """
        wikipage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (wikipage)

        path = "".join ([self._getContentFile (wikipage), "# Страница 5"])

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, wikipage["# Страница 5"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, "# Страница 5")


    def testSubpath3 (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на якорь
        """
        wikipage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (wikipage)

        path = "".join ([self._getContentFile (wikipage), "# Страница 5", "\\Страница 7"])

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (page, wikipage["# Страница 5/Страница 7"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, "# Страница 5\\Страница 7")


    def testAnchor (self):
        """
        Тест на распознавание ссылок на подстраницы, когда движок IE считает, что это ссылка на якорь
        """
        wikipage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (wikipage)

        path = "".join ([self._getContentFile (wikipage), "# Страница 666"])

        identifier = UriIdentifierIE (wikipage, contentfile)

        (url, page, filename, anchor) = identifier.identify (path)

        self.assertEqual (url, None)
        self.assertEqual (None, page)
        self.assertEqual (anchor, "# Страница 666")



    def testAttachment1 (self):
        """
        Тест на распознавание ссылок на вложенные файлы
        """
        wikipage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (wikipage)
        path = os.path.join (Attachment (wikipage).getAttachPath (), "accept.png")

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
        wikipage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (wikipage)
        identifier = UriIdentifierIE (wikipage, contentfile)
        (url, page, filename, anchor) = identifier.identify (wikipage.path)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, wikipage.path)
        self.assertEqual (anchor, None)


    def testLinkPage_01 (self):
        Application.wikiroot = self.wikiroot
        currentpage = self.wikiroot["Страница 1"]
        contentfile = self._getContentFile (currentpage)
        link = generateLink (Application, currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)
        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testLinkPage_02 (self):
        Application.wikiroot = self.wikiroot
        currentpage = self.wikiroot["Страница 2/Страница 3"]
        contentfile = self._getContentFile (currentpage)
        link = generateLink (Application, currentpage)

        identifier = UriIdentifierIE (currentpage, contentfile)
        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testLinkPage_03 (self):
        Application.wikiroot = self.wikiroot
        currentpage = self.wikiroot["Страница 2/Страница 3"]
        contentfile = self._getContentFile (currentpage)
        link = generateLink (Application, currentpage) + "/#anchor"

        identifier = UriIdentifierIE (currentpage, contentfile)
        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, "#anchor")


@skipIf (os.name == "nt", 'Test executed under Unix only')
class UriIdentifierWebKitTest (UriIdentifierTest):
    """
    Тесты идентификации ссылок для WebKit
    """
    def _getBasePath (self, page):
        """
        Возвращает путь до файла __content.html
        """
        path = "".join (["file://", page.path])
        if path[-1] != "/":
            path += "/"

        return path


    def testFindUriHttp (self):
        """
        Тест на распознавание адресов, начинающихся с http
        """
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify ("http://jenyay.net")

        self.assertEqual (url, "http://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriHttps (self):
        """
        Тест на распознавание адресов, начинающихся с https
        """
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify ("https://jenyay.net")

        self.assertEqual (url, "https://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriFtp (self):
        """
        Тест на распознавание адресов, начинающихся с ftp
        """
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify ("ftp://jenyay.net")

        self.assertEqual (url, "ftp://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFindUriMailto (self):
        """
        Тест на распознавание адресов, начинающихся с mailto
        """
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify ("mailto://jenyay.net")

        self.assertEqual (url, "mailto://jenyay.net")
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testFullPageLink2 (self):
        """
        Тест на распознавание ссылок на страницы по полному пути в вики
        """
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify ("file:///Страница 2/Страница 3/# Страница 4")

        self.assertEqual (url, None)
        self.assertEqual (page, self.wikiroot["Страница 2/Страница 3/# Страница 4"])
        self.assertNotEqual (None, page)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testRelativePageLink1 (self):
        """
        При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
        """
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        link = "file://{0}".format (os.path.join (currentpage.path, "Страница 6"))

        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage["Страница 6"])
        self.assertEqual (page, self.wikiroot["Страница 1/Страница 6"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, None)


    def testRelativePageLink2 (self):
        """
        При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
        """
        currentpage = self.wikiroot["Страница 2"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        link = "file://{0}".format (os.path.join (currentpage.path,
                                                   "Страница 3", "# Страница 4"))

        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, self.wikiroot["Страница 2/Страница 3/# Страница 4"])
        self.assertEqual (page, currentpage["Страница 3/# Страница 4"])
        self.assertNotEqual (None, page)
        self.assertEqual (anchor, None)


    def testAnchor (self):
        """
        При относительной ссылке на вложенную страницу WebKit считает, что ссылаемся на папку страницы
        """
        currentpage = self.wikiroot["Страница 2"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        link = "file://{0}".format (os.path.join (currentpage.path, "# Страница 666"))

        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, "# Страница 666")


    def testAttachment1 (self):
        """
        Тест на распознавание ссылок на вложенные файлы
        """
        wikipage = self.wikiroot["Страница 1"]

        path = os.path.join (Attachment (wikipage).getAttachPath (),
                             "accept.png")

        href = "".join (["file://", path])

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
        currentpage = self.wikiroot["Страница 1"]
        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (currentpage.path)

        self.assertEqual (url, None)
        self.assertEqual (page, None)
        self.assertEqual (filename, currentpage.path)
        self.assertEqual (anchor, None)


    def testLinkPage_01 (self):
        Application.wikiroot = self.wikiroot
        currentpage = self.wikiroot["Страница 1"]
        link = generateLink (Application, currentpage)

        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testLinkPage_02 (self):
        Application.wikiroot = self.wikiroot
        currentpage = self.wikiroot["Страница 2/Страница 3"]
        link = generateLink (Application, currentpage)

        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, None)


    def testLinkPage_03 (self):
        Application.wikiroot = self.wikiroot
        currentpage = self.wikiroot["Страница 2/Страница 3"]
        link = generateLink (Application, currentpage) + "/#anchor"

        identifier = UriIdentifierWebKit (currentpage, self._getBasePath (currentpage))
        (url, page, filename, anchor) = identifier.identify (link)

        self.assertEqual (url, None)
        self.assertEqual (page, currentpage)
        self.assertEqual (filename, None)
        self.assertEqual (anchor, "#anchor")
