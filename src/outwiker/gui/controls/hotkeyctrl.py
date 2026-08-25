# -*- coding: utf-8 -*-

import wx
from wx.lib.newevent import NewEvent

from outwiker.gui.hotkey import HotKey


HotkeyEditEvent, EVT_HOTKEY_EDIT = NewEvent()


class HotkeyCtrl(wx.TextCtrl):
    def __init__(self, parent, id=-1, value=None):
        super().__init__(parent, id)

        self.KEYMAP = {
            wx.WXK_BACK: "Back",
            wx.WXK_TAB: "Tab",
            wx.WXK_RETURN: "Enter",
            wx.WXK_ESCAPE: "Esc",
            wx.WXK_SPACE: "Space",
            wx.WXK_DELETE: "Delete",
            wx.WXK_CLEAR: "Clear",
            wx.WXK_MENU: "Menu",
            wx.WXK_PAUSE: "Pause",
            wx.WXK_END: "End",
            wx.WXK_HOME: "Home",
            wx.WXK_LEFT: "Left",
            wx.WXK_UP: "Up",
            wx.WXK_RIGHT: "Right",
            wx.WXK_DOWN: "Down",
            wx.WXK_SELECT: "Select",
            wx.WXK_PRINT: "Print",
            wx.WXK_INSERT: "Insert",
            wx.WXK_MULTIPLY: "*",
            wx.WXK_ADD: "+",
            wx.WXK_SUBTRACT: "-",
            wx.WXK_DECIMAL: ".",
            wx.WXK_DIVIDE: "/",
            wx.WXK_F1: "F1",
            wx.WXK_F2: "F2",
            wx.WXK_F3: "F3",
            wx.WXK_F4: "F4",
            wx.WXK_F5: "F5",
            wx.WXK_F6: "F6",
            wx.WXK_F7: "F7",
            wx.WXK_F8: "F8",
            wx.WXK_F9: "F9",
            wx.WXK_F10: "F10",
            wx.WXK_F11: "F11",
            wx.WXK_F12: "F12",
            wx.WXK_F13: "F13",
            wx.WXK_F14: "F14",
            wx.WXK_F15: "F15",
            wx.WXK_F16: "F16",
            wx.WXK_F17: "F17",
            wx.WXK_F18: "F18",
            wx.WXK_F19: "F19",
            wx.WXK_F20: "F20",
            wx.WXK_F21: "F21",
            wx.WXK_F22: "F22",
            wx.WXK_F23: "F23",
            wx.WXK_F24: "F24",
            wx.WXK_PAGEUP: "Pageup",
            wx.WXK_PAGEDOWN: "Pagedown",
            wx.WXK_NUMPAD_MULTIPLY: "*",
            wx.WXK_NUMPAD_ADD: "+",
            wx.WXK_NUMPAD_SUBTRACT: "-",
            wx.WXK_NUMPAD_DIVIDE: "/",
        }
        self.SetValue(value)
        self.Bind(wx.EVT_CHAR_HOOK, self._onKeyPressed)

    def _onKeyPressed(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()

        if keycode == wx.WXK_TAB and modifiers == 0:
            event.Skip()
            return

        if self._check(keycode):
            char = self._keycode2str(keycode)
            hotkey = HotKey(
                char, event.ControlDown(), event.AltDown(), event.ShiftDown()
            )

            if keycode == wx.WXK_BACK and modifiers == 0:
                hotkey = None
            self.SetValue(hotkey)

    def SetValue(self, value):
        super().SetValue(self._key2str(value))
        event = HotkeyEditEvent(hotkey=value)
        wx.PostEvent(self, event)

    def GetValue(self):
        text = super().GetValue()
        if len(text) == 0:
            return None

        ctrl = "Ctrl+" in text
        shift = "Shift+" in text
        alt = "Alt+" in text

        key = text.replace("Ctrl+", "")
        key = key.replace("Shift+", "")
        key = key.replace("Alt+", "")

        if len(key) == 0:
            return None

        return HotKey(key, ctrl, alt, shift)

    def GetText(self):
        return super(HotkeyCtrl, self).GetValue()

    def _key2str(self, hotkey):
        if hotkey is None:
            return ""

        result = ""
        if hotkey.ctrl:
            result += "Ctrl+"
        if hotkey.shift:
            result += "Shift+"
        if hotkey.alt:
            result += "Alt+"
        result += hotkey.key
        return result

    def _check(self, keycode):
        if keycode == 0:
            return False

        if keycode in self.KEYMAP:
            return True

        if keycode > 255:
            return False

        try:
            chr(keycode)
            return True
        except ValueError:
            return False

    def _keycode2str(self, keycode):
        if keycode in self.KEYMAP:
            return self.KEYMAP[keycode]
        return chr(keycode)
