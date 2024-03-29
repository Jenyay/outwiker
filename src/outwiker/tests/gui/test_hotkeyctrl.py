# -*- coding: utf-8 -*-

import unittest

from outwiker.gui.controls.hotkeyctrl import HotkeyCtrl
from outwiker.gui.hotkey import HotKey
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class HotkeyCtrlTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

    def tearDown(self):
        self.destroyApplication()

    def test_empty(self):
        ctrl = HotkeyCtrl(self.mainWindow)
        self.assertEqual(ctrl.GetText(), '')
        self.assertEqual(ctrl.GetValue(), None)

    def test_none_01(self):
        ctrl = HotkeyCtrl(self.mainWindow, -1, None)
        self.assertEqual(ctrl.GetText(), '')
        self.assertEqual(ctrl.GetValue(), None)

    def test_none_02(self):
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(None)
        self.assertEqual(ctrl.GetText(), '')
        self.assertEqual(ctrl.GetValue(), None)

    def test_key_01(self):
        hotkey = HotKey('X')
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), 'X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_02(self):
        hotkey = HotKey('X', ctrl=True)
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), 'Ctrl+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_03(self):
        hotkey = HotKey('X', shift=True)
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), 'Shift+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_04(self):
        hotkey = HotKey('X', alt=True)
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), 'Alt+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_05(self):
        hotkey = HotKey('X', ctrl=True, shift=True, alt=True)
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), 'Ctrl+Shift+Alt+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_06(self):
        hotkey = HotKey('Home', ctrl=True, shift=True, alt=True)
        ctrl = HotkeyCtrl(self.mainWindow)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), 'Ctrl+Shift+Alt+Home')
        self.assertEqual(ctrl.GetValue(), hotkey)
