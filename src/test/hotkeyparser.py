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
