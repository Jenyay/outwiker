# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.hotkeyparser import HotKeyParser
from outwiker.gui.hotkey import HotKey


class HotKeyParserTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testToString(self):
        self.assertEqual(HotKeyParser.toString(HotKey("A")), "A")
        self.assertEqual(HotKeyParser.toString(HotKey("F1")), "F1")

        self.assertEqual(HotKeyParser.toString(HotKey("A", ctrl=True)),
                         "Ctrl+A")

        self.assertEqual(HotKeyParser.toString(HotKey("A", shift=True)),
                         "Shift+A")

        self.assertEqual(HotKeyParser.toString(HotKey("A", alt=True)),
                         "Alt+A")

        self.assertEqual(HotKeyParser.toString(
            HotKey("A", ctrl=True, alt=True)),
            "Ctrl+Alt+A")

        self.assertEqual(HotKeyParser.toString(
            HotKey("A", ctrl=True, shift=True)),
            "Ctrl+Shift+A")

        self.assertEqual(HotKeyParser.toString(
            HotKey("A", alt=True, shift=True)),
            "Shift+Alt+A")

        self.assertEqual(HotKeyParser.toString(
            HotKey("A", ctrl=True, alt=True, shift=True)),
            "Ctrl+Shift+Alt+A")

    def testParse1(self):
        hotkey = HotKeyParser.fromString("A")

        self.assertEqual(hotkey.key, "A")
        self.assertFalse(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse2(self):
        hotkey = HotKeyParser.fromString("F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertFalse(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse3(self):
        hotkey = HotKeyParser.fromString("Shift+A")

        self.assertEqual(hotkey.key, "A")
        self.assertFalse(hotkey.ctrl)
        self.assertTrue(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse4(self):
        hotkey = HotKeyParser.fromString("Alt+A")

        self.assertEqual(hotkey.key, "A")
        self.assertFalse(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertTrue(hotkey.alt)

    def testParse5(self):
        hotkey = HotKeyParser.fromString("Shift+Alt+Ctrl+F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertTrue(hotkey.ctrl)
        self.assertTrue(hotkey.shift)
        self.assertTrue(hotkey.alt)

    def testParse6(self):
        self.assertIsNone(HotKeyParser.fromString(""))

    def testParse7(self):
        hotkey = HotKeyParser.fromString("+")

        self.assertEqual(hotkey.key, "+")
        self.assertFalse(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse8(self):
        hotkey = HotKeyParser.fromString("Ctrl++")

        self.assertEqual(hotkey.key, "+")
        self.assertTrue(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse9(self):
        hotkey = HotKeyParser.fromString("ShIfT+ALT+ctrl+F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertTrue(hotkey.ctrl)
        self.assertTrue(hotkey.shift)
        self.assertTrue(hotkey.alt)

    def testParse10(self):
        hotkey = HotKeyParser.fromString("Ctrl + F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertTrue(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse11(self):
        hotkey = HotKeyParser.fromString("Ctrl + Shift + F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertTrue(hotkey.ctrl)
        self.assertTrue(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse12(self):
        hotkey = HotKeyParser.fromString(" Alt + F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertFalse(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertTrue(hotkey.alt)

    def testParse13(self):
        hotkey = HotKeyParser.fromString(" Ctrl + F1 ")

        self.assertEqual(hotkey.key, "F1")
        self.assertTrue(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParse14(self):
        self.assertIsNone(HotKeyParser.fromString("    "))

    def testParse15(self):
        hotkey = HotKeyParser.fromString("Ctrl+F1")

        self.assertEqual(hotkey.key, "F1")
        self.assertTrue(hotkey.ctrl)
        self.assertFalse(hotkey.shift)
        self.assertFalse(hotkey.alt)

    def testParseInvalid_01(self):
        self.assertIsNone(HotKeyParser.fromString("Ctrl+"))

    def testParseInvalid_02(self):
        self.assertIsNone(HotKeyParser.fromString("Ctrl+Shift+"))

    def testParseInvalid_03(self):
        self.assertIsNone(HotKeyParser.fromString("Ctrl+Shift+Alt+"))

    def testParseInvalid_04(self):
        self.assertIsNone(HotKeyParser.fromString("asdfasd Абырвалг"))
