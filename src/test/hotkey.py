#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.gui.hotkey import HotKey


class HotKeyTest (unittest.TestCase):
    def setUp (self):
        pass


    def tearDown (self):
        pass


    def testHotKey1 (self):
        hotkey = HotKey (u"F1")

        self.assertEqual (hotkey.key, u"F1")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.alt)
        self.assertFalse (hotkey.shift)


    def testHotKey2 (self):
        hotkey = HotKey (u"F1", ctrl=True)

        self.assertEqual (hotkey.key, u"F1")
        self.assertTrue (hotkey.ctrl)
        self.assertFalse (hotkey.alt)
        self.assertFalse (hotkey.shift)


    def testHotKey3 (self):
        hotkey = HotKey (u"F1", alt=True)

        self.assertEqual (hotkey.key, u"F1")
        self.assertFalse (hotkey.ctrl)
        self.assertTrue (hotkey.alt)
        self.assertFalse (hotkey.shift)


    def testHotKey4 (self):
        hotkey = HotKey (u"F1", shift=True)

        self.assertEqual (hotkey.key, u"F1")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.alt)
        self.assertTrue (hotkey.shift)


    def testHotKey5 (self):
        hotkey = HotKey (u"F1", ctrl=True, alt=True, shift=True)

        self.assertEqual (hotkey.key, u"F1")
        self.assertTrue (hotkey.ctrl)
        self.assertTrue (hotkey.alt)
        self.assertTrue (hotkey.shift)
