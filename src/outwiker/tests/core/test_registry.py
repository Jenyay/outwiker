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

    def test_get_bool_01(self):
        items = {
            'параметр': True,
        }
        reg = Registry(items)
        self.assertTrue(reg.getbool('параметр'))

    def test_get_bool_02(self):
        items = {
            'параметр': False,
        }
        reg = Registry(items)
        self.assertFalse(reg.getbool('параметр'))

    def test_get_bool_03(self):
        items = {
            'параметр': True,
        }
        reg = Registry(items)
        self.assertTrue(reg.getbool('параметр', default=False))

    def test_get_bool_04(self):
        items = {
        }
        reg = Registry(items)
        self.assertTrue(reg.getbool('параметр', default=True))

    def test_get_bool_05(self):
        items = {
            'параметр': 110,
        }
        reg = Registry(items)
        self.assertFalse(reg.getbool('параметр', default=False))

    def test_get_bool_error_00(self):
        items = {
            'параметр': 110,
        }
        reg = Registry(items)
        self.assertRaises(ValueError, reg.getbool, 'параметр')

    def test_get_bool_error_01(self):
        items = {
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.getbool, 'параметр')

    def test_get_bool_error_02(self):
        items = {
            'раздел': {},
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.getbool, 'раздел')

    def test_get_bool_error_04(self):
        items = {
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.getbool)

    def test_get_int_error_00(self):
        items = {
            'параметр': '111',
        }
        reg = Registry(items)
        self.assertRaises(ValueError, reg.getint, 'параметр')

    def test_get_int_error_01(self):
        items = {
            'параметр': {},
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.getint, 'параметр')

    def test_get_int_01(self):
        items = {
            'параметр': 100,
        }
        reg = Registry(items)
        self.assertEqual(reg.getint('параметр'), 100)

    def test_get_int_02(self):
        items = {
        }
        reg = Registry(items)
        self.assertEqual(reg.getint('параметр', default=100), 100)

    def test_get_float_error_00(self):
        items = {
            'параметр': '111',
        }
        reg = Registry(items)
        self.assertRaises(ValueError, reg.getfloat, 'параметр')

    def test_get_float_error_01(self):
        items = {
            'параметр': {},
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.getfloat, 'параметр')

    def test_get_float_01(self):
        items = {
            'параметр': 100.0,
        }
        reg = Registry(items)
        self.assertEqual(reg.getfloat('параметр'), 100.0)

    def test_get_float_02(self):
        items = {
        }
        reg = Registry(items)
        self.assertEqual(reg.getfloat('параметр', default=100.0), 100.0)

    def test_get_float_03(self):
        items = {
            'параметр': 100,
        }
        reg = Registry(items)
        self.assertEqual(reg.getfloat('параметр'), 100)

    def test_get_str_error_00(self):
        items = {
            'параметр': 111,
        }
        reg = Registry(items)
        self.assertRaises(ValueError, reg.getstr, 'параметр')

    def test_get_str_error_01(self):
        items = {
            'параметр': {},
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.getstr, 'параметр')

    def test_get_str_01(self):
        items = {
            'параметр': 'абырвалг',
        }
        reg = Registry(items)
        self.assertEqual(reg.getstr('параметр'), 'абырвалг')

    def test_get_str_02(self):
        items = {
        }
        reg = Registry(items)
        self.assertEqual(reg.getstr('параметр', default='абырвалг'),
                         'абырвалг')

    def test_create_section_error_01(self):
        items = {}
        reg = Registry(items)
        self.assertRaises(KeyError, reg.create_section)

    def test_create_error_02(self):
        items = {
            'параметр': 111,
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.create_section, 'параметр')

    def test_create_error_03(self):
        items = {
            'раздел': {
                'параметр': 1000,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.create_section, 'раздел', 'параметр')

    def test_create_error_04(self):
        items = {
            'параметр': 111,
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.create_section, 'параметр', 'раздел')

    def test_create_section_01(self):
        items = {}
        reg = Registry(items)
        reg.create_section('раздел')

        self.assertTrue(reg.has_section('раздел'))

    def test_create_section_02(self):
        items = {}
        reg = Registry(items)
        reg.create_section('раздел-1', 'раздел-2')

        self.assertTrue(reg.has_section('раздел-1'))
        self.assertTrue(reg.has_section('раздел-1', 'раздел-2'))

    def test_create_section_03(self):
        items = {
            'раздел': {},
        }
        reg = Registry(items)
        reg.create_section('раздел')

        self.assertTrue(reg.has_section('раздел'))

    def test_create_section_04(self):
        items = {}
        reg = Registry(items)
        reg.create_section('раздел-1', 'раздел-2')
        reg.create_section('раздел-1', 'раздел-2')

        self.assertTrue(reg.has_section('раздел-1'))
        self.assertTrue(reg.has_section('раздел-1', 'раздел-2'))

    def test_remove_option_error_01(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.remove_option)

    def test_remove_option_error_02(self):
        items = {}
        reg = Registry(items)

        self.assertFalse(reg.remove_option('параметр'))

    def test_remove_option_error_03(self):
        items = {
            'раздел': {},
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.remove_option, 'раздел')

    def test_remove_option_error_04(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.remove_option, 'раздел-1', 'раздел-2')

    def test_remove_option_01(self):
        items = {
            'параметр': 100,
        }
        reg = Registry(items)
        result = reg.remove_option('параметр')

        self.assertTrue(result)
        self.assertFalse(reg.has_option('параметр'))

    def test_remove_option_02(self):
        items = {
            'раздел': {
                'параметр': 100,
            },
        }
        reg = Registry(items)
        result = reg.remove_option('раздел', 'параметр')

        self.assertTrue(result)
        self.assertFalse(reg.has_option('раздел', 'параметр'))

    def test_remove_option_03(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 100,
                },
            },
        }
        reg = Registry(items)
        result = reg.remove_option('раздел-1', 'раздел-2', 'параметр')

        self.assertTrue(result)
        self.assertFalse(reg.has_option('раздел-1', 'раздел-2', 'параметр'))

    def test_remove_section_error_01(self):
        items = {}
        reg = Registry(items)

        result = reg.remove_section('раздел')
        self.assertFalse(result)

    def test_remove_section_error_02(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.remove_section)

    def test_remove_section_error_03(self):
        items = {
            'параметр': 100,
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.remove_section)

    def test_remove_section_error_04(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 100,
                }
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError,
                          reg.remove_section,
                          'раздел-1', 'раздел-2', 'параметр')

    def test_remove_section_01(self):
        items = {
            'раздел': {},
        }
        reg = Registry(items)
        result = reg.remove_section('раздел')

        self.assertTrue(result)
        self.assertFalse(reg.has_section('раздел'))

    def test_remove_section_02(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 100,
                }
            },
        }
        reg = Registry(items)
        result = reg.remove_section('раздел-1')

        self.assertTrue(result)
        self.assertFalse(reg.has_section('раздел-1'))

    def test_remove_section_03(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 100,
                }
            },
        }
        reg = Registry(items)
        result = reg.remove_section('раздел-1', 'раздел-2')

        self.assertTrue(result)
        self.assertTrue(reg.has_section('раздел-1'))
        self.assertFalse(reg.has_section('раздел-1', 'раздел-2'))

    def test_set_error_01(self):
        items = {}
        reg = Registry(items)
        self.assertRaises(KeyError, reg.set)
        self.assertRaises(KeyError, reg.set, 'bla-bla-bla')

    def test_set_error_02(self):
        items = {
            'раздел': {}
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.set, 'раздел', 100)
        self.assertTrue(reg.has_section('раздел'))

    def test_set_error_03(self):
        items = {
            'раздел-1': {
                'раздел-2': {},
            }
        }
        reg = Registry(items)
        self.assertRaises(KeyError, reg.set, 'раздел-1', 'раздел-2', 100)
        self.assertTrue(reg.has_section('раздел-1', 'раздел-2'))

    def test_set_01(self):
        items = {}
        reg = Registry(items)
        reg.set('параметр', 100)

        self.assertTrue(reg.has_option('параметр'))
        self.assertEqual(reg.getint('параметр'), 100)

    def test_set_02(self):
        items = {
            'параметр': '111',
        }
        reg = Registry(items)
        reg.set('параметр', 100)

        self.assertTrue(reg.has_option('параметр'))
        self.assertEqual(reg.getint('параметр'), 100)

    def test_set_03(self):
        items = {
            'раздел-1': {
                'параметр': '111',
            }
        }
        reg = Registry(items)
        reg.set('раздел-1', 'параметр', 100)

        self.assertTrue(reg.has_option('раздел-1', 'параметр'))
        self.assertEqual(reg.getint('раздел-1', 'параметр'), 100)

    def test_set_04(self):
        items = {}
        reg = Registry(items)
        reg.set('раздел-1', 'параметр', 100)

        self.assertTrue(reg.has_option('раздел-1', 'параметр'))
        self.assertEqual(reg.getint('раздел-1', 'параметр'), 100)

    def test_set_05(self):
        items = {}
        reg = Registry(items)
        reg.set('раздел-1', 'раздел-2', 'параметр', 100)

        self.assertTrue(reg.has_option('раздел-1', 'раздел-2', 'параметр'))
        self.assertEqual(reg.getint('раздел-1', 'раздел-2', 'параметр'), 100)

    def test_get_subregistry_error_01(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get_subregistry)

    def test_get_subregistry_error_02(self):
        items = {}
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get_subregistry, 'раздел')

    def test_get_subregistry_error_03(self):
        items = {
            'параметр': 10,
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get_subregistry, 'параметр')

    def test_get_subregistry_error_04(self):
        items = {
            'раздел': {
                'параметр': 10,
            },
        }
        reg = Registry(items)

        self.assertRaises(KeyError, reg.get_subregistry, 'раздел', 'параметр')

    def test_get_subregistry_01(self):
        items = {
            'раздел': {
                'параметр': 10,
            },
        }
        reg = Registry(items)
        subreg = reg.get_subregistry('раздел')

        self.assertTrue(subreg.has_option('параметр'))

    def test_get_subregistry_02(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 10,
                },
            },
        }
        reg = Registry(items)
        subreg = reg.get_subregistry('раздел-1')

        self.assertTrue(subreg.has_option('раздел-2', 'параметр'))

    def test_get_subregistry_03_change(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 10,
                },
            },
        }
        reg = Registry(items)

        subreg = reg.get_subregistry('раздел-1')
        subreg.set('раздел-2', 'параметр', 1000)

        self.assertEqual(subreg.getint('раздел-2', 'параметр'), 1000)
        self.assertEqual(reg.getint('раздел-1', 'раздел-2', 'параметр'), 1000)

    def test_get_subregistry_04_change(self):
        items = {
            'раздел-1': {
                'раздел-2': {
                    'параметр': 10,
                },
            },
        }
        reg = Registry(items)

        subreg = reg.get_subregistry('раздел-1')
        subreg.create_section('раздел-2', 'раздел-3')

        self.assertTrue(reg.has_section('раздел-1', 'раздел-2', 'раздел-3'))
