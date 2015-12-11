# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import urllib2
from urlparse import urljoin

from bs4 import BeautifulSoup


class Downloader (object):
    def __init__ (self, timeout=20):
        self._timeout = 20

        self._content_src = None
        self._pageTitle = None
        self._soup = None


    def start (self, url, controller):
        obj = urllib2.urlopen (url, timeout=self._timeout)
        self._soup = BeautifulSoup(obj.read(), 'html.parser')
        self._content_src = self._soup.prettify()

        if self._soup.title is not None:
            self._pageTitle = self._soup.title.string

        images = self._soup.find_all (u'img')
        for image in images:
            controller.process (url, image['src'], image)


    @property
    def content_src (self):
        return self._content_src


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


class DownloadController (BaseDownloadController):
    def __init__ (self, rootDownloadDir, staticDir, timeout=20):
        self._rootDownloadDir = rootDownloadDir
        self._staticDir = staticDir
        self._timeout = timeout
        self._fullDownloadDir = os.path.join (rootDownloadDir, staticDir)


    def process (self, startUrl, url, node):
        if not os.path.exists (self._fullDownloadDir):
            os.mkdir (self._fullDownloadDir)

        fullUrl = urljoin (startUrl, url)

        downloadPath = self._getDownloadPath (url)
        downloadDir = os.path.dirname (downloadPath)

        if not os.path.exists (downloadDir):
            os.makedirs (downloadDir)

        try:
            obj = urllib2.urlopen (fullUrl, timeout=self._timeout)
            with open (downloadPath, 'wb') as fp:
                fp.write (obj.read())
        except urllib2.URLError:
            pass


    def _getDownloadPath (self, url):
        protocol_pos = url.find (u'://')
        url_clean = url[protocol_pos + 3:] if protocol_pos != -1 else url

        if url_clean.startswith (u'/'):
            url_clean = url_clean[1:]

        url_clean = url_clean.replace (u':', u'_')

        result = os.path.join (self._fullDownloadDir, url_clean)

        return result
