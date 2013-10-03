#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.gui.hotkeyparser import HotKeyParser
from outwiker.gui.hotkey import HotKey


class HotKeyParserTest (unittest.TestCase):
    def setUp (self):
        self.parser = HotKeyParser()


    def tearDown (self):
        pass


    def testToString (self):
        self.assertEqual (self.parser.toString (HotKey (u"A")), u"A")
        self.assertEqual (self.parser.toString (HotKey (u"F1")), u"F1")

        self.assertEqual (self.parser.toString (HotKey (u"A", ctrl=True)), 
                u"Ctrl+A")

        self.assertEqual (self.parser.toString (HotKey (u"A", shift=True)), 
                u"Shift+A")

        self.assertEqual (self.parser.toString (HotKey (u"A", alt=True)), 
                u"Alt+A")

        self.assertEqual (self.parser.toString (HotKey (u"A", ctrl=True, alt=True)), 
                u"Ctrl+Alt+A")

        self.assertEqual (self.parser.toString (HotKey (u"A", ctrl=True, shift=True)), 
                u"Ctrl+Shift+A")

        self.assertEqual (self.parser.toString (HotKey (u"A", alt=True, shift=True)), 
                u"Shift+Alt+A")

        self.assertEqual (self.parser.toString (HotKey (u"A", ctrl=True, alt=True, shift=True)), 
                u"Ctrl+Shift+Alt+A")


    def testParse1 (self):
        hotkey = self.parser.fromString (u"A")

        self.assertEqual (hotkey.key, "A")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse2 (self):
        hotkey = self.parser.fromString (u"F1")

        self.assertEqual (hotkey.key, "F1")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse2 (self):
        hotkey = self.parser.fromString (u"Ctrl+F1")

        self.assertEqual (hotkey.key, "F1")
        self.assertTrue (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse3 (self):
        hotkey = self.parser.fromString (u"Shift+A")

        self.assertEqual (hotkey.key, "A")
        self.assertFalse (hotkey.ctrl)
        self.assertTrue (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse4 (self):
        hotkey = self.parser.fromString (u"Alt+A")

        self.assertEqual (hotkey.key, "A")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertTrue (hotkey.alt)


    def testParse5 (self):
        hotkey = self.parser.fromString (u"Shift+Alt+Ctrl+F1")

        self.assertEqual (hotkey.key, "F1")
        self.assertTrue (hotkey.ctrl)
        self.assertTrue (hotkey.shift)
        self.assertTrue (hotkey.alt)


    def testParse6 (self):
        hotkey = self.parser.fromString (u"")

        self.assertEqual (hotkey.key, u"")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse7 (self):
        hotkey = self.parser.fromString (u"+")

        self.assertEqual (hotkey.key, u"+")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse8 (self):
        hotkey = self.parser.fromString (u"Ctrl++")

        self.assertEqual (hotkey.key, u"+")
        self.assertTrue (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse9 (self):
        hotkey = self.parser.fromString (u"ShIfT+ALT+ctrl+F1")

        self.assertEqual (hotkey.key, "F1")
        self.assertTrue (hotkey.ctrl)
        self.assertTrue (hotkey.shift)
        self.assertTrue (hotkey.alt)


    def testParse10 (self):
        hotkey = self.parser.fromString (u"Ctrl + F1")

        self.assertEqual (hotkey.key, u"F1")
        self.assertTrue (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse11 (self):
        hotkey = self.parser.fromString (u"Ctrl + Shift + F1")

        self.assertEqual (hotkey.key, u"F1")
        self.assertTrue (hotkey.ctrl)
        self.assertTrue (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse12 (self):
        hotkey = self.parser.fromString (u" Alt + F1")

        self.assertEqual (hotkey.key, u"F1")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertTrue (hotkey.alt)


    def testParse13 (self):
        hotkey = self.parser.fromString (u" Ctrl + F1 ")

        self.assertEqual (hotkey.key, u"F1")
        self.assertTrue (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParse14 (self):
        hotkey = self.parser.fromString (u"    ")

        self.assertEqual (hotkey.key, u"")
        self.assertFalse (hotkey.ctrl)
        self.assertFalse (hotkey.shift)
        self.assertFalse (hotkey.alt)


    def testParseInvalid1 (self):
        self.assertRaises (ValueError, self.parser.fromString, u"Ctrl+")


    def testParseInvalid2 (self):
        self.assertRaises (ValueError, self.parser.fromString, u"Ctrl+Shift+")


    def testParseInvalid2 (self):
        self.assertRaises (ValueError, self.parser.fromString, u"Ctrl+Shift+Alt+")
