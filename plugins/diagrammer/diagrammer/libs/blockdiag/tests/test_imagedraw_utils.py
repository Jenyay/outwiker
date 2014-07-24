# -*- coding: utf-8 -*-

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from blockdiag.imagedraw.utils import (
    is_zenkaku, zenkaku_len, hankaku_len,
    string_width, textsize
)
from blockdiag.utils.compat import u


class TestUtils(unittest.TestCase):
    def test_is_zenkaku(self):
        # A
        self.assertEqual(False, is_zenkaku(u("A")))
        # あ
        self.assertEqual(True, is_zenkaku(u("\u3042")))

    def test_zenkaku_len(self):
        # abc
        self.assertEqual(0, zenkaku_len(u("abc")))
        # あいう
        self.assertEqual(3, zenkaku_len(u("\u3042\u3044\u3046")))
        # あいc
        self.assertEqual(2, zenkaku_len(u("\u3042\u3044c")))

    def test_hankaku_len(self):
        # abc
        self.assertEqual(3, hankaku_len(u("abc")))
        # あいう
        self.assertEqual(0, hankaku_len(u("\u3042\u3044\u3046")))
        # あいc
        self.assertEqual(1, hankaku_len(u("\u3042\u3044c")))

    def test_string_width(self):
        # abc
        self.assertEqual(3, string_width(u("abc")))
        # あいう
        self.assertEqual(6, string_width(u("\u3042\u3044\u3046")))
        # あいc
        self.assertEqual(5, string_width(u("\u3042\u3044c")))

    def test_test_textsize(self):
        from blockdiag.utils.fontmap import FontInfo
        font = FontInfo('serif', None, 11)

        # abc
        self.assertEqual((19, 11), textsize(u("abc"), font))
        # あいう
        self.assertEqual((33, 11), textsize(u("\u3042\u3044\u3046"), font))
        # あいc
        self.assertEqual((29, 11), textsize(u("\u3042\u3044c"), font))

        # abc
        font = FontInfo('serif', None, 24)
        self.assertEqual((40, 24), textsize(u("abc"), font))

        # あいう
        font = FontInfo('serif', None, 18)
        self.assertEqual((54, 18), textsize(u("\u3042\u3044\u3046"), font))
