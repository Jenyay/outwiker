# -*- coding: utf-8 -*-

from unittest import TestCase

from outwiker.core.registry import Registry


class RegistryTest(TestCase):
    def test_empty(self):
        reg = Registry({})
        self.assertFalse(reg.has_section('параметр'))
        self.assertFalse(reg.has_option('раздел', 'параметр'))

    def test_has_option_root(self):
        items = {'параметр': 1}
        reg = Registry(items)

        self.assertTrue(reg.has_option('параметр'))

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

        self.assertTrue(reg.has_section('раздел-1', 'раздел-2'))

    def test_has_section_02(self):
        items = {
            'раздел-1': {
                'параметр': 1,
            },
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.has_section)

    def test_has_option_01(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)
        self.assertTrue(reg.has_option('раздел-1', 'параметр'))

    def test_has_option_02(self):
        items = {
            'раздел-1': {
                'параметр': 1,
            },
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.has_option)

    def test_get_root(self):
        items = {
            'параметр': 1,
        }
        reg = Registry(items)

        self.assertEqual(reg.get('параметр'), 1)

    def test_get_section(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertEqual(reg.get('раздел-1', 'параметр'), 1)

    def test_get_key_error_01(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get, 'параметр')

    def test_get_key_error_02(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get, 'раздел-1', 'параметр-2')

    def test_get_key_error_03(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get, 'раздел-2', 'параметр')

    def test_get_key_error_04(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get)

    def test_get_key_error_05(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get, 'раздел-1')

    def test_get_key_error_06(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get, 'раздел-1', default=10)

    def test_get_key_error_07(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get, default=10)

    def test_get_key_error_08(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
                'параметр': 1,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError,
                          reg.get, 'раздел-1', 'раздел-2', default=10)

    def test_get_default_01(self):
        items = {
        }
        reg = Registry(items)

        self.assertEqual(reg.get('параметр', default=1), 1)

    def test_get_default_02(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 1,
                },
            },
        }
        reg = Registry(items)
        self.assertEqual(reg.get('раздел-1', 'раздел-2', 'параметр',
                                 default=10), 1)

    def test_get_default_03(self):
        items = {
            'раздел-1': {
                'параметр': 1,
            },
        }
        reg = Registry(items)
        self.assertEqual(reg.get('раздел-1', 'раздел-2', 'параметр',
                                 default=10), 10)

    def test_get_default_04(self):
        items = {
            'раздел-1': {
                'параметр': 1,
            },
        }
        reg = Registry(items)
        self.assertEqual(reg.get('раздел-1', 'параметр-2',
                                 default=10), 10)
