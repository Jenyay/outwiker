# -*- coding: utf-8 -*-

from unittest import TestCase

from outwiker.core.registry import Registry


class RegistryTest(TestCase):
    def test_empty(self):
        reg = Registry({})
        self.assertFalse(reg.has_section('параметр'))
        self.assertFalse(reg.has_option('раздел/параметр'))

    def test_has_option_root(self):
        items = {'параметр': 1}
        reg = Registry(items)

        self.assertTrue(reg.has_option('параметр'))
        self.assertTrue(reg.has_option('/параметр'))

    def test_has_section_root(self):
        items = {
            'параметр': 1,
            'раздел': {},
        }
        reg = Registry(items)

        self.assertFalse(reg.has_section('параметр'))
        self.assertTrue(reg.has_section('раздел'))

    def test_has_section_01(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertTrue(reg.has_section('раздел-1/раздел-2'))
        self.assertTrue(reg.has_section('/раздел-1/раздел-2'))

    def test_has_option_01(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertTrue(reg.has_option('раздел-1/параметр'))
        self.assertTrue(reg.has_option('/раздел-1/параметр'))
