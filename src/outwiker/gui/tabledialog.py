# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class TableDialog (TestedDialog):
    def __init__ (self, parent):
        super (TableDialog, self).__init__ (parent)
        self._createGui()

        self.SetTitle (_(u'Insert table'))


    def _createTextAndSpin (self, label, sizer):
        label = wx.StaticText (self, label=label)
        spin = wx.SpinCtrl (self)
        spin.SetRange (1, 100)
        spin.SetValue (1)
        spin.SetMinSize ((150, -1))

        sizer.Add (label,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                   border = 2)

        sizer.Add (spin,
                   flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
                   border = 2)

        return spin


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        sizeSizer = wx.FlexGridSizer (cols=2)
        sizeSizer.AddGrowableCol (0)
        sizeSizer.AddGrowableCol (1)

        self._colsCount = self._createTextAndSpin (_(u'Columns count'), sizeSizer)
        self._rowsCount = self._createTextAndSpin (_(u'Rows count'), sizeSizer)

        mainSizer.Add (sizeSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)

        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.Add (okCancel, 1, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border = 2)

        self.SetSizer(mainSizer)
        self.Fit()
