# -*- coding: UTF-8 -*-

import os.path
import os
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeDir


class ManualEditTest (unittest.TestCase):
    """
    Класс тестов, связанных с изменением страниц внешними средствами
    """
    def setUp(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp (prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create (self.path)

        factory = TextPageFactory()
        factory.create (self.wikiroot, "Страница 1", [])
        factory.create (self.wikiroot, "Страница 2", [])
        factory.create (self.wikiroot["Страница 2"], "Страница 3", [])
        factory.create (self.wikiroot["Страница 2/Страница 3"], "Страница 4", [])
        factory.create (self.wikiroot["Страница 1"], "Страница 5", [])

        self.wikiroot["Страница 1"].content = "1234567"
        self.wikiroot["Страница 2/Страница 3"].content = "Абырвалг"
        self.wikiroot["Страница 2/Страница 3/Страница 4"].content = "Тарам-пам-пам"
        self.wikiroot["Страница 1/Страница 5"].content = "111111"

        self.wikiroot["Страница 1"].tags = ["метка 1"]
        self.wikiroot["Страница 2/Страница 3"].tags = ["метка 2", "метка 3"]
        self.wikiroot["Страница 2/Страница 3/Страница 4"].tags = ["метка 1", "метка 2", "метка 4"]

        self.wikiroot["Страница 2/Страница 3/Страница 4"].icon = "../test/images/feed.gif"


    def tearDown(self):
        removeDir (self.path)


    def __changeContent (self, page, newcontent):
        page.content = newcontent


    def testContentRenamedPage (self):
        page = self.wikiroot["Страница 1"]

        newtitle = "Новый заголовок"
        newpath = os.path.join (page.root.path, newtitle)

        os.renames (page.path, newpath)

        self.assertRaises (IOError, self.__changeContent, page, "bla-bla-bla")


    def testTagsRenamedPage (self):
        page = self.wikiroot["Страница 1"]

        newtitle = "Новый заголовок"
        newpath = os.path.join (page.root.path, newtitle)

        os.renames (page.path, newpath)

        page.tags = ["bla-bla-bla"]
        self.assertTrue (os.path.exists (page.path))
        self.assertEqual (self.wikiroot["Страница 1"], page)


    def testReloadWiki (self):
        page = self.wikiroot["Страница 1"]

        newtitle = "Новый заголовок"
        newpath = os.path.join (page.root.path, newtitle)

        os.renames (page.path, newpath)

        # Заново загрузим вики
        newroot = WikiDocument.load (self.path)

        self.assertEqual (newroot["Страница 1"], None)
        self.assertNotEqual (newroot[newtitle], None)
        self.assertEqual (newroot[newtitle].title, newtitle)
