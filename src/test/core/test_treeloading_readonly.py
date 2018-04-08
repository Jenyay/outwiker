# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style
from outwiker.core.config import StringOption

from outwiker.pages.text.textpage import TextPageFactory, TextWikiPage
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.html.htmlpage import HtmlWikiPage
from outwiker.pages.search.searchpage import SearchWikiPage

from test.utils import removeDir


class ReadonlyLoadTest (unittest.TestCase):
    """
    Тест на открытие вики
    """
    def setUp(self):
        self.path = "../test/samplewiki"
        self.root = WikiDocument.load (self.path, readonly=True)


    def testLoadWiki(self):
        self.assertEqual (len (self.root), 6)


    def testPageType1 (self):
        self.assertEqual (type (self.root["Типы страниц/HTML-страница"]), HtmlWikiPage)
        self.assertEqual (type (self.root["Типы страниц/wiki-страница"]), WikiWikiPage)
        self.assertEqual (type (self.root["Типы страниц/Страница поиска"]), SearchWikiPage)
        self.assertEqual (type (self.root["Типы страниц/Текстовая страница"]), TextWikiPage)


    def testPageType2 (self):
        self.assertEqual (self.root["Типы страниц/HTML-страница"].getTypeString(),
                          HtmlWikiPage.getTypeString())

        self.assertEqual (self.root["Типы страниц/wiki-страница"].getTypeString(),
                          WikiWikiPage.getTypeString())

        self.assertEqual (self.root["Типы страниц/Страница поиска"].getTypeString(),
                          SearchWikiPage.getTypeString())

        self.assertEqual (self.root["Типы страниц/Текстовая страница"].getTypeString(),
                          TextWikiPage.getTypeString())


    def testPagesAccess (self):
        """
        Проверка доступа к отдельным страницам и правильности установки заголовков
        """
        self.assertEqual (self.root["page 4"].title, "page 4")
        self.assertEqual (self.root["Страница 1"].title, "Страница 1")
        self.assertEqual (self.root["стрАниЦа 3"].title, "Страница 3")
        self.assertEqual (self.root["Страница 1/Страница 2"].title, "Страница 2")
        self.assertEqual (self.root["СтраНица 1/стРаниЦА 2/СтраНицА 5"].title, "Страница 5")
        self.assertEqual (self.root["Страница 1"]["Страница 2"].title, "Страница 2")

        self.assertEqual (self.root["Страница 111"], None)


    def testPagesParent (self):
        """
        Проверка доступа к отдельным страницам и правильности установки заголовков
        """
        self.assertEqual (self.root["page 4"].parent, self.root)
        self.assertEqual (self.root["Страница 1"].parent, self.root)
        self.assertEqual (self.root["Страница 1/Страница 2"].parent, self.root["Страница 1"])
        self.assertEqual (self.root["Страница 1/Страница 2/Страница 5"].parent, self.root["Страница 1/Страница 2"])

        self.assertEqual (self.root.parent, None)


    def testPagesPath (self):
        """
        Проверка правильности путей до страниц
        """
        self.assertEqual (self.root["page 4"].path, os.path.join (self.path, "page 4"))
        self.assertEqual (self.root["Страница 1"].path, os.path.join (self.path, "Страница 1"))
        self.assertEqual (self.root["Страница 3"].path, os.path.join (self.path, "Страница 3"))

        fullpath = os.path.join (self.path, "Страница 1")
        fullpath = os.path.join (fullpath, "Страница 2")

        self.assertEqual (self.root["Страница 1/Страница 2"].path, fullpath)



    def testTags (self):
        self.assertTrue ("тест" in self.root["Страница 1"].tags)
        self.assertTrue ("test" in self.root["Страница 1"].tags, self.root["Страница 1"].tags)
        self.assertTrue ("двойной тег" in self.root["Страница 1"].tags)
        self.assertEqual (len (self.root["Страница 1"].tags), 3)

        self.assertTrue ("test" in self.root["Страница 1/Страница 2"].tags)
        self.assertEqual (len (self.root["Страница 1/Страница 2"].tags), 1)

        self.assertTrue ("test" in self.root["Страница 3"].tags)
        self.assertTrue ("тест" in self.root["Страница 3"].tags)
        self.assertEqual (len (self.root["Страница 3"].tags), 2)

        self.assertEqual (len (self.root["page 4"].tags), 0)


    def testTypes (self):
        self.assertEqual (self.root["Страница 1"].getTypeString(), "html")
        self.assertEqual (self.root["Страница 1/Страница 2"].getTypeString(), "text")
        self.assertEqual (self.root["Страница 3"].getTypeString(), "html")
        self.assertEqual (self.root["page 4"].getTypeString(), "text")
        self.assertEqual (self.root["Страница 1/Страница 2/Страница 5"].getTypeString(), "text")


    def testChildren (self):
        self.assertEqual (len (self.root["Страница 1"].children), 1)
        self.assertEqual (self.root["Страница 1"].children[0], self.root["Страница 1/Страница 2"])

        self.assertEqual (len (self.root["Страница 1/Страница 2"].children), 2)
        self.assertEqual (len (self.root["Страница 3"].children), 0)
        self.assertEqual (len (self.root["page 4"].children), 0)


    def testIcons (self):
        self.assertEqual (os.path.basename (self.root["Страница 1"].icon), "__icon.png")
        self.assertEqual (os.path.basename (self.root["Страница 1/Страница 2"].icon), "__icon.gif")
        self.assertEqual (self.root["Страница 3"].icon, None)


    def testParams (self):
        typeOption = StringOption (self.root["Страница 1"].params, "General", "type", "")
        tagsOption = StringOption (self.root["Страница 1"].params, "General", "tags", "")

        self.assertEqual (typeOption.value, "html")
        self.assertEqual (tagsOption.value, "Тест, test, двойной тег")


    def testGetRoot (self):
        self.assertEqual (self.root["Страница 1"].root, self.root)
        self.assertEqual (self.root["Страница 1/Страница 2/Страница 5"].root, self.root)


    def testSubpath (self):
        self.assertEqual (self.root["Страница 1"].subpath, "Страница 1")

        self.assertEqual (self.root["Страница 1/Страница 2/Страница 5"].subpath,
                          "Страница 1/Страница 2/Страница 5")


class ReadonlyChangeTest (unittest.TestCase):
    """
    Тест для проверки перемещения заметок по дереву
    """
    def setUp (self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self._exampleStyleDir = "../styles/example_jblog"
        self._exampleStyleDir2 = "../styles/example_jnet"

        wiki = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (wiki, "Страница 1", [])
        factory.create (wiki, "Страница 2", [])
        factory.create (wiki["Страница 2"], "Страница 3", [])
        factory.create (wiki["Страница 2/Страница 3"], "Страница 4", [])
        factory.create (wiki["Страница 1"], "Страница 5", [])
        factory.create (wiki, "страница 4", [])

        filesPath = "../test/samplefiles/"
        files = ["accept.png", "add.png", "anchor.png"]

        fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

        Attachment (wiki["Страница 4"]).attach (fullFilesPath)
        Attachment (wiki["Страница 1/Страница 5"]).attach (fullFilesPath)

        self.wiki = WikiDocument.load (self.path, readonly=True)


    def tearDown(self):
        removeDir (self.path)


    def __changeTitle (self, page, newtitle):
        page.title = newtitle


    def __changeTags (self, page, newtags):
        page.tags = newtags


    def __changeIcon (self, page, newicon):
        page.icon = newicon

    def __changeContent (self, page, newcontent):
        page.content = newcontent


    def __changeOrder (self, page, neworder):
        page.order = neworder


    def testMoveTo (self):
        self.assertRaises (ReadonlyException, self.wiki["Страница 1/Страница 5"].moveTo, self.wiki)


    def testChangeTitle1 (self):
        self.assertRaises (ReadonlyException, self.__changeTitle, self.wiki["Страница 1"], "Страница 666")


    def testChangeTitle2 (self):
        self.assertRaises (ReadonlyException, self.__changeTitle, self.wiki["Страница 2/Страница 3"], "Страница 666")


    def testChangeTags1 (self):
        self.assertRaises (ReadonlyException, self.__changeTags, self.wiki["Страница 1"], ["111", "222"])


    def testChangeTags2 (self):
        self.assertRaises (ReadonlyException, self.__changeTags, self.wiki["Страница 2/Страница 3"], ["111", "222"])


    def testSetParameter1 (self):
        param = StringOption (self.wiki["Страница 1"].params, "section", "param", "")
        param.value = "value"


    def testSetParameter2 (self):
        param = StringOption (self.wiki["Страница 2/Страница 3"].params, "section", "param", "")
        param.value = "value"


    def testChangeIcon1 (self):
        self.assertRaises (ReadonlyException, self.__changeIcon, self.wiki["Страница 1"], "../test/images/feed.gif")


    def testChangeIcon2 (self):
        self.assertRaises (ReadonlyException, self.__changeIcon, self.wiki["Страница 2/Страница 3"], "../test/images/feed.gif")


    def testAttach1 (self):
        filesPath = "../test/samplefiles/"
        files = ["accept.png", "add.png", "anchor.png"]

        fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

        self.assertRaises (ReadonlyException, Attachment (self.wiki["Страница 1"]).attach, fullFilesPath)


    def testAttach2 (self):
        filesPath = "../test/samplefiles/"
        files = ["accept.png", "add.png", "anchor.png"]

        fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

        self.assertRaises (ReadonlyException, Attachment (self.wiki["Страница 2/Страница 3"]).attach, fullFilesPath)


    def testChangeStyle1 (self):
        style = Style ()
        self.assertRaises (ReadonlyException,
                           style.setPageStyle, self.wiki["Страница 1"], self._exampleStyleDir)


    def testChangeStyle2 (self):
        style = Style ()
        self.assertRaises (ReadonlyException,
                           style.setPageStyleDefault, self.wiki["Страница 1"])


    def testRemoveAttach1 (self):
        self.assertRaises (ReadonlyException, Attachment (self.wiki["Страница 4"]).removeAttach, "add.png")


    def testRemoveAttach2 (self):
        self.assertRaises (ReadonlyException, Attachment (self.wiki["Страница 1/Страница 5"]).removeAttach, "anchor.png")


    def testCreate1 (self):
        self.assertRaises (ReadonlyException, TextPageFactory().create, self.wiki["Страница 1"], "Страница 666", [])


    def testCreate2 (self):
        self.assertRaises (ReadonlyException, TextPageFactory().create, self.wiki["Страница 2/Страница 3"], "Страница 666", [])


    def testChangeContent1 (self):
        self.assertRaises (ReadonlyException, self.__changeContent, self.wiki["Страница 1"], "бла-бла-бла")


    def testChangeContent2 (self):
        self.assertRaises (ReadonlyException, self.__changeContent, self.wiki["Страница 2/Страница 3"], "бла-бла-бла")


    def testSelectedPage1 (self):
        self.wiki.root.selectedPage = self.wiki["Страница 1"]


    def testSelectedPage2 (self):
        self.wiki.root.selectedPage = self.wiki["Страница 2/Страница 3"]


    def testRemove1 (self):
        self.assertRaises (ReadonlyException, self.wiki["Страница 1"].remove)
        self.assertNotEqual (self.wiki["Страница 1"], None)


    def testRemove2 (self):
        self.assertRaises (ReadonlyException, self.wiki["Страница 2/Страница 3"].remove)
        self.assertNotEqual (self.wiki["Страница 2/Страница 3"], None)


    def testOrder1 (self):
        self.assertRaises (ReadonlyException, self.__changeOrder, self.wiki["Страница 1"], 3)
