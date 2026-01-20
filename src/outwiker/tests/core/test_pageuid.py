# -*- coding: utf-8 -*-

import unittest
from tempfile import mkdtemp

from outwiker.api.core.tree import createNotesTree, generateLink
from outwiker.core.tree import PageUidDepot
from outwiker.core.application import Application
from outwiker.core.exceptions import ReadonlyException
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


class PageUidDepotTest(unittest.TestCase):
    """Тест класса PageUidDepot"""

    def setUp(self):
        self._application = Application()
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = createNotesTree(self.path)

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 1", [])
        # factory.create(self.wikiroot, "Страница 2", [])
        # factory.create(self.wikiroot["Страница 2"], "Страница 3", [])
        # factory.create(self.wikiroot["Страница 2/Страница 3"],
        #                "Страница 4",
        #                [])
        # factory.create(self.wikiroot["Страница 1"], "Страница 5", [])

        self.page_1 = self.wikiroot["Страница 1"]
        self._application.wikiroot = None

    def tearDown(self):
        self._application.wikiroot = None
        removeDir(self.path)

    def test_invalid_uid(self):
        self.assertEqual(self.wikiroot.getPageByUid("Абырвалг"), None)

    def test_empty_uid_not_generate(self):
        self.page_1._clearUid()
        uid = self.page_1.getUid(generate=False)
        self.assertIsNone(uid)

    def test_empty_uid_generate(self):
        self.page_1._clearUid()
        uid = self.page_1.getUid(generate=True)
        self.assertIsNotNone(uid)

    def test_default_uid(self):
        uid = self.page_1.getUid(generate=False)
        self.assertIsNotNone(uid)

    def test_uid_not_changed(self):
        uid_1 = self.page_1.getUid(generate=False)
        uid_2 = self.page_1.getUid(generate=True)
        self.assertEqual(uid_1, uid_2)

    def test_get_page_by_uid(self):
        uid = self.page_1.getUid(generate=False)
        self.assertIsNotNone(self.wikiroot.getPageByUid(uid))

    def test_get_page_by_uid_deeper(self):
        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 2", [])
        new_page = factory.create(self.wikiroot["Страница 2"], "Страница 3", [])

        uid = new_page.getUid(generate=False)
        self.assertIsNotNone(self.wikiroot.getPageByUid(uid))

    def test_get_page_by_uid_upper(self):
        uid = self.page_1.getUid(generate=False)
        self.assertIsNotNone(self.wikiroot.getPageByUid(uid.upper()))

    def test_change_uid(self):
        old_uid = self.page_1.getUid(generate=True)
        new_uid = "new_uid"
        self.page_1.setUid(new_uid)

        self.assertEqual(self.wikiroot.getPageByUid(new_uid).subpath, self.page_1.subpath)
        self.assertIsNone(self.wikiroot.getPageByUid(old_uid))

    def test_change_uid_not_unique(self):
        factory = TextPageFactory()
        page_1_uid = self.page_1.getUid(generate=True)
        page_2 = factory.create(self.wikiroot, "Страница 2", [])

        with self.assertRaises(KeyError):
            page_2.setUid(page_1_uid)

    def test_change_uid_not_unique_upper(self):
        factory = TextPageFactory()
        page_1_uid = self.page_1.getUid(generate=True)
        page_2 = factory.create(self.wikiroot, "Страница 2", [])

        with self.assertRaises(KeyError):
            page_2.setUid(page_1_uid.upper())

    def test_change_uid_empty(self):
        factory = TextPageFactory()
        page_2 = factory.create(self.wikiroot, "Страница 2", [])

        with self.assertRaises(ValueError):
            page_2.setUid("")

    def test_change_uid_spaces(self):
        factory = TextPageFactory()
        page_2 = factory.create(self.wikiroot, "Страница 2", [])

        with self.assertRaises(ValueError):
            page_2.setUid("    ")

    def test_change_uid_slash(self):
        factory = TextPageFactory()
        page_2 = factory.create(self.wikiroot, "Страница 2", [])

        with self.assertRaises(ValueError):
            page_2.setUid("1111/222")

    def test_change_uid_none(self):
        factory = TextPageFactory()
        page_2 = factory.create(self.wikiroot, "Страница 2", [])

        with self.assertRaises(ValueError):
            page_2.setUid(None)

    def test_change_uid_readonly(self):
        new_uid = "new_uid"
        self.page_1.readonly = True

        with self.assertRaises(ReadonlyException):
            self.page_1.setUid(new_uid)

        self.wikiroot.getPageByUid(new_uid)

    def test_change_uid_equal(self):
        uid = self.page_1.getUid(generate=True)
        self.page_1.setUid(uid)

        self.assertIsNotNone(self.wikiroot.getPageByUid(uid))

    def test_get_new_uid_readonly_generate_true(self):
        self.page_1._clearUid()
        self.page_1.readonly = True

        with self.assertRaises(ReadonlyException):
            self.page_1.getUid(generate=True)

    def test_get_new_uid_readonly_generate_false(self):
        self.page_1._clearUid()
        self.page_1.readonly = True

        uid = self.page_1.getUid(generate=False)
        self.assertIsNone(uid)

    def test_get_new_uid_readonly_generate_default(self):
        self.page_1._clearUid()
        self.page_1.readonly = True

        uid = self.page_1.getUid(generate=False)
        self.assertIsNone(uid)

    def test_rename_page(self):
        uid = self.page_1.getUid()
        new_title = "Новый заголовок"
        self.page_1.title = new_title
        self.assertEqual(self.wikiroot.getPageByUid(uid).title, new_title)

    def test_remove_page(self):
        uid = self.page_1.getUid()
        self.assertIsNotNone(self.wikiroot.getPageByUid(uid))

        self.page_1.remove()
        self.assertIsNone(self.wikiroot.getPageByUid(uid))

    def test_move_page(self):
        uid = self.page_1.getUid()

        factory = TextPageFactory()
        factory.create(self.wikiroot, "Страница 2", [])
        new_page = factory.create(self.wikiroot["Страница 2"], "Страница 3", [])

        self.page_1.moveTo(new_page)
        self.assertEqual(self.wikiroot.getPageByUid(uid).subpath, self.page_1.subpath)

    def test_generate_link_01(self):
        self._application.wikiroot = self.wikiroot
        page = self.wikiroot["Страница 1"]
        uid = page.getUid()

        link = generateLink(self._application, page)
        self.assertIn("page://", link)
        self.assertIn(uid, link)

    def test_generate_link_02(self):
        self._application.wikiroot = self.wikiroot
        page = self.wikiroot["Страница 1"]

        newUid = "Абырвалг"
        page.setUid(newUid)

        link = generateLink(self._application, page)
        self.assertIn("page://", link)
        self.assertIn("абырвалг", link)

    def test_generate_link_03(self):
        self._application.wikiroot = self.wikiroot
        page = self.wikiroot["Страница 1"]

        newUid = "Абырвалг"
        page.setUid(newUid)

        link = generateLink(self._application, page)
        self.assertIn("page://", link)
        self.assertIn("абырвалг", link)
