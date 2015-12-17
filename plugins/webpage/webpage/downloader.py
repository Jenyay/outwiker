# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import urllib2
from urlparse import urljoin

import wx

from bs4 import BeautifulSoup
from events import UpdateLogEvent


class Downloader (object):
    def __init__ (self, timeout=20):
        self._timeout = 20

        self._contentSrc = None
        self._pageTitle = None
        self._soup = None

        self._contentResult = None


    def start (self, url, controller):
        obj = urllib2.urlopen (url, timeout=self._timeout)
        self._soup = BeautifulSoup(obj.read(), "html.parser")
        self._contentSrc = self._soup.prettify()

        if self._soup.title is not None:
            self._pageTitle = self._soup.title.string

        images = self._soup.find_all (u'img')
        for image in images:
            controller.process (url, image['src'], image)

        self._contentResult = self._soup.prettify()


    @property
    def contentSrc (self):
        return self._contentSrc


    @property
    def contentResult (self):
        return self._contentResult


    @property
    def pageTitle (self):
        return self._pageTitle



class BaseDownloadController (object):
    '''
    Instance the class select action for every downloaded file
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def process (self, startUrl, url, node):
        pass


    def log (self, text):
        pass


    def _changeNodeUrl (self, node, url):
        if node.name == 'img':
            node['src'] = url


class DownloadController (BaseDownloadController):
    """
    Class with main logic for downloading
    """
    def __init__ (self, rootDownloadDir, staticDir, timeout=20):
        self._rootDownloadDir = rootDownloadDir
        self._staticDir = staticDir
        self._timeout = timeout
        self._fullStaticDir = os.path.join (rootDownloadDir, staticDir).replace (u'\\', u'/')


    def process (self, startUrl, url, node):
        if not os.path.exists (self._fullStaticDir):
            os.mkdir (self._fullStaticDir)

        fullUrl = urljoin (startUrl, url)

        relativeDownloadPath = self._getRelativeDownloadPath (url)
        fullDownloadPath = os.path.join (self._rootDownloadDir,
                                         relativeDownloadPath).replace (u'\\', u'/')
        downloadDir = os.path.dirname (fullDownloadPath)

        if not os.path.exists (downloadDir):
            os.makedirs (downloadDir)

        try:
            obj = urllib2.urlopen (fullUrl, timeout=self._timeout)
            with open (fullDownloadPath, 'wb') as fp:
                fp.write (obj.read())
            self._changeNodeUrl (node, relativeDownloadPath)
        except (urllib2.URLError, IOError):
            self.log (_(u"Can't download {}\n").format (url))


    def _getRelativeDownloadPath (self, url):
        """
        Return relative path to download.
        For example: '__download/folder/subfolder/image.jpg'
        """
        protocol_pos = url.find (u'://')
        url_clean = url[protocol_pos + 3:] if protocol_pos != -1 else url

        if url_clean.startswith (u'/'):
            url_clean = url_clean[1:]

        url_clean = url_clean.replace (u':', u'_')

        relativeDownloadPath = os.path.join (self._staticDir, url_clean).replace (u'\\', u'/')
        return relativeDownloadPath


class WebPageDownloadController (DownloadController):
    """
    DownloadController for using for creation WebPage.
    Downloading can be terminated with event.
    Log will be send with UpdateLogEvent
    """
    def __init__ (self, runEvent, rootDownloadDir, staticDir, dialog, timeout=20):
        super (WebPageDownloadController, self).__init__ (rootDownloadDir,
                                                          staticDir,
                                                          timeout)
        self._runEvent = runEvent
        self._dialog = dialog


    def process (self, startUrl, url, node):
        if self._runEvent.is_set():
            super (WebPageDownloadController, self).process (startUrl, url, node)


    def log (self, text):
        event = UpdateLogEvent (text=text)
        wx.PostEvent (self._dialog, event)
