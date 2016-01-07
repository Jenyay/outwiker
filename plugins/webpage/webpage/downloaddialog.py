# -*- coding: UTF-8 -*-

from threading import Event, Thread
from tempfile import mkdtemp
import urllib2
import os.path
from shutil import rmtree

import wx

from outwiker.core.tagslist import TagsList
from outwiker.gui.testeddialog import TestedDialog
from outwiker.gui.tagsselector import TagsSelector
from outwiker.core.commands import MessageBox

import events
from .downloader import Downloader, WebPageDownloadController
from webnotepage import STATIC_DIR_NAME, WebPageFactory


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
        self.SetTitle (_(u'Download web page'))
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
    def __init__ (self, dialog, application, parentPage):
        self._dialog = dialog
        self._application = application
        self._parentPage = parentPage

        self._downloadDir = None


        self._runEvent = Event()
        self._thread = None

        self._dialog.Bind (wx.EVT_BUTTON, self._onOk, id=wx.ID_OK)
        self._dialog.Bind (wx.EVT_BUTTON, self._onCancel, id=wx.ID_CANCEL)

        self._dialog.Bind (events.EVT_UPDATE_LOG, self._onLogUpdate)
        self._dialog.Bind (events.EVT_DOWNLOAD_ERROR, self._onDownloadError)
        self._dialog.Bind (events.EVT_DOWNLOAD_FINISH, self._onDownloadFinish)


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
        self._dialog.logText.ShowPosition (count)


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
        url = self._dialog.urlText.Value.strip()

        if len (url) == 0:
            MessageBox (_(u'Enter link for downloading'),
                        _(u"Error"),
                        wx.ICON_ERROR | wx.OK)
            self._dialog.urlText.SetFocus()
            return

        if self._thread is None:
            self._removeDownloadDir()
            self._downloadDir = mkdtemp (prefix=u'webpage_tmp_')

            self._runEvent.set()
            self._thread = DownloadThread (self._dialog,
                                           self._runEvent,
                                           self._downloadDir,
                                           url)
            self._thread.start()
        elif self._thread is not None:
            self._removeDownloadDir()
            event.Skip()


    def _onCancel (self, event):
        self._runEvent.clear()
        if self._thread is not None:
            self._thread.join()

        self._removeDownloadDir()
        event.Skip()


    def _onDownloadError (self, event):
        self._onLogUpdate (event)
        self._thread = None


    def _onDownloadFinish (self, event):
        parentPage = self._parentPage
        title = event.title
        tags = self._dialog.tagsSelector.tags
        content = event.content
        url = event.url
        tmpStaticDir = event.staticPath
        logContent = self._dialog.logText.Value

        page = WebPageFactory().createWebPage (parentPage,
                                               title,
                                               tags,
                                               content,
                                               url,
                                               tmpStaticDir,
                                               logContent)

        self._dialog.EndModal (wx.ID_OK)
        self._application.selectedPage = page


class DownloadThread (Thread):
    def __init__ (self, parentWnd, runEvent, downloadDir, url, name=None):
        super (DownloadThread, self).__init__ (name=name)
        self._parentWnd = parentWnd
        self._runEvent = runEvent
        self._downloadDir = downloadDir
        self._url = url

        # Timeout in seconds
        self._timeout = 20


    def run (self):
        controller = WebPageDownloadController (
            self._runEvent,
            self._downloadDir,
            STATIC_DIR_NAME,
            self._parentWnd,
            self._timeout
        )

        downloader = Downloader (self._timeout)

        self._log (_(u'Start downloading\n'))

        try:
            downloader.start (self._url, controller)
        except urllib2.URLError as error:
            self._error (_(u'Download error: {}\n').format (
                unicode (error.reason))
            )
        except ValueError:
            self._error (_(u'Invalid URL\n'))
        else:
            self._log (_(u'Finish downloading\n'))

            content = downloader.contentResult
            staticPath = os.path.join (self._downloadDir, STATIC_DIR_NAME)
            title = downloader.pageTitle

            finishEvent = events.FinishDownloadEvent (content=content,
                                                      staticPath=staticPath,
                                                      title=title,
                                                      url=self._url)
            wx.PostEvent (self._parentWnd, finishEvent)


    def _log (self, text):
        event = events.UpdateLogEvent (text=text)
        wx.PostEvent (self._parentWnd, event)


    def _error (self, text):
        event = events.ErrorDownloadEvent (text=text)
        wx.PostEvent (self._parentWnd, event)
