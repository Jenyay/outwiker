# -*- coding: utf-8 -*-

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import os
import tempfile
from blockdiag.utils.compat import u
from blockdiag.tests.utils import capture_stderr

from io import StringIO
from collections import namedtuple
from blockdiag.utils.fontmap import FontInfo, FontMap


FontElement = namedtuple('FontElement', 'fontfamily fontsize')


class TestUtilsFontmap(unittest.TestCase):
    def setUp(self):
        fontpath1 = __file__
        fontpath2 = os.path.join(os.path.dirname(__file__), 'utils.py')
        self.fontpath = [fontpath1, fontpath2]

    def test_fontinfo_new(self):
        FontInfo("serif", None, 11)
        FontInfo("sansserif", None, 11)
        FontInfo("monospace", None, 11)
        FontInfo("cursive", None, 11)
        FontInfo("fantasy", None, 11)

        FontInfo("serif-bold", None, 11)
        FontInfo("sansserif-italic", None, 11)
        FontInfo("monospace-oblique", None, 11)
        FontInfo("my-cursive", None, 11)
        FontInfo("-fantasy", None, 11)

    def test_fontinfo_invalid_familyname1(self):
        with self.assertRaises(AttributeError):
            FontInfo("unknown", None, 11)

    def test_fontinfo_invalid_familyname2(self):
        with self.assertRaises(AttributeError):
            FontInfo("sansserif-", None, 11)

    def test_fontinfo_invalid_familyname3(self):
        with self.assertRaises(AttributeError):
            FontInfo("monospace-unkown", None, 11)

    def test_fontinfo_invalid_familyname4(self):
        with self.assertRaises(AttributeError):
            FontInfo("cursive-bold-bold", None, 11)

    def test_fontinfo_invalid_familyname5(self):
        with self.assertRaises(AttributeError):
            FontInfo("SERIF", None, 11)

    def test_fontinfo_invalid_fontsize1(self):
        with self.assertRaises(TypeError):
            FontInfo("serif", None, None)

    def test_fontinfo_invalid_fontsize2(self):
        with self.assertRaises(ValueError):
            FontInfo("serif", None, '')

    def test_fontinfo_parse(self):
        font = FontInfo("serif", None, 11)
        self.assertEqual('', font.name)
        self.assertEqual('serif', font.generic_family)
        self.assertEqual('normal', font.weight)
        self.assertEqual('normal', font.style)

        font = FontInfo("sansserif-bold", None, 11)
        self.assertEqual('', font.name)
        self.assertEqual('sansserif', font.generic_family)
        self.assertEqual('bold', font.weight)
        self.assertEqual('normal', font.style)

        font = FontInfo("monospace-italic", None, 11)
        self.assertEqual('', font.name)
        self.assertEqual('monospace', font.generic_family)
        self.assertEqual('normal', font.weight)
        self.assertEqual('italic', font.style)

        font = FontInfo("my-cursive-oblique", None, 11)
        self.assertEqual('my', font.name)
        self.assertEqual('cursive', font.generic_family)
        self.assertEqual('normal', font.weight)
        self.assertEqual('oblique', font.style)

        font = FontInfo("my-fantasy-bold", None, 11)
        self.assertEqual('my', font.name)
        self.assertEqual('fantasy', font.generic_family)
        self.assertEqual('bold', font.weight)
        self.assertEqual('normal', font.style)

        font = FontInfo("serif-serif", None, 11)
        self.assertEqual('serif', font.name)
        self.assertEqual('serif', font.generic_family)
        self.assertEqual('normal', font.weight)
        self.assertEqual('normal', font.style)

    def test_fontinfo_familyname(self):
        font = FontInfo("serif", None, 11)
        self.assertEqual('serif-normal', font.familyname)

        font = FontInfo("sansserif-bold", None, 11)
        self.assertEqual('sansserif-bold', font.familyname)

        font = FontInfo("monospace-italic", None, 11)
        self.assertEqual('monospace-italic', font.familyname)

        font = FontInfo("my-cursive-oblique", None, 11)
        self.assertEqual('my-cursive-oblique', font.familyname)

        font = FontInfo("my-fantasy-bold", None, 11)
        self.assertEqual('my-fantasy-bold', font.familyname)

        font = FontInfo("serif-serif", None, 11)
        self.assertEqual('serif-serif-normal', font.familyname)

        font = FontInfo("-serif", None, 11)
        self.assertEqual('serif-normal', font.familyname)

    @capture_stderr
    def test_fontmap_empty_config(self):
        config = StringIO(u(""))
        fmap = FontMap(config)

        font1 = fmap.find()
        self.assertTrue(font1)
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual(None, font1.path)
        self.assertEqual(11, font1.size)

        element = FontElement('sansserif', 11)
        font2 = fmap.find(element)
        self.assertEqual(font1.familyname, font2.familyname)
        self.assertEqual(font1.path, font2.path)
        self.assertEqual(font1.size, font2.size)

        element = FontElement('sansserif-normal', 11)
        font3 = fmap.find(element)
        self.assertEqual(font1.familyname, font3.familyname)
        self.assertEqual(font1.path, font3.path)
        self.assertEqual(font1.size, font3.size)

        # non-registered familyname
        element = FontElement('my-sansserif-normal', 11)
        font4 = fmap.find(element)
        self.assertEqual(font1.familyname, font4.familyname)
        self.assertEqual(font1.path, font4.path)
        self.assertEqual(font1.size, font4.size)

    @capture_stderr
    def test_fontmap_none_config(self):
        fmap = FontMap()

        font1 = fmap.find()
        self.assertTrue(font1)
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual(None, font1.path)
        self.assertEqual(11, font1.size)

    def test_fontmap_normal_config(self):
        _config = u("[fontmap]\nsansserif: %s\nsansserif-bold: %s\n") % \
                  (self.fontpath[0], self.fontpath[1])
        config = StringIO(_config)
        fmap = FontMap(config)

        font1 = fmap.find()
        self.assertTrue(font1)
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual(self.fontpath[0], font1.path)
        self.assertEqual(11, font1.size)

        element = FontElement('sansserif', 11)
        font2 = fmap.find(element)
        self.assertEqual(font1.familyname, font2.familyname)
        self.assertEqual(font1.path, font2.path)
        self.assertEqual(font1.size, font2.size)

        element = FontElement('sansserif-normal', 11)
        font3 = fmap.find(element)
        self.assertEqual(font1.familyname, font3.familyname)
        self.assertEqual(font1.path, font3.path)
        self.assertEqual(font1.size, font3.size)

        element = FontElement('sansserif-bold', 11)
        font4 = fmap.find(element)
        self.assertEqual('sansserif-bold', font4.familyname)
        self.assertEqual(self.fontpath[1], font4.path)
        self.assertEqual(font1.size, font4.size)

        element = FontElement(None, None)
        font5 = fmap.find(element)
        self.assertEqual(font1.familyname, font5.familyname)
        self.assertEqual(font1.path, font5.path)
        self.assertEqual(font1.size, font5.size)

        element = object()
        font6 = fmap.find(element)
        self.assertEqual(font1.familyname, font6.familyname)
        self.assertEqual(font1.path, font6.path)
        self.assertEqual(font1.size, font6.size)

    def test_fontmap_duplicated_fontentry1(self):
        _config = u("[fontmap]\nsansserif: %s\nsansserif: %s\n") % \
                  (self.fontpath[0], self.fontpath[1])
        config = StringIO(_config)
        if sys.version_info[0] == 2:
            fmap = FontMap(config)

            font1 = fmap.find()
            self.assertEqual('sansserif', font1.generic_family)
            self.assertEqual(self.fontpath[1], font1.path)
            self.assertEqual(11, font1.size)
        else:
            import configparser
            with self.assertRaises(configparser.DuplicateOptionError):
                FontMap(config)

    def test_fontmap_duplicated_fontentry2(self):
        # this testcase is only for python2.6 or later
        if sys.version_info > (2, 6):
            _config = u("[fontmap]\nsansserif: %s\nsansserif-normal: %s\n") % \
                      (self.fontpath[0], self.fontpath[1])
            config = StringIO(_config)
            fmap = FontMap(config)

            font1 = fmap.find()
            self.assertEqual('sansserif', font1.generic_family)
            self.assertEqual(self.fontpath[1], font1.path)
            self.assertEqual(11, font1.size)

    def test_fontmap_with_capital_character(self):
        _config = u("[fontmap]\nCapitalCase-sansserif: %s\n") % \
                  self.fontpath[0]
        config = StringIO(_config)
        fmap = FontMap(config)

        element = FontElement('CapitalCase-sansserif', 11)
        font1 = fmap.find(element)
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual('capitalcase-sansserif-normal', font1.familyname)
        self.assertEqual(self.fontpath[0], font1.path)
        self.assertEqual(11, font1.size)

    @capture_stderr
    def test_fontmap_with_nodefault_fontentry(self):
        _config = u("[fontmap]\nserif: %s\n") % self.fontpath[0]
        config = StringIO(_config)
        fmap = FontMap(config)

        font1 = fmap.find()
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual(None, font1.path)
        self.assertEqual(11, font1.size)

        element = FontElement('serif', 11)
        font2 = fmap.find(element)
        self.assertEqual('serif', font2.generic_family)
        self.assertEqual(self.fontpath[0], font2.path)
        self.assertEqual(font1.size, font2.size)

        element = FontElement('fantasy', 20)
        font3 = fmap.find(element)
        self.assertEqual('sansserif', font3.generic_family)
        self.assertEqual(None, font3.path)
        self.assertEqual(20, font3.size)

    @capture_stderr
    def test_fontmap_with_nonexistence_fontpath(self):
        _config = u("[fontmap]\nserif: unknown_file\n")
        config = StringIO(_config)
        fmap = FontMap(config)

        font1 = fmap.find()
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual(None, font1.path)
        self.assertEqual(11, font1.size)

    def test_fontmap_switch_defaultfamily(self):
        _config = u("[fontmap]\nserif-bold: %s\n") % self.fontpath[0]
        config = StringIO(_config)
        fmap = FontMap(config)

        font1 = fmap.find()
        self.assertEqual('sansserif-normal', font1.familyname)
        self.assertEqual(None, font1.path)
        self.assertEqual(11, font1.size)

        fmap.set_default_fontfamily('serif-bold')
        font2 = fmap.find()
        self.assertEqual('serif-bold', font2.familyname)
        self.assertEqual(self.fontpath[0], font2.path)
        self.assertEqual(11, font2.size)

        fmap.set_default_fontfamily('fantasy-italic')
        font3 = fmap.find()
        self.assertEqual('fantasy-italic', font3.familyname)
        self.assertEqual(None, font3.path)
        self.assertEqual(11, font3.size)

        fmap.fontsize = 20
        font4 = fmap.find()
        self.assertEqual('fantasy-italic', font4.familyname)
        self.assertEqual(None, font4.path)
        self.assertEqual(20, font4.size)

    def test_fontmap_using_fontalias(self):
        _config = (u("[fontmap]\nserif-bold: %s\n") +
                   u("[fontalias]\ntest = serif-bold\n")) % self.fontpath[0]
        config = StringIO(_config)
        fmap = FontMap(config)

        element = FontElement('test', 20)
        font1 = fmap.find(element)
        self.assertEqual('serif-bold', font1.familyname)
        self.assertEqual(self.fontpath[0], font1.path)
        self.assertEqual(20, font1.size)

    def test_fontmap_by_file(self):
        tmp = tempfile.mkstemp()

        _config = u("[fontmap]\nsansserif: %s\nsansserif-bold: %s\n") % \
                  (self.fontpath[0], self.fontpath[1])

        fp = os.fdopen(tmp[0], 'wt')
        fp.write(_config)
        fp.close()
        fmap = FontMap(tmp[1])

        font1 = fmap.find()
        self.assertTrue(font1)
        self.assertEqual('sansserif', font1.generic_family)
        self.assertEqual(self.fontpath[0], font1.path)
        self.assertEqual(11, font1.size)

        os.unlink(tmp[1])

    def test_fontmap_including_bom_by_file(self):
        tmp = tempfile.mkstemp()

        _config = (u("[fontmap]\nsansserif: %s\n") +
                   u("sansserif-bold: %s\n")) % \
                  (self.fontpath[0], self.fontpath[1])

        try:
            fp = os.fdopen(tmp[0], 'wb')
            fp.write(_config.encode('utf-8-sig'))
            fp.close()
            fmap = FontMap(tmp[1])

            font1 = fmap.find()
            self.assertTrue(font1)
            self.assertEqual('sansserif', font1.generic_family)
            self.assertEqual(self.fontpath[0], font1.path)
            self.assertEqual(11, font1.size)
        finally:
            os.unlink(tmp[1])
