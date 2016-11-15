# -*- coding: utf-8 -*-

import wx

from outwiker.gui.hotkey import HotKey


HotkeyEditEvent, EVT_HOTKEY_EDIT = wx.lib.newevent.NewEvent()


class HotkeyCtrl(wx.TextCtrl):
    """
    Added in Outwiker 2.0.0.807.
    outwiker.gui 1.3
    """
    def __init__(self, parent, id=-1, value=None, pos=None, size=None):
        super(HotkeyCtrl, self).__init__(parent, id, pos=pos, size=size)

        self.KEYMAP = {
            wx.WXK_BACK: u'Back',
            wx.WXK_TAB: u'Tab',
            wx.WXK_RETURN: u'Enter',
            wx.WXK_ESCAPE: u'Esc',
            wx.WXK_SPACE: u'Space',
            wx.WXK_DELETE: u'Delete',
            wx.WXK_CLEAR: u'Clear',
            wx.WXK_MENU: u'Menu',
            wx.WXK_PAUSE: u'Pause',
            wx.WXK_END: u'End',
            wx.WXK_HOME: u'Home',
            wx.WXK_LEFT: u'Left',
            wx.WXK_UP: u'Up',
            wx.WXK_RIGHT: u'Right',
            wx.WXK_DOWN: u'Down',
            wx.WXK_SELECT: u'Select',
            wx.WXK_PRINT: u'Print',
            wx.WXK_INSERT: u'Insert',
            wx.WXK_MULTIPLY: u'*',
            wx.WXK_ADD: u'+',
            wx.WXK_SUBTRACT: u'-',
            wx.WXK_DECIMAL: u'.',
            wx.WXK_DIVIDE: u'/',
            wx.WXK_F1: u'F1',
            wx.WXK_F2: u'F2',
            wx.WXK_F3: u'F3',
            wx.WXK_F4: u'F4',
            wx.WXK_F5: u'F5',
            wx.WXK_F6: u'F6',
            wx.WXK_F7: u'F7',
            wx.WXK_F8: u'F8',
            wx.WXK_F9: u'F9',
            wx.WXK_F10: u'F10',
            wx.WXK_F11: u'F11',
            wx.WXK_F12: u'F12',
            wx.WXK_F13: u'F13',
            wx.WXK_F14: u'F14',
            wx.WXK_F15: u'F15',
            wx.WXK_F16: u'F16',
            wx.WXK_F17: u'F17',
            wx.WXK_F18: u'F18',
            wx.WXK_F19: u'F19',
            wx.WXK_F20: u'F20',
            wx.WXK_F21: u'F21',
            wx.WXK_F22: u'F22',
            wx.WXK_F23: u'F23',
            wx.WXK_F24: u'F24',
            wx.WXK_PAGEUP: u'Pageup',
            wx.WXK_PAGEDOWN: u'Pagedown',
            wx.WXK_NUMPAD_MULTIPLY: u'*',
            wx.WXK_NUMPAD_ADD: u'+',
            wx.WXK_NUMPAD_SUBTRACT: u'-',
            wx.WXK_NUMPAD_DIVIDE: u'/',
        }
        self.SetValue(value)
        self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPressed)

    def onKeyPressed(self, event):
        keycode = event.GetKeyCode()
        modifiers = event.GetModifiers()

        if keycode == wx.WXK_TAB and modifiers == 0:
            event.Skip()
            return

        if self._check(event):
            char = self._keycode2str(keycode)
            hotkey = HotKey(char,
                            event.ControlDown(),
                            event.AltDown(),
                            event.ShiftDown())

            if keycode == wx.WXK_BACK and modifiers == 0:
                hotkey = None
            self.SetValue(hotkey)

    def SetValue(self, value):
        super(HotkeyCtrl, self).SetValue(self._key2str(value))
        event = HotkeyEditEvent(hotkey=value)
        wx.PostEvent(self, event)

    def GetValue(self):
        text = super(HotkeyCtrl, self).GetValue()
        if len(text) == 0:
            return None

        ctrl = u'Ctrl+' in text
        shift = u'Shift+' in text
        alt = u'Alt+' in text

        key = text.replace(u'Ctrl+', u'')
        key = key.replace(u'Shift+', u'')
        key = key.replace(u'Alt+', u'')

        if len(key) == 0:
            return None

        return HotKey(key, ctrl, alt, shift)

    def GetText(self):
        return super(HotkeyCtrl, self).GetValue()

    def _key2str(self, hotkey):
        if hotkey is None:
            return u''

        result = u''
        if hotkey.ctrl:
            result += u'Ctrl+'
        if hotkey.shift:
            result += u'Shift+'
        if hotkey.alt:
            result += u'Alt+'
        result += hotkey.key
        return result

    def _check(self, event):
        keycode = event.GetKeyCode()

        if keycode in self.KEYMAP:
            return True

        try:
            chr(keycode)
            return True
        except ValueError:
            return False

    def _keycode2str(self, keycode):
        if keycode in self.KEYMAP:
            return self.KEYMAP[keycode]
        return unichr(keycode)
