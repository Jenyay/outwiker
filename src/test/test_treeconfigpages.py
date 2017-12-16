# -*- coding: UTF-8 -*-

import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.config import StringOption
from outwiker.pages.text.textpage import TextPageFactory
from .utils import removeDir


class ConfigPagesTest (unittest.TestCase):
    """
    Тесты, связанные с настройками страниц и вики в целом
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


    def tearDown (self):
        removeDir (self.path)


    def testSetRootParams (self):
        param = StringOption (self.wikiroot.params, "TestSection_1", "value1", "")
        param.value = "Значение 1"

        self.assertEqual (param.value, "Значение 1")

        # Прочитаем вики и проверим установленный параметр
        wiki = WikiDocument.create (self.path)

        param_new = StringOption (wiki.params, "TestSection_1", "value1", "")
        self.assertEqual (param_new.value, "Значение 1")


    def testSetPageParams (self):
        param = StringOption (self.wikiroot["Страница 1"].params, "TestSection_1", "value1", "")
        param.value = "Значение 1"

        param2 = StringOption (self.wikiroot["Страница 1"].params, "TestSection_1", "value1", "")
        self.assertEqual (param.value, "Значение 1")
        self.assertEqual (param2.value, "Значение 1")

        # Прочитаем вики и проверим установленный параметр
        wiki = WikiDocument.load (self.path)
        param3 = StringOption (wiki["Страница 1"].params, "TestSection_1", "value1", "")

        self.assertEqual (param3.value, "Значение 1")


    def testSubwikiParams (self):
        """
        Проверка того, что установка параметров страницы как полноценной вики не портит исходные параметры
        """
        param = StringOption (self.wikiroot["Страница 1"].params, "TestSection_1", "value1", "")
        param.value = "Значение 1"

        path = os.path.join (self.path, "Страница 1")
        subwiki = WikiDocument.load (path)

        subwikiparam = StringOption (subwiki.params, "TestSection_1", "value1", "")
        self.assertEqual (subwikiparam.value, "Значение 1")

        # Добавим новый параметр
        subwikiparam1 = StringOption (subwiki.params, "TestSection_1", "value1", "")
        subwikiparam2 = StringOption (subwiki.params, "TestSection_2", "value2", "")
        subwikiparam2.value = "Значение 2"

        self.assertEqual (subwikiparam1.value, "Значение 1")
        self.assertEqual (subwikiparam2.value, "Значение 2")

        # На всякий случай прочитаем вики еще раз
        wiki = WikiDocument.load (self.path)

        wikiparam1 = StringOption (wiki["Страница 1"].params, "TestSection_1", "value1", "")
        wikiparam2 = StringOption (wiki["Страница 1"].params, "TestSection_2", "value2", "")

        self.assertEqual (wikiparam1.value, "Значение 1")
        self.assertEqual (wikiparam2.value, "Значение 2")
