# -*- coding: UTF-8 -*-

from threading import Event, Thread
from tempfile import mkdtemp
from shutil import rmtree

import wx

from outwiker.core.tagslist import TagsList
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.tagsselector import TagsSelector
from outwiker.core.commands import MessageBox

UpdateLogEvent, EVT_UPDATE_LOG = wx.lib.newevent.NewEvent()
ErrorDownloadEvent, EVT_DOWNLOAD_ERROR = wx.lib.newevent.NewEvent()
FinishDownloadEvent, EVT_DOWNLOAD_FINISH = wx.lib.newevent.NewEvent()

# Directory for images, scripts, css etc.
STATIC_DIR_NAME = u'__download'


class DownloadDialog (TestedDialog):
    def __init__ (self, parent):
        super (DownloadDialog, self).__init__ (parent)
        self._createGui()
        self.urlText.SetFocus()


    def _createGui (self):
        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)
        mainSizer.AddGrowableRow (1)
        mainSizer.AddGrowableRow (2)

        self._addUrlGui (mainSizer)
        self._addTagsList (mainSizer)
        self._addLogGui (mainSizer)
        self._addOkCancel (mainSizer)

        self.SetSizer (mainSizer)
        self.SetTitle (_(u'Download page'))
        self.SetMinSize ((500, 350))
        self.Fit()


    def _addUrlGui (self, mainSizer):
        urlSizer = wx.FlexGridSizer (cols=2)
        urlSizer.AddGrowableCol (1)

        urlLabel = wx.StaticText (self, label = _(u'Link'))
        self.urlText = wx.TextCtrl (self)

        urlSizer.Add (urlLabel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=2)
        urlSizer.Add (self.urlText, 0, wx.ALL | wx.EXPAND, border=2)

        mainSizer.Add (urlSizer, 0, wx.ALL | wx.EXPAND, border=2)


    def _addTagsList (self, mainSizer):
        self.tagsSelector = TagsSelector (self)
        mainSizer.Add (self.tagsSelector, 0, wx.EXPAND, 0)


    def _addLogGui (self, mainSizer):
        self.logText = wx.TextCtrl (self,
                                    style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.logText.SetMinSize ((-1, 100))
        mainSizer.Add (self.logText, 0, wx.EXPAND, 0)


    def _addOkCancel (self, mainSizer):
        buttonsSizer = self.CreateButtonSizer (wx.OK | wx.CANCEL)
        mainSizer.Add (buttonsSizer,
                       0,
                       wx.ALIGN_RIGHT | wx.ALIGN_BOTTOM | wx.ALL,
                       border = 4)


    def setTagsList (self, tagslist):
        self.tagsSelector.setTagsList (tagslist)



class DownloadDialogController (object):
    def __init__ (self, dialog, application):
        self._dialog = dialog
        self._application = application

        self._downloadDir = None


        self._runEvent = Event()
        self._thread = None

        self._dialog.Bind (wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
        self._dialog.Bind (wx.EVT_BUTTON, self._onCancel, id=wx.ID_CANCEL)

        self._dialog.Bind (EVT_UPDATE_LOG, self._onLogUpdate)
        self._dialog.Bind (EVT_DOWNLOAD_ERROR, self._onDownloadError)
        self._dialog.Bind (EVT_DOWNLOAD_FINISH, self._onDownloadFinish)


    def showDialog (self):
        """
        The method show the dialog and return result of the ShowModal() method
        """
        if self._application.wikiroot is None:
            return

        self._loadState()

        result = self._dialog.ShowModal()
        if result == wx.ID_OK:
            self._saveState()

        return result


    def addToLog (self, text):
        self._dialog.logText.Value += text

        count = len (self._dialog.logText.Value)
        self._dialog.logText.SetSelection (count, count)
        self._dialog.logText.SetFocus()


    def _loadState (self):
        tagslist = TagsList (self._application.wikiroot)
        self._dialog.setTagsList (tagslist)


    def _saveState (self):
        pass


    def _onLogUpdate (self, event):
        self.addToLog (event.text)


    def _removeDownloadDir (self):
        if self._downloadDir is not None:
            try:
                rmtree (self._downloadDir)
            except EnvironmentError:
                self.addToLog (_(u"Can't remove temp directory"))


    def _onOk (self, event):
        if len (self._dialog.urlText.Value.strip()) == 0:
            MessageBox (_(u'Enter url for downloading'),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            self._dialog.urlText.SetFocus()
            return

        if self._thread is None:
            self._removeDownloadDir()
            self._downloadDir = mkdtemp (prefix=u'webpage_tmp_')

            self._runEvent.clear()
            self._thread = DownloadThread (self._dialog,
                                           self._runEvent,
                                           self._downloadDir)
            self._thread.start()
        elif self._thread is not None:
            self._removeDownloadDir()
            event.Skip()


    def _onCancel (self, event):
        self._runEvent.set()
        if self._thread is not None:
            self._thread.join()

        self._removeDownloadDir()
        event.Skip()


    def _onDownloadError (self, event):
        self._onLogUpdate (event.text)
        self._thread = None


    def _onDownloadFinish (self, event):
        pass



class DownloadThread (Thread):
    def __init__ (self, parentWnd, runEvent, downloadDir, name=None):
        super (DownloadThread, self).__init__ (name=name)
        self._parentWnd = parentWnd
        self._runEvent = runEvent
        self._downloadDir = downloadDir

        # Timeout in seconds
        self._timeout = 20


    def run (self):
        self._log (_(u'Start downloading\n'))

        self._log (_(u'Finish downloading\n'))
        finishEvent = FinishDownloadEvent ()
        wx.PostEvent (self._parentWnd, finishEvent)


    def _log (self, text):
        event = UpdateLogEvent (text=text)
        wx.PostEvent (self._parentWnd, event)
