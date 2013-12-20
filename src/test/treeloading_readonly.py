#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import shutil
import unittest

from outwiker.core.tree import RootWikiPage, WikiDocument
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.event import Event
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style
from outwiker.core.config import StringOption

from outwiker.pages.text.textpage import TextPageFactory, TextWikiPage
from outwiker.pages.wiki.wikipage import WikiPageFactory, WikiWikiPage
from outwiker.pages.html.htmlpage import HtmlPageFactory, HtmlWikiPage
from outwiker.pages.search.searchpage import SearchPageFactory, SearchWikiPage

from test.utils import removeWiki


class ReadonlyLoadTest (unittest.TestCase):
    """
    Тест на открытие вики
    """
    def setUp(self):
        self.path = u"../test/samplewiki"
        self.root = WikiDocument.load (self.path, readonly=True)
        #print self.root


    def testLoadWiki(self):
        self.assertEqual ( len (self.root), 6)
    

    def testPageType1 (self):
        self.assertEqual (type (self.root[u"Типы страниц/HTML-страница"]), HtmlWikiPage)
        self.assertEqual (type (self.root[u"Типы страниц/wiki-страница"]), WikiWikiPage)
        self.assertEqual (type (self.root[u"Типы страниц/Страница поиска"]), SearchWikiPage)
        self.assertEqual (type (self.root[u"Типы страниц/Текстовая страница"]), TextWikiPage)
    

    def testPageType2 (self):
        self.assertEqual (self.root[u"Типы страниц/HTML-страница"].getTypeString(), 
                HtmlWikiPage.getTypeString())

        self.assertEqual (self.root[u"Типы страниц/wiki-страница"].getTypeString(), 
                WikiWikiPage.getTypeString())

        self.assertEqual (self.root[u"Типы страниц/Страница поиска"].getTypeString(), 
                SearchWikiPage.getTypeString())

        self.assertEqual (self.root[u"Типы страниц/Текстовая страница"].getTypeString(), 
                TextWikiPage.getTypeString())


    def testPagesAccess (self):
        """
        Проверка доступа к отдельным страницам и правильности установки заголовков
        """
        self.assertEqual (self.root[u"page 4"].title, u"page 4")
        self.assertEqual (self.root[u"Страница 1"].title, u"Страница 1")
        self.assertEqual (self.root[u"стрАниЦа 3"].title, u"Страница 3")
        self.assertEqual (self.root[u"Страница 1/Страница 2"].title, u"Страница 2")
        self.assertEqual (self.root[u"СтраНица 1/стРаниЦА 2/СтраНицА 5"].title, u"Страница 5")
        self.assertEqual (self.root[u"Страница 1"][u"Страница 2"].title, u"Страница 2")

        self.assertEqual (self.root[u"Страница 111"], None)


    def testPagesParent (self):
        """
        Проверка доступа к отдельным страницам и правильности установки заголовков
        """
        self.assertEqual (self.root[u"page 4"].parent, self.root)
        self.assertEqual (self.root[u"Страница 1"].parent, self.root)
        self.assertEqual (self.root[u"Страница 1/Страница 2"].parent, self.root[u"Страница 1"])
        self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].parent, self.root[u"Страница 1/Страница 2"])

        self.assertEqual (self.root.parent, None)


    def testPagesPath (self):
        """
        Проверка правильности путей до страниц
        """
        self.assertEqual (self.root[u"page 4"].path, os.path.join (self.path, u"page 4") )
        self.assertEqual (self.root[u"Страница 1"].path, os.path.join (self.path, u"Страница 1") )
        self.assertEqual (self.root[u"Страница 3"].path, os.path.join (self.path, u"Страница 3") )

        fullpath = os.path.join (self.path, u"Страница 1")
        fullpath = os.path.join (fullpath, u"Страница 2")

        self.assertEqual (self.root[u"Страница 1/Страница 2"].path, fullpath)



    def testTags (self):
        self.assertTrue (u"тест" in self.root[u"Страница 1"].tags)
        self.assertTrue (u"test" in self.root[u"Страница 1"].tags, self.root[u"Страница 1"].tags)
        self.assertTrue (u"двойной тег" in self.root[u"Страница 1"].tags)
        self.assertEqual (len (self.root[u"Страница 1"].tags), 3)

        self.assertTrue (u"test" in self.root[u"Страница 1/Страница 2"].tags)
        self.assertEqual (len (self.root[u"Страница 1/Страница 2"].tags), 1)

        self.assertTrue (u"test" in self.root[u"Страница 3"].tags)
        self.assertTrue (u"тест" in self.root[u"Страница 3"].tags)
        self.assertEqual (len (self.root[u"Страница 3"].tags), 2)

        self.assertEqual (len (self.root[u"page 4"].tags), 0)


    def testTypes (self):
        self.assertEqual (self.root[u"Страница 1"].getTypeString(), "html")
        self.assertEqual (self.root[u"Страница 1/Страница 2"].getTypeString(), "text")
        self.assertEqual (self.root[u"Страница 3"].getTypeString(), "html")
        self.assertEqual (self.root[u"page 4"].getTypeString(), "text")
        self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].getTypeString(), "text")


    def testChildren (self):
        self.assertEqual (len (self.root[u"Страница 1"].children), 1)
        self.assertEqual (self.root[u"Страница 1"].children[0], self.root[u"Страница 1/Страница 2"])

        self.assertEqual (len (self.root[u"Страница 1/Страница 2"].children), 2)
        self.assertEqual (len (self.root[u"Страница 3"].children), 0)
        self.assertEqual (len (self.root[u"page 4"].children), 0)


    def testIcons (self):
        self.assertEqual (os.path.basename (self.root[u"Страница 1"].icon), "__icon.png")
        self.assertEqual (os.path.basename (self.root[u"Страница 1/Страница 2"].icon), "__icon.gif")
        self.assertEqual (self.root[u"Страница 3"].icon, None)


    def testParams (self):
        typeOption = StringOption (self.root[u"Страница 1"].params, u"General", u"type", u"")
        tagsOption = StringOption (self.root[u"Страница 1"].params, u"General", u"tags", u"")

        self.assertEqual (typeOption.value, u"html")
        self.assertEqual (tagsOption.value, u"Тест, test, двойной тег")
        

    def testGetRoot (self):
        self.assertEqual (self.root[u"Страница 1"].root, self.root)
        self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].root, self.root)
    

    def testSubpath (self):
        self.assertEqual (self.root[u"Страница 1"].subpath, u"Страница 1")

        self.assertEqual (self.root[u"Страница 1/Страница 2/Страница 5"].subpath, 
                u"Страница 1/Страница 2/Страница 5")
    

class ReadonlyChangeTest (unittest.TestCase):
    """
    Тест для проверки перемещения заметок по дереву
    """
    def setUp (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self._exampleStyleDir = u"../styles/example_jblog"
        self._exampleStyleDir2 = u"../styles/example_jnet"

        wiki = WikiDocument.create (self.path)

        TextPageFactory.create (wiki, u"Страница 1", [])
        TextPageFactory.create (wiki, u"Страница 2", [])
        TextPageFactory.create (wiki[u"Страница 2"], u"Страница 3", [])
        TextPageFactory.create (wiki[u"Страница 2/Страница 3"], u"Страница 4", [])
        TextPageFactory.create (wiki[u"Страница 1"], u"Страница 5", [])
        TextPageFactory.create (wiki, u"страница 4", [])

        filesPath = u"../test/samplefiles/"
        files = [u"accept.png", u"add.png", u"anchor.png"]

        fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

        Attachment (wiki[u"Страница 4"]).attach (fullFilesPath)
        Attachment (wiki[u"Страница 1/Страница 5"]).attach (fullFilesPath)

        self.wiki = WikiDocument.load (self.path, readonly=True)
    

    def tearDown(self):
        removeWiki (self.path)


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
        self.assertRaises (ReadonlyException, self.wiki[u"Страница 1/Страница 5"].moveTo, self.wiki)


    def testChangeTitle1 (self):
        self.assertRaises (ReadonlyException, self.__changeTitle, self.wiki[u"Страница 1"], u"Страница 666")


    def testChangeTitle2 (self):
        self.assertRaises (ReadonlyException, self.__changeTitle, self.wiki[u"Страница 2/Страница 3"], u"Страница 666")
    

    def testChangeTags1 (self):
        self.assertRaises (ReadonlyException, self.__changeTags, self.wiki[u"Страница 1"], ["111", "222"])


    def testChangeTags2 (self):
        self.assertRaises (ReadonlyException, self.__changeTags, self.wiki[u"Страница 2/Страница 3"], ["111", "222"])
    

    def testSetParameter1 (self):
        param = StringOption (self.wiki[u"Страница 1"].params, "section", "param", u"")
        param.value = u"value"


    def testSetParameter2 (self):
        param = StringOption (self.wiki[u"Страница 2/Страница 3"].params, "section", "param", u"")
        param.value = u"value"

    
    def testChangeIcon1 (self):
        self.assertRaises (ReadonlyException, self.__changeIcon, self.wiki[u"Страница 1"], u"../test/images/feed.gif")


    def testChangeIcon2 (self):
        self.assertRaises (ReadonlyException, self.__changeIcon, self.wiki[u"Страница 2/Страница 3"], u"../test/images/feed.gif")


    def testAttach1 (self):
        filesPath = u"../test/samplefiles/"
        files = [u"accept.png", u"add.png", u"anchor.png"]

        fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

        self.assertRaises (ReadonlyException, Attachment (self.wiki[u"Страница 1"]).attach, fullFilesPath)
    

    def testAttach2 (self):
        filesPath = u"../test/samplefiles/"
        files = [u"accept.png", u"add.png", u"anchor.png"]

        fullFilesPath = [os.path.join (filesPath, fname) for fname in files]

        self.assertRaises (ReadonlyException, Attachment (self.wiki[u"Страница 2/Страница 3"]).attach, fullFilesPath)


    def testChangeStyle1 (self):
        style = Style ()
        self.assertRaises (ReadonlyException,
            style.setPageStyle, self.wiki[u"Страница 1"], self._exampleStyleDir)
    

    def testChangeStyle2 (self):
        style = Style ()
        self.assertRaises (ReadonlyException,
            style.setPageStyleDefault, self.wiki[u"Страница 1"])
    

    def testRemoveAttach1 (self):
        self.assertRaises (ReadonlyException, Attachment (self.wiki[u"Страница 4"]).removeAttach, u"add.png")
    

    def testRemoveAttach2 (self):
        self.assertRaises (ReadonlyException, Attachment (self.wiki[u"Страница 1/Страница 5"]).removeAttach, u"anchor.png")
    

    def testCreate1 (self):
        self.assertRaises (ReadonlyException, TextPageFactory.create, self.wiki[u"Страница 1"], u"Страница 666", [])


    def testCreate2 (self):
        self.assertRaises (ReadonlyException, TextPageFactory.create, self.wiki[u"Страница 2/Страница 3"], u"Страница 666", [])


    def testChangeContent1 (self):
        self.assertRaises (ReadonlyException, self.__changeContent, self.wiki[u"Страница 1"], u"бла-бла-бла")
    

    def testChangeContent2 (self):
        self.assertRaises (ReadonlyException, self.__changeContent, self.wiki[u"Страница 2/Страница 3"], u"бла-бла-бла")
    

    def testSelectedPage1 (self):
        self.wiki.root.selectedPage = self.wiki[u"Страница 1"]

    
    def testSelectedPage2 (self):
        self.wiki.root.selectedPage = self.wiki[u"Страница 2/Страница 3"]

    
    def testRemove1 (self):
        self.assertRaises (ReadonlyException, self.wiki[u"Страница 1"].remove)
        self.assertNotEqual (self.wiki[u"Страница 1"], None)


    def testRemove2 (self):
        self.assertRaises (ReadonlyException, self.wiki[u"Страница 2/Страница 3"].remove)
        self.assertNotEqual (self.wiki[u"Страница 2/Страница 3"], None)
    

    def testOrder1 (self):
        self.assertRaises (ReadonlyException, self.__changeOrder, self.wiki[u"Страница 1"], 3)

