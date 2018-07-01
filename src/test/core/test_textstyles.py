# -*- coding: utf-8 -*-

import unittest

from outwiker.core.textstyles import TextStylesStorage


class TextStylesStorageTest(unittest.TestCase):
    def test_empty_01(self):
        storage = TextStylesStorage()

        result_valid = {}

        self.assertEqual(storage.getStyles(), result_valid)
        self.assertEqual(storage.filterByTag('div'), result_valid)

    def test_empty_02(self):
        text = ''
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        result_valid = {}

        self.assertEqual(storage.getStyles(), result_valid)
        self.assertEqual(storage.filterByTag('div'), result_valid)

    def test_add_styles_01(self):
        text = 'div.red { color:red; }'
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        result_valid = {'div.red': 'div.red { color:red; }'}
        self.assertEqual(storage.getStyles(), result_valid)

    def test_add_styles_02(self):
        text = 'div.red { color:red; } div.blue { color:blue; }'
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        result_valid = {
            'div.red': 'div.red { color:red; }',
            'div.blue': 'div.blue { color:blue; }',
        }
        self.assertEqual(storage.getStyles(), result_valid)

    def test_add_styles_03(self):
        text = '''div.red { color:red; }

div.blue
{
color:blue;
}
'''
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        all_styles = storage.getStyles()
        self.assertEqual(len(all_styles), 2)

        self.assertEqual(all_styles['div.red'], 'div.red { color:red; }')
        self.assertEqual(all_styles['div.blue'], 'div.blue\n{\ncolor:blue;\n}')

    def test_add_styles_replace(self):
        text_1 = 'div.red { color:red; } div.blue { color:blue; }'
        text_2 = 'div.blue { color:yellow; }'
        storage = TextStylesStorage()
        storage.addStylesFromString(text_1)
        storage.addStylesFromString(text_2)

        result_valid = {
            'div.red': 'div.red { color:red; }',
            'div.blue': 'div.blue { color:yellow; }',
        }
        self.assertEqual(storage.getStyles(), result_valid)

    def test_filter_tag(self):
        text = 'div.red { color:red; } span.blue { color:blue; }'
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        self.assertEqual(len(storage.getStyles()), 2)
        self.assertEqual(storage.filterByTag('div'),
                         {'div.red': 'div.red { color:red; }'}
                         )

        self.assertEqual(storage.filterByTag('span'),
                         {'span.blue': 'span.blue { color:blue; }'}
                         )

    def test_filter_tag_upper(self):
        text = 'DIV.RED { color:red; } SPAN.BLUE { color:blue; }'
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        self.assertEqual(len(storage.getStyles()), 2)
        self.assertEqual(storage.filterByTag('div'),
                         {'DIV.RED': 'DIV.RED { color:red; }'}
                         )

        self.assertEqual(storage.filterByTag('span'),
                         {'SPAN.BLUE': 'SPAN.BLUE { color:blue; }'}
                         )

    def test_filter_tag_lower(self):
        text = 'div.red { color:red; } span.blue { color:blue; }'
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        self.assertEqual(len(storage.getStyles()), 2)
        self.assertEqual(storage.filterByTag('DIV'),
                         {'div.red': 'div.red { color:red; }'}
                         )

        self.assertEqual(storage.filterByTag('SPAN'),
                         {'span.blue': 'span.blue { color:blue; }'}
                         )

    def test_filter_tag_several(self):
        text = '''div.red { color:red; }
span.blue { color:blue; }
span.yellow { color:yellow; }
'''
        storage = TextStylesStorage()
        storage.addStylesFromString(text)

        self.assertEqual(len(storage.getStyles()), 3)
        self.assertEqual(storage.filterByTag('span'),
                         {
                             'span.blue': 'span.blue { color:blue; }',
                             'span.yellow': 'span.yellow { color:yellow; }',
                         }
                         )
