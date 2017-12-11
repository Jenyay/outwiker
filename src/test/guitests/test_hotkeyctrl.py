# -*- coding: UTF-8 -*-

from .basemainwnd import BaseMainWndTest
from outwiker.core.application import Application
from outwiker.gui.controls.hotkeyctrl import HotkeyCtrl
from outwiker.gui.hotkey import HotKey


class HotkeyCtrlTest(BaseMainWndTest):

    def setUp(self):
        BaseMainWndTest.setUp(self)
        self._mainWnd = Application.mainWindow

    def test_empty(self):
        ctrl = HotkeyCtrl(self._mainWnd)
        self.assertEqual(ctrl.GetText(), u'')
        self.assertEqual(ctrl.GetValue(), None)

    def test_none_01(self):
        ctrl = HotkeyCtrl(self._mainWnd, -1, None)
        self.assertEqual(ctrl.GetText(), u'')
        self.assertEqual(ctrl.GetValue(), None)

    def test_none_02(self):
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(None)
        self.assertEqual(ctrl.GetText(), u'')
        self.assertEqual(ctrl.GetValue(), None)

    def test_key_01(self):
        hotkey = HotKey(u'X')
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), u'X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_02(self):
        hotkey = HotKey(u'X', ctrl=True)
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), u'Ctrl+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_03(self):
        hotkey = HotKey(u'X', shift=True)
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), u'Shift+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_04(self):
        hotkey = HotKey(u'X', alt=True)
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), u'Alt+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_05(self):
        hotkey = HotKey(u'X', ctrl=True, shift=True, alt=True)
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), u'Ctrl+Shift+Alt+X')
        self.assertEqual(ctrl.GetValue(), hotkey)

    def test_key_06(self):
        hotkey = HotKey(u'Home', ctrl=True, shift=True, alt=True)
        ctrl = HotkeyCtrl(self._mainWnd)
        ctrl.SetValue(hotkey)
        self.assertEqual(ctrl.GetText(), u'Ctrl+Shift+Alt+Home')
        self.assertEqual(ctrl.GetValue(), hotkey)
