# -*- coding: utf-8 -*-

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

from blockdiag.imagedraw.textfolder import splitlabel
from blockdiag.imagedraw.textfolder import splittext
from blockdiag.imagedraw.textfolder import truncate_text
from blockdiag.utils import Size
from blockdiag.utils.compat import u


CHAR_WIDTH = 14
CHAR_HEIGHT = 10


class Metrics(object):
    def textsize(self, text):
        length = len(text)
        return Size(CHAR_WIDTH * length, CHAR_HEIGHT)


class TestTextFolder(unittest.TestCase):
    def test_splitlabel(self):
        # single line text
        text = "abc"
        self.assertEqual(['abc'], list(splitlabel(text)))

        # text include \n (as char a.k.a. \x5c)
        text = "abc\ndef"
        self.assertEqual(['abc', 'def'], list(splitlabel(text)))

        # text include \n (as mac yensign a.k.a. \xa5)
        text = "abc\xa5ndef"
        self.assertEqual(['abc', 'def'], list(splitlabel(text)))

        # text includes \n (as text)
        text = "abc\\ndef"
        self.assertEqual(['abc', 'def'], list(splitlabel(text)))

        # text includes escaped \n
        text = "abc\\\\ndef"
        self.assertEqual(['abc\\ndef'], list(splitlabel(text)))

        # text includes escaped \n (\x5c and mac yensign mixed)
        if sys.version_info[0] == 2:
            text = u("abc\xa5\\\\ndef")
        else:
            text = u("abc\xa5\\ndef")
        self.assertEqual(['abc\\ndef'], list(splitlabel(text)))

        # text include \n and spaces
        text = " abc \n def "
        self.assertEqual(['abc', 'def'], list(splitlabel(text)))

        # text starts empty line
        text = " \nabc\ndef"
        self.assertEqual(['abc', 'def'], list(splitlabel(text)))

        # text starts empty line with \n (as text)
        text = " \\nabc\\ndef"
        self.assertEqual(['', 'abc', 'def'], list(splitlabel(text)))

    def test_splittext_width(self):
        metrics = Metrics()

        # just fit text
        text = "abc"
        ret = splittext(metrics, text, CHAR_WIDTH * 3)
        self.assertEqual(['abc'], ret)

        # text should be folded (once)
        text = "abcdef"
        ret = splittext(metrics, text, CHAR_WIDTH * 3)
        self.assertEqual(['abc', 'def'], ret)

        # text should be folded (twice)
        text = "abcdefghi"
        ret = splittext(metrics, text, CHAR_WIDTH * 3)
        self.assertEqual(['abc', 'def', 'ghi'], ret)

        # empty text
        text = ""
        ret = splittext(metrics, text, CHAR_WIDTH * 3)
        self.assertEqual([' '], ret)

    def test_truncate_text(self):
        metrics = Metrics()

        # truncated
        text = "abcdef"
        ret = truncate_text(metrics, text, CHAR_WIDTH * 8)
        self.assertEqual("abcd ...", ret)

        # truncated
        text = "abcdef"
        ret = truncate_text(metrics, text, CHAR_WIDTH * 5)
        self.assertEqual("a ...", ret)

        # not truncated (too short)
        text = "abcdef"
        ret = truncate_text(metrics, text, CHAR_WIDTH * 4)
        self.assertEqual("abcdef", ret)
