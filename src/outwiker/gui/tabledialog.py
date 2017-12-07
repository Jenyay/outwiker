# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog


class TableDialog (TestedDialog):
    def __init__ (self, parent):
        super (TableDialog, self).__init__ (parent)
        self._SPIN_SIZE = 150
        self._createGui()

        self.SetTitle (_(u'Insert table'))


    @property
    def colsCount (self):
        return self._colsCount.GetValue()


    @colsCount.setter
    def colsCount (self, value):
        self._colsCount.SetValue (value)


    @property
    def rowsCount (self):
        return self._rowsCount.GetValue()


    @rowsCount.setter
    def rowsCount (self, value):
        self._rowsCount.SetValue (value)


    @property
    def borderWidth (self):
        return self._border.GetValue()


    @borderWidth.setter
    def borderWidth (self, value):
        self._border.SetValue (value)


    @property
    def headerCells (self):
        return self._headerCells.GetValue()


    @headerCells.setter
    def headerCells (self, value):
        self._headerCells.SetValue (value)


    def _createTextAndSpin (self, parent, label, sizer):
        label = wx.StaticText (parent, label=label)
        spin = wx.SpinCtrl (parent)
        spin.SetRange (1, 100)
        spin.SetMinSize ((self._SPIN_SIZE, -1))

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
        mainSizer.AddGrowableRow (2)

        sizeSizer = wx.FlexGridSizer (cols=2)
        sizeSizer.AddGrowableCol (0)
        sizeSizer.AddGrowableCol (1)

        self._colsCount = self._createTextAndSpin (self, _(u'Columns count'), sizeSizer)
        self._colsCount.SetValue (1)

        self._rowsCount = self._createTextAndSpin (self, _(u'Rows count'), sizeSizer)
        self._rowsCount.SetValue (1)

        mainSizer.Add (sizeSizer,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)

        mainSizer.AddSpacer (10)
        self._createAdvancedControls (mainSizer)

        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.Add (okCancel, 1, wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM, border = 2)

        self.SetSizer(mainSizer)
        self.Fit()


    def _createAdvancedControls (self, mainSizer):
        advancedPanel = wx.CollapsiblePane (self, label=_(u'Advanced'))
        pane = advancedPanel.GetPane()

        paneSizer = wx.FlexGridSizer (cols=1)
        paneSizer.AddGrowableCol (0)

        borderSizer = wx.FlexGridSizer (cols=2)
        borderSizer.AddGrowableCol (0)
        borderSizer.AddGrowableCol (1)

        self._border = self._createTextAndSpin (pane, _(u'Border width'), borderSizer)
        self._border.SetRange (0, 100)
        self._border.SetValue (1)

        self._headerCells = wx.CheckBox (
            pane,
            label = _(u'Header cells for first row')
        )

        paneSizer.Add (
            borderSizer,
            1,
            flag = wx.ALL | wx.EXPAND,
            border = 2
        )

        paneSizer.Add (
            self._headerCells,
            1,
            flag = wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            border = 2
        )

        pane.SetSizer (paneSizer)

        mainSizer.Add (advancedPanel,
                       flag = wx.ALL | wx.EXPAND,
                       border = 2)
