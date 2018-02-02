# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.core.config import StringOption

from outwiker.pages.text.textpage import TextPageFactory, TextWikiPage
from outwiker.pages.wiki.wikipage import WikiWikiPage
from outwiker.pages.html.htmlpage import HtmlWikiPage
from outwiker.pages.search.searchpage import SearchWikiPage

from test.utils import removeDir


class WikiPagesTest(unittest.TestCase):
    """
    Тест на открытие вики
    """
    def setUp(self):
        self.path = "../test/samplewiki"
        self.root = WikiDocument.load(self.path)

    def testLoadWiki(self):
        self.assertEqual(len(self.root), 6)

    def testInvalidEncoding(self):
        self.root["invalid encoding"].content
        self.assertEqual(len(self.root["invalid encoding"].tags), 1)

    def testPagesAccess(self):
        """
        Проверка доступа к отдельным страницам и
        правильности установки заголовков
        """
        self.assertEqual(self.root["page 4"].title,
                         "page 4")

        self.assertEqual(self.root["Страница 1"].title,
                         "Страница 1")

        self.assertEqual(self.root["стрАниЦа 3"].title,
                         "Страница 3")

        self.assertEqual(self.root["Страница 1/Страница 2"].title,
                         "Страница 2")

        self.assertEqual(self.root["СтраНица 1/стРаниЦА 2/СтраНицА 5"].title,
                         "Страница 5")

        self.assertEqual(self.root["Страница 1"]["Страница 2"].title,
                         "Страница 2")

        self.assertEqual(self.root["Страница 111"], None)
        self.assertEqual(self.root["/"], self.root)

    def testPageAccess2(self):
        self.assertEqual(self.root["Страница 1"]["Страница 2"],
                         self.root["Страница 1/Страница 2"])

        self.assertEqual(self.root["СтраНица 1"]["стРаниЦА 2/СтраНицА 5"],
                         self.root["СтраНица 1/стРаниЦА 2/СтраНицА 5"])

    def testPageAccess3(self):
        self.assertEqual(self.root["Страница 1"]["/Страница 1/Страница 2"],
                         self.root["Страница 1/Страница 2"])

        self.assertEqual(self.root["СтраНица 1"]["/СтраНица 1/стРаниЦА 2/СтраНицА 5"],
                         self.root["СтраНица 1/стРаниЦА 2/СтраНицА 5"])

    def testAccessRoot(self):
        self.assertEqual(self.root["Страница 1"]["/"], self.root)

    def testPageType1(self):
        self.assertEqual(type(self.root["Типы страниц/HTML-страница"]),
                         HtmlWikiPage)

        self.assertEqual(type(self.root["Типы страниц/wiki-страница"]),
                         WikiWikiPage)

        self.assertEqual(type(self.root["Типы страниц/Страница поиска"]),
                         SearchWikiPage)

        self.assertEqual(type(self.root["Типы страниц/Текстовая страница"]),
                         TextWikiPage)

    def testPageType2(self):
        self.assertEqual(self.root["Типы страниц/HTML-страница"].getTypeString(),
                         HtmlWikiPage.getTypeString())

        self.assertEqual(self.root["Типы страниц/wiki-страница"].getTypeString(),
                         WikiWikiPage.getTypeString())

        self.assertEqual(self.root["Типы страниц/Страница поиска"].getTypeString(),
                         SearchWikiPage.getTypeString())

        self.assertEqual(self.root["Типы страниц/Текстовая страница"].getTypeString(),
                         TextWikiPage.getTypeString())

    def testPagesParent(self):
        """
        Проверка доступа к отдельным страницам и правильности установки заголовков
        """
        self.assertEqual(self.root["page 4"].parent, self.root)
        self.assertEqual(self.root["Страница 1"].parent, self.root)
        self.assertEqual(self.root["Страница 1/Страница 2"].parent, self.root["Страница 1"])
        self.assertEqual(self.root["Страница 1/Страница 2/Страница 5"].parent, self.root["Страница 1/Страница 2"])

        self.assertEqual(self.root.parent, None)

    def testPagesPath(self):
        """
        Проверка правильности путей до страниц
        """
        self.assertEqual(self.root["page 4"].path, os.path.join(self.path, "page 4"))
        self.assertEqual(self.root["Страница 1"].path, os.path.join(self.path, "Страница 1"))
        self.assertEqual(self.root["Страница 3"].path, os.path.join(self.path, "Страница 3"))

        fullpath = os.path.join(self.path, "Страница 1")
        fullpath = os.path.join(fullpath, "Страница 2")

        self.assertEqual(self.root["Страница 1/Страница 2"].path, fullpath)

    def testTags(self):
        self.assertTrue("тест" in self.root["Страница 1"].tags)
        self.assertTrue("test" in self.root["Страница 1"].tags, self.root["Страница 1"].tags)
        self.assertTrue("двойной тег" in self.root["Страница 1"].tags)
        self.assertEqual(len(self.root["Страница 1"].tags), 3)

        self.assertTrue("test" in self.root["Страница 1/Страница 2"].tags)
        self.assertEqual(len(self.root["Страница 1/Страница 2"].tags), 1)

        self.assertTrue("test" in self.root["Страница 3"].tags)
        self.assertTrue("тест" in self.root["Страница 3"].tags)
        self.assertEqual(len(self.root["Страница 3"].tags), 2)

        self.assertEqual(len(self.root["page 4"].tags), 0)

    def testTypes(self):
        self.assertEqual(self.root["Страница 1"].getTypeString(), "html")
        self.assertEqual(self.root["Страница 1/Страница 2"].getTypeString(), "text")
        self.assertEqual(self.root["Страница 3"].getTypeString(), "html")
        self.assertEqual(self.root["page 4"].getTypeString(), "text")
        self.assertEqual(self.root["Страница 1/Страница 2/Страница 5"].getTypeString(), "text")

    def testChildren(self):
        self.assertEqual(len(self.root["Страница 1"].children), 1)
        self.assertEqual(self.root["Страница 1"].children[0], self.root["Страница 1/Страница 2"])

        self.assertEqual(len(self.root["Страница 1/Страница 2"].children), 2)
        self.assertEqual(len(self.root["Страница 3"].children), 0)
        self.assertEqual(len(self.root["page 4"].children), 0)

    def testIcons(self):
        self.assertEqual(os.path.basename(self.root["Страница 1"].icon), "__icon.png")
        self.assertEqual(os.path.basename(self.root["Страница 1/Страница 2"].icon), "__icon.gif")
        self.assertEqual(self.root["Страница 3"].icon, None)

    def testParams(self):
        typeOption = StringOption(self.root["Страница 1"].params, "General", "type", "")
        tagsOption = StringOption(self.root["Страница 1"].params, "General", "tags", "")

        self.assertEqual(typeOption.value, "html")
        self.assertEqual(tagsOption.value, "Тест, test, двойной тег")

    def testGetRoot(self):
        self.assertEqual(self.root["Страница 1"].root, self.root)
        self.assertEqual(self.root["Страница 1/Страница 2/Страница 5"].root, self.root)

    def testSubpath_01(self):
        self.assertEqual(self.root["Страница 1"].subpath, "Страница 1")

        self.assertEqual(self.root["Страница 1/Страница 2/Страница 5"].subpath,
                         "Страница 1/Страница 2/Страница 5")

    def testSubpath_02(self):
        page = self.root["Страница 1"]
        self.assertEqual(page[""], None)

    def testSubpathParent_01(self):
        page = self.root["Страница 1/Страница 2/Страница 5"]
        self.assertEqual(page[".."], self.root["Страница 1/Страница 2"])

    def testSubpathParent_02(self):
        page = self.root["Страница 1/Страница 2"]
        self.assertEqual(page[".."], self.root["Страница 1"])

    def testSubpathParent_03(self):
        page = self.root["Страница 1"]
        self.assertEqual(page[".."], self.root)

    def testSubpathParent_04(self):
        page = self.root
        self.assertEqual(page[".."], None)

    def testSubpathParent_05(self):
        page = page = self.root["Страница 1"]
        self.assertEqual(page["../.."], None)

    def testSubpathParent_06(self):
        page = self.root
        self.assertEqual(page["../.."], None)

    def testIsChild1(self):
        self.assertTrue(self.root.isChild(self.root["Страница 1"]))

    def testIsChild2(self):
        self.assertTrue(self.root.isChild(self.root))

    def testIsChild3(self):
        self.assertTrue(self.root["Страница 1"].isChild(self.root["Страница 1/Страница 2/Страница 5"]))


class SubWikiTest(unittest.TestCase):
    """
    Тест на открытие подстраниц вики как полноценную вики
    """
    def setUp(self):
        self.rootpath = "../test/samplewiki"

    def test1(self):
        path = os.path.join(self.rootpath, "Страница 1")
        root = WikiDocument.load(path)

        self.assertEqual(len(root), 1)
        self.assertEqual(root["Страница 2"].title, "Страница 2")


class TextPageAttachmentTest(unittest.TestCase):
    """
    Тест для проверки работы с прикрепленными файлами
    """
    def setUp(self):
        # Количество срабатываний особытий при обновлении страницы
        self.pageUpdateCount = 0
        self.pageUpdateSender = None

        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        Application.wikiroot = self.wikiroot

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create(self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

    def tearDown(self):
        removeDir(self.path)

    def testEvent(self):
        self.pageUpdateCount = 0

        Application.onAttachListChanged += self.onAttachListChanged

        page1 = "Страница 1"
        page3 = "Страница 2/Страница 3"

        filesPath = "../test/samplefiles/"
        files = ["accept.png", "add.png", "anchor.png"]

        fullFilesPath = [os.path.join(filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.wikiroot[page1]).attach(fullFilesPath)

        self.assertEqual(self.pageUpdateCount, 1)
        self.assertEqual(self.pageUpdateSender, self.wikiroot[page1])

        Attachment(self.wikiroot[page3]).attach([fullFilesPath[0], fullFilesPath[1]])

        self.assertEqual(self.pageUpdateCount, 2)
        self.assertEqual(self.pageUpdateSender, self.wikiroot[page3])

        Application.onAttachListChanged -= self.onAttachListChanged

    def onAttachListChanged(self, sender, params):
        self.pageUpdateCount += 1
        self.pageUpdateSender = sender

    def testAttach(self):
        page1 = "Страница 1"
        page3 = "Страница 2/Страница 3"

        filesPath = "../test/samplefiles/"
        files = ["accept.png", "add.png", "anchor.png"]

        fullFilesPath = [os.path.join(filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.wikiroot[page1]).attach(fullFilesPath)
        Attachment(self.wikiroot[page3]).attach([fullFilesPath[0], fullFilesPath[1]])

        # Заново загрузим вики
        wiki = WikiDocument.load(self.path)

        # Проверим, что файлы прикрепились к тем страницам, куда прикрепляли
        self.assertEqual(len(Attachment(wiki[page1]).attachmentFull), 3)
        self.assertEqual(len(Attachment(wiki[page3]).attachmentFull), 2)
        self.assertEqual(len(Attachment(wiki["Страница 2"]).attachmentFull), 0)

        # Проверим пути до прикрепленных файлов
        attachPathPage1 = TextPageAttachmentTest.getFullAttachPath(wiki, page1, files)
        attachPathPage3 = TextPageAttachmentTest.getFullAttachPath(wiki, page3, files)

        self.assertTrue(attachPathPage1[0] in Attachment(wiki[page1]).attachmentFull)
        self.assertTrue(attachPathPage1[1] in Attachment(wiki[page1]).attachmentFull)
        self.assertTrue(attachPathPage1[2] in Attachment(wiki[page1]).attachmentFull)

        self.assertTrue(attachPathPage3[0] in Attachment(wiki[page3]).attachmentFull)
        self.assertTrue(attachPathPage3[1] in Attachment(wiki[page3]).attachmentFull)

    def testAttach2(self):
        page1 = "Страница 1"
        page3 = "Страница 2/Страница 3"

        filesPath = "../test/samplefiles/"
        files = ["accept.png", "add.png", "anchor.png"]

        fullFilesPath = [os.path.join(filesPath, fname) for fname in files]

        # Прикрепим к двум страницам файлы
        Attachment(self.wikiroot[page1]).attach(fullFilesPath)
        Attachment(self.wikiroot[page3]).attach([fullFilesPath[0], fullFilesPath[1]])

        # Проверим, что файлы прикрепились к тем страницам, куда прикрепляли
        self.assertEqual(len(Attachment(self.wikiroot[page1]).attachmentFull), 3)
        self.assertEqual(len(Attachment(self.wikiroot[page3]).attachmentFull), 2)
        self.assertEqual(len(Attachment(self.wikiroot["Страница 2"]).attachmentFull), 0)

        # Проверим пути до прикрепленных файлов
        attachPathPage1 = TextPageAttachmentTest.getFullAttachPath(self.wikiroot, page1, files)
        attachPathPage3 = TextPageAttachmentTest.getFullAttachPath(self.wikiroot, page3, files)

        self.assertTrue(attachPathPage1[0] in Attachment(self.wikiroot[page1]).attachmentFull)
        self.assertTrue(attachPathPage1[1] in Attachment(self.wikiroot[page1]).attachmentFull)
        self.assertTrue(attachPathPage1[2] in Attachment(self.wikiroot[page1]).attachmentFull)

        self.assertTrue(attachPathPage3[0] in Attachment(self.wikiroot[page3]).attachmentFull)
        self.assertTrue(attachPathPage3[1] in Attachment(self.wikiroot[page3]).attachmentFull)

    @staticmethod
    def getFullAttachPath(wiki, pageSubpath, fnames):
        """
        Сформировать список полных путей до прикрепленных файлов
        wiki -- загруженная вики
        pageSubpath -- путь до страницы
        fnames -- имена файлов
        """
        attachPath = os.path.join(Attachment(wiki[pageSubpath]).getAttachPath())
        result = [os.path.join(attachPath, fname) for fname in fnames]

        return result
