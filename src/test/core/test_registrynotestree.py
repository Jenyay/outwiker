# -*- coding: utf-8 -*-

from unittest import TestCase

from outwiker.core.registrynotestree import BaseSaver, NotesTreeRegistry
from outwiker.pages.text.textpage import TextPageFactory

from test.basetestcases import BaseOutWikerMixin


class SimpleSaver(BaseSaver):
    def __init__(self, items_dict):
        self._items_dict = items_dict
        self.load_count = 0
        self.save_count = 0

    def load(self):
        self.load_count += 1
        return self._items_dict

    def save(self, items_dict):
        self.save_count += 1


class RegistryNotesTreeTest(TestCase):
    def test_load(self):
        saver = SimpleSaver({})
        NotesTreeRegistry(saver)

        self.assertEqual(saver.load_count, 1)
        self.assertEqual(saver.save_count, 0)

    def test_save(self):
        saver = SimpleSaver({})
        reg = NotesTreeRegistry(saver)
        reg.save()

        self.assertEqual(saver.save_count, 1)

    def test_get_section_or_create_01(self):
        saver = SimpleSaver({})
        reg = NotesTreeRegistry(saver)

        reg.get_section_or_create('раздел-1')
        reg.has_section('раздел-1')

    def test_get_section_or_create_02(self):
        saver = SimpleSaver({})
        reg = NotesTreeRegistry(saver)

        reg.get_section_or_create('раздел-1', 'раздел-2')
        reg.has_section('раздел-1', 'раздел-2')

    def test_get_section_or_create_03(self):
        saver = SimpleSaver({
            'бла-бла-бла': 1000,
        })
        reg = NotesTreeRegistry(saver)

        reg.get_section_or_create('бла-бла-бла')
        reg.has_section('бла-бла-бла')

    def test_get_section_or_create_04(self):
        saver = SimpleSaver({
            'раздел-1': {
                'бла-бла-бла': 1000,
            },
        })
        reg = NotesTreeRegistry(saver)

        reg.get_section_or_create('раздел-1', 'бла-бла-бла')
        reg.has_section('раздел-1', 'бла-бла-бла')

    def test_get_section_or_create_05(self):
        saver = SimpleSaver({})
        reg = NotesTreeRegistry(saver)

        subreg = reg.get_section_or_create('раздел-1', 'раздел-2', 'раздел-3')

        subreg.set('параметр', 100)
        self.assertEqual(reg.getint('раздел-1', 'раздел-2', 'раздел-3',
                                    'параметр'),
                         100)

    def test_get_section_or_create_06_invalid_type(self):
        saver = SimpleSaver({
            'раздел-1': {
                'раздел-2': 0,
            }
        })
        reg = NotesTreeRegistry(saver)

        subreg = reg.get_section_or_create('раздел-1', 'раздел-2', 'раздел-3')

        subreg.set('параметр', 100)
        self.assertEqual(reg.getint('раздел-1', 'раздел-2', 'раздел-3',
                                    'параметр'),
                         100)


class RegistryNotesTreeWikiTest(TestCase, BaseOutWikerMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()

    def tearDown(self):
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_registry_remove_page_01(self):
        factory = TextPageFactory()
        page1 = factory.create(self.wikiroot, "Страница 1", [])
        self.wikiroot.registry.get_page_registry(page1)

        self.assertTrue(self.wikiroot.registry.has_section_for_page(page1))

        page1.remove()
        self.assertFalse(self.wikiroot.registry.has_section_for_page(page1))

    def test_registry_remove_page_02_subpage(self):
        factory = TextPageFactory()
        page1 = factory.create(self.wikiroot, "Страница 1", [])
        page2 = factory.create(page1, "Страница 2", [])

        self.wikiroot.registry.get_page_registry(page2)
        self.assertTrue(self.wikiroot.registry.has_section_for_page(page2))

        page2.remove()
        self.assertFalse(self.wikiroot.registry.has_section_for_page(page2))

    def test_registry_remove_page_03_with_children(self):
        factory = TextPageFactory()
        page1 = factory.create(self.wikiroot, "Страница 1", [])
        page2 = factory.create(page1, "Страница 2", [])

        self.wikiroot.registry.get_page_registry(page1)
        self.wikiroot.registry.get_page_registry(page2)
        self.assertTrue(self.wikiroot.registry.has_section_for_page(page1))
        self.assertTrue(self.wikiroot.registry.has_section_for_page(page2))

        page1.remove()
        self.assertFalse(self.wikiroot.registry.has_section_for_page(page1))
        self.assertFalse(self.wikiroot.registry.has_section_for_page(page2))
