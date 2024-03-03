import wx
import wx.stc

from outwiker.gui.htmltexteditor import HtmlTextEditor

class HtmlCodeView(HtmlTextEditor):
    def setDefaultSettings(self):
        super().setDefaultSettings()
        self._setHotkeys()

    def _setHotkeys(self):
        defaultHotKeys = (
            (ord("A"), wx.stc.STC_SCMOD_CTRL, wx.stc.STC_CMD_SELECTALL),
            (wx.stc.STC_KEY_INSERT, wx.stc.STC_SCMOD_CTRL, wx.stc.STC_CMD_COPY),
            (wx.stc.STC_KEY_DELETE, wx.stc.STC_SCMOD_SHIFT, wx.stc.STC_CMD_CUT),
            (ord("C"), wx.stc.STC_SCMOD_CTRL, wx.stc.STC_CMD_COPY),
            (ord("X"), wx.stc.STC_SCMOD_CTRL, wx.stc.STC_CMD_CUT),
                )
        [self.textCtrl.CmdKeyAssign(*key) for key in defaultHotKeys]
