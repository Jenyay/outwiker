# -*- coding: UTF-8 -*-
import os.path
import os
import unittest

from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeWiki


class ManualEditTest (unittest.TestCase):
    """
    Класс тестов, связанных с изменением страниц внешними средствами
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeWiki (self.path)

        self.rootwiki = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.rootwiki, u"Страница 1", [])
        factory.create (self.rootwiki, u"Страница 2", [])
        factory.create (self.rootwiki[u"Страница 2"], u"Страница 3", [])
        factory.create (self.rootwiki[u"Страница 2/Страница 3"], u"Страница 4", [])
        factory.create (self.rootwiki[u"Страница 1"], u"Страница 5", [])

        self.rootwiki[u"Страница 1"].content = u"1234567"
        self.rootwiki[u"Страница 2/Страница 3"].content = u"Абырвалг"
        self.rootwiki[u"Страница 2/Страница 3/Страница 4"].content = u"Тарам-пам-пам"
        self.rootwiki[u"Страница 1/Страница 5"].content = u"111111"

        self.rootwiki[u"Страница 1"].tags = [u"метка 1"]
        self.rootwiki[u"Страница 2/Страница 3"].tags = [u"метка 2", u"метка 3"]
        self.rootwiki[u"Страница 2/Страница 3/Страница 4"].tags = [u"метка 1", u"метка 2", u"метка 4"]

        self.rootwiki[u"Страница 2/Страница 3/Страница 4"].icon = "../test/images/feed.gif"


    def tearDown(self):
        removeWiki (self.path)


    def __changeContent (self, page, newcontent):
        page.content = newcontent


    def testContentRenamedPage (self):
        page = self.rootwiki[u"Страница 1"]

        newtitle = u"Новый заголовок"
        newpath = os.path.join (page.root.path, newtitle)

        os.renames (page.path, newpath)

        self.assertRaises (IOError, self.__changeContent, page, u"bla-bla-bla")


    def testTagsRenamedPage (self):
        page = self.rootwiki[u"Страница 1"]

        newtitle = u"Новый заголовок"
        newpath = os.path.join (page.root.path, newtitle)

        os.renames (page.path, newpath)

        page.tags = [u"bla-bla-bla"]
        self.assertTrue (os.path.exists (page.path))
        self.assertEqual (self.rootwiki[u"Страница 1"], page)


    def testReloadWiki (self):
        page = self.rootwiki[u"Страница 1"]

        newtitle = u"Новый заголовок"
        newpath = os.path.join (page.root.path, newtitle)

        os.renames (page.path, newpath)

        # Заново загрузим вики
        newroot = WikiDocument.load (self.path)

        self.assertEqual (newroot[u"Страница 1"], None)
        self.assertNotEqual (newroot[newtitle], None)
        self.assertEqual (newroot[newtitle].title, newtitle)
