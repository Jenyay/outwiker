"""
Тесты, связанные с созданием вики
"""

import os
import os.path
import stat
import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, loadNotesTree
from outwiker.core.attachment import Attachment
from outwiker.core.application import Application
from outwiker.core.defines import PAGE_OPT_FILE
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.utils import removeDir

from outwiker.pages.text.defines import PAGE_TYPE_STRING as TEXT_TS
from outwiker.pages.wiki.defines import PAGE_TYPE_STRING as WIKI_TS
from outwiker.pages.html.defines import PAGE_TYPE_STRING as HTML_TS
from outwiker.pages.search.defines import PAGE_TYPE_STRING as SEARCH_TS


class TextPageCreationTest(unittest.TestCase):
    """
    Класс тестов, связанных с созданием страниц вики
    """

    def setUp(self):
        self._application = Application()
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')
        self.eventcount = 0

        self.wikiroot = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        factory.create(self.wikiroot, "Страница 2", [])
        factory.create(self.wikiroot["Страница 2"], "Страница 3", [])

        factory.create(self.wikiroot["Страница 2/Страница 3"],
                       "Страница 4",
                       [])

        factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.wikiroot["Страница 1"].content = "1234567"
        self.wikiroot["Страница 2/Страница 3"].content = "Абырвалг"
        self.wikiroot["Страница 2/Страница 3/Страница 4"].content = "Тарам-пам-пам"
        self.wikiroot["Страница 1/Страница 5"].content = "111111"

        self.wikiroot["Страница 1"].tags = ["метка 1"]
        self.wikiroot["Страница 2/Страница 3"].tags = ["метка 2", "метка 3"]
        self.wikiroot["Страница 2/Страница 3/Страница 4"].tags = ["метка 1",
                                                                  "метка 2", "метка 4"]

        self.wikiroot["Страница 2/Страница 3/Страница 4"].icon = "testdata/images/feed.gif"

        self.wikiroot["Страница 1"].alias = 'page 1'
        self.wikiroot["Страница 1/Страница 5"].alias = 'page 5'
        self.wikiroot["Страница 2/Страница 3"].alias = 'page 3'

        self.icons = ["testdata/images/icon.gif",
                      "testdata/images/icon.png",
                      "testdata/images/icon.jpg",
                      "testdata/images/icon.ico"]

        self._application.wikiroot = None

    def tearDown(self):
        self._application.wikiroot = None
        os.chmod(self._getConfigPath(self.wikiroot),
                 stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR)
        os.chmod(self._getConfigPath(self.wikiroot["Страница 1"]),
                 stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR)

        if self.wikiroot["Страница 2"] is not None:
            os.chmod(self._getConfigPath(self.wikiroot["Страница 2"]),
                     stat.S_IRUSR | stat.S_IXUSR | stat.S_IWUSR)

        removeDir(self.path)

    def onPageUpdate(self, page, **kwargs):
        self.eventcount += 1

    def testDisplaySubpath(self):
        self.assertEqual(self.wikiroot.display_subpath, '/')

        self.assertEqual(
            self.wikiroot["Страница 1"].display_subpath,
            'page 1'
        )

        self.assertEqual(
            self.wikiroot["Страница 1/Страница 5"].display_subpath,
            'page 1/page 5'
        )

        self.assertEqual(
            self.wikiroot["Страница 2/Страница 3"].display_subpath,
            'Страница 2/page 3'
        )

    def testEventChangeContent(self):
        self._application.wikiroot = self.wikiroot
        self._application.onPageUpdate += self.onPageUpdate

        self.wikiroot["Страница 1"].content = "тарам-там-там"
        self.assertEqual(self.eventcount, 1)

        self._application.onPageUpdate -= self.onPageUpdate

    def testNoEventChangeContent(self):
        self._application.onPageUpdate += self.onPageUpdate

        self.wikiroot["Страница 1"].content = "тарам-там-там"
        self.assertEqual(self.eventcount, 0)

        self._application.onPageUpdate -= self.onPageUpdate

    def testEventChangeTags(self):
        self._application.wikiroot = self.wikiroot
        self._application.onPageUpdate += self.onPageUpdate

        self.wikiroot["Страница 1"].tags = ["метка 1", "метка 2", "метка 4"]
        self.assertEqual(self.eventcount, 1)

        # То же самое содержимое
        self.wikiroot["Страница 1"].tags = ["метка 1", "метка 2", "метка 4"]
        self.assertEqual(self.eventcount, 1)

        self._application.onPageUpdate -= self.onPageUpdate

    def testNoEventChangeTags(self):
        self._application.onPageUpdate += self.onPageUpdate

        self.wikiroot["Страница 1"].tags = ["метка 1", "метка 2", "метка 4"]
        self.assertEqual(self.eventcount, 0)

        self._application.onPageUpdate -= self.onPageUpdate

    def testAttach1(self):
        # Получить путь до прикрепленных файлов, не создавая ее
        path = Attachment(self.wikiroot["Страница 2"]).getAttachPath()
        # Вложенных файлов еще нет, поэтому нет и папки
        self.assertFalse(os.path.exists(path))

    def testAttach2(self):
        # Получить путь до прикрепленных файлов, не создавая ее
        path = Attachment(
            self.wikiroot["Страница 2"]).getAttachPath(create=False)
        # Вложенных файлов еще нет, поэтому нет и папки
        self.assertFalse(os.path.exists(path))

    def testAttach3(self):
        # Получить путь до прикрепленных файлов, создав ее
        path = Attachment(
            self.wikiroot["Страница 2"]).getAttachPath(create=True)
        # Вложенных файлов еще нет, поэтому нет и папки
        self.assertTrue(os.path.exists(path))

    def testTypeCreation(self):
        textPage = TextPageFactory().create(self.wikiroot,
                                            "Текстовая страница",
                                            [])

        self.assertEqual(TEXT_TS, textPage.getTypeString())

        wikiPage = WikiPageFactory().create(self.wikiroot,
                                            "Вики-страница",
                                            [])

        self.assertEqual(WIKI_TS, wikiPage.getTypeString())

        htmlPage = HtmlPageFactory().create(self.wikiroot,
                                            "HTML-страница",
                                            [])

        self.assertEqual(HTML_TS, htmlPage.getTypeString())

        searchPage = SearchPageFactory().create(self.wikiroot,
                                                "Поисковая страница",
                                                [])

        self.assertEqual(SEARCH_TS, searchPage.getTypeString())

    def testIcon(self):
        wiki = loadNotesTree(self.path)
        self.assertEqual(os.path.basename(
            wiki["Страница 2/Страница 3/Страница 4"].icon),
            "__icon.gif")

    def testReplaceIcon(self):
        wiki = loadNotesTree(self.path)

        wiki["Страница 1"].icon = self.icons[3]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.ico")

        wiki["Страница 1"].icon = self.icons[1]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.png")

        wiki["Страница 1"].icon = self.icons[0]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.gif")

        wiki["Страница 1"].icon = self.icons[2]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.jpg")

        wiki["Страница 1"].icon = self.icons[3]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.ico")

        wiki["Страница 1"].icon = self.icons[0]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.gif")

        wiki["Страница 1"].icon = self.icons[1]
        self.assertEqual(os.path.basename(wiki["Страница 1"].icon),
                         "__icon.png")

    def testTags(self):
        wiki = loadNotesTree(self.path)
        self.assertTrue("метка 1" in wiki["Страница 1"].tags)
        self.assertEqual(len(wiki["Страница 1"].tags), 1)

        self.assertIn("метка 2", wiki["Страница 2/Страница 3"].tags)
        self.assertIn("метка 3", wiki["Страница 2/Страница 3"].tags)
        self.assertEqual(len(wiki["Страница 2/Страница 3"].tags), 2)

        self.assertIn("метка 1",
                      wiki["Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn("метка 2",
                      wiki["Страница 2/Страница 3/Страница 4"].tags)

        self.assertIn("метка 4",
                      wiki["Страница 2/Страница 3/Страница 4"].tags)

        self.assertEqual(len(wiki["Страница 2/Страница 3/Страница 4"].tags),
                         3)

    def testCreation(self):
        self.assertTrue(os.path.exists(self.path))
        self.assertTrue(os.path.exists(os.path.join(self.path, PAGE_OPT_FILE)))

    def testInvalidPageName(self):
        children = len(self.wikiroot.children)
        self.assertRaises(Exception,
                          TextPageFactory.create,
                          self.wikiroot,
                          "+*5name:/\0",
                          [])

        self.assertEqual(len(self.wikiroot.children), children)

    def testPageCreate(self):
        wiki = loadNotesTree(self.path)
        self.assertEqual(wiki["Страница 1"].title, "Страница 1")
        self.assertEqual(wiki["Страница 2"].title, "Страница 2")
        self.assertEqual(wiki["Страница 2/Страница 3"].title, "Страница 3")

    def testCreateTextContent(self):
        wiki = loadNotesTree(self.path)
        self.assertEqual(wiki["Страница 1"].content, "1234567")
        self.assertEqual(wiki["Страница 2/Страница 3"].content, "Абырвалг")
        self.assertEqual(wiki["Страница 2/Страница 3/Страница 4"].content,
                         "Тарам-пам-пам")
        self.assertEqual(wiki["Страница 1/Страница 5"].content, "111111")

    def testSelection1(self):
        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.assertEqual(self.wikiroot.selectedPage,
                         self.wikiroot["Страница 2/Страница 3"])

    def testSelection3(self):
        self.wikiroot.selectedPage = None
        wiki2 = loadNotesTree(self.path)

        self.assertEqual(wiki2.selectedPage, None)

    def testSelection5(self):
        self.wikiroot.selectedPage = self.wikiroot["Страница 2/Страница 3"]
        self.wikiroot["Страница 2"].remove()

        wiki2 = loadNotesTree(self.path)

        self.assertEqual(wiki2.selectedPage, None)

    def testReadOnly_01(self):
        os.chmod(self._getConfigPath(self.wikiroot["Страница 1"]),
                 stat.S_IRUSR | stat.S_IXUSR)

        wiki2 = loadNotesTree(self.path)
        self.assertTrue(wiki2["Страница 1"].readonly)
        self.assertFalse(wiki2["Страница 1/Страница 5"].readonly)
        self.assertFalse(wiki2["Страница 2"].readonly)

    def testReadOnly_02(self):
        os.chmod(self._getConfigPath(self.wikiroot),
                 stat.S_IRUSR | stat.S_IXUSR)

        wiki2 = loadNotesTree(self.path)
        self.assertTrue(wiki2["Страница 1"].readonly)
        self.assertTrue(wiki2["Страница 1/Страница 5"].readonly)
        self.assertTrue(wiki2["Страница 2"].readonly)

    def testReadOnly_03(self):
        os.chmod(self._getConfigPath(self.wikiroot["Страница 2"]),
                 stat.S_IRUSR | stat.S_IXUSR)

        wiki2 = loadNotesTree(self.path)
        self.assertTrue(wiki2["Страница 2"].readonly)
        self.assertFalse(wiki2["Страница 2/Страница 3"].readonly)
        self.assertFalse(wiki2["Страница 2/Страница 3/Страница 4"].readonly)

    def _getConfigPath(self, page):
        return os.path.join(page.path, PAGE_OPT_FILE)
