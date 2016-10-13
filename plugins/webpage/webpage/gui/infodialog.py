# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.testeddialog import TestedDialog

from webpage.i18n import get_


class InfoDialog(TestedDialog):
    """Dialog with Web page information(log, source url, etc)"""
    def __init__(self, parent):
        super(InfoDialog, self).__init__(parent)
        global _
        _ = get_()

        self._createGui()

    def _createGui(self):
        mainSizer = wx.FlexGridSizer(cols=1)
        mainSizer.AddGrowableCol(0)
        mainSizer.AddGrowableRow(2)

        self._addUrlGui(mainSizer)
        self._addLogGui(mainSizer)
        self._addOk(mainSizer)

        self.SetSizer(mainSizer)
        self.SetTitle(_(u'Web page information'))
        self.SetMinSize((550, 350))
        self.Fit()

    def _addLogGui(self, mainSizer):
        logLabel = wx.StaticText(self, label=_(u'Downloading log'))
        self.logText = wx.TextCtrl(self,
                                   style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.logText.SetMinSize((-1, 100))

        mainSizer.Add(logLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        mainSizer.Add(self.logText, 0, wx.ALL | wx.EXPAND, border=2)

    def _addUrlGui(self, mainSizer):
        sizer = wx.FlexGridSizer(cols=2)
        sizer.AddGrowableCol(1)

        self.urlLabel = wx.StaticText(self, label=_(u'Source URL'))
        self.urlText = wx.HyperlinkCtrl(self,
                                        -1,
                                        _(u'Link'),
                                        u'http://jenyay.net',
                                        style=wx.HL_ALIGN_LEFT | wx.NO_BORDER)

        sizer.Add(self.urlLabel,
                  0,
                  wx.ALL | wx.ALIGN_CENTER_VERTICAL,
                  border=2)
        sizer.Add(self.urlText, 0, wx.ALL | wx.EXPAND, border=2)

        mainSizer.Add(sizer, 0, wx.ALL | wx.EXPAND, border=2)

        self.urlLabel.Hide()
        self.urlText.Hide()

    def _addOk(self, mainSizer):
        buttonsSizer = self.CreateButtonSizer(wx.OK)
        mainSizer.Add(buttonsSizer,
                      0,
                      wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                      border=4)

    def setUrl(self, url):
        self.urlText.SetURL(url)
        self.urlText.SetLabel(url)

        self.urlLabel.Show()
        self.urlText.Show()

    def setLog(self, log):
        self.logText.SetValue(log)


class InfoDialogController(object):
    """Controller for InfoDialog"""
    def __init__(self, dialog, application, page):
        """
        Constructor.

        dalog - InfoDialog instance.
        application - Application.
        page - page(current) for info showing.
        """
        self._dialog = dialog
        self._application = application
        self._page = page

        self._downloadDir = None

    def showDialog(self):
        """
        The method show the info dialog and return result of the ShowModal()
        method
        """
        self._loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._saveState()

        return result

    def _loadState(self):
        url = self._page.source
        if url is not None:
            self._dialog.setUrl(url)

        self._dialog.setLog(self._page.log)

    def _saveState(self):
        pass
