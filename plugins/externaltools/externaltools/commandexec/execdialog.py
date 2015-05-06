# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog

from externaltools.i18n import get_


class ExecDialog (TestedDialog):
    def __init__ (self, parent):
        super (ExecDialog, self).__init__(parent)

        global _
        _ = get_()

        self._formats = [_(u'Link'), _(u'Button')]

        self.SetTitle (_(u'Inserting (:exec:) command'))
        self._createGui ()
        self._titleTextBox.SetFocus()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=2)
        mainSizer.AddGrowableCol (1)
        mainSizer.AddGrowableRow (2)

        # Title
        titleLabel = wx.StaticText (self, -1, _(u'Title'))

        self._titleTextBox = wx.TextCtrl (self)
        self._titleTextBox.SetMinSize ((250, -1))

        mainSizer.Add (
            titleLabel,
            flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border = 2
        )

        mainSizer.Add (
            self._titleTextBox,
            flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL,
            border = 2
        )

        # Format (link or button)
        formatLabel = wx.StaticText (self, -1, _(u'Format'))

        self._formatCombo = wx.ComboBox (
            self,
            -1,
            style = wx.CB_DROPDOWN | wx.CB_READONLY
        )
        self._formatCombo.SetMinSize ((250, -1))
        self._formatCombo.SetItems (self._formats)
        self._formatCombo.SetSelection (0)

        mainSizer.Add (
            formatLabel,
            flag = wx.ALIGN_CENTER_VERTICAL | wx.ALL,
            border = 2
        )

        mainSizer.Add (
            self._formatCombo,
            flag = wx.ALIGN_RIGHT | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND | wx.ALL,
            border = 2
        )


        okCancel = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.AddStretchSpacer ()
        mainSizer.Add (okCancel,
                       1,
                       wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                       border = 2)

        self.SetSizer (mainSizer)
        self.Fit()


    @property
    def title (self):
        return self._titleTextBox.GetValue()


    @title.setter
    def title (self, value):
        self._titleTextBox.SetValue (value)


    @property
    def format (self):
        return self._formatCombo.GetSelection()


    @format.setter
    def format (self, value):
        self._formatCombo.SetSelection (value)
