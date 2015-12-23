# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import re
import urllib2
from urlparse import urljoin, urlparse

import wx

from bs4 import BeautifulSoup
from events import UpdateLogEvent


class BaseDownloader (object):
    def download (self, url):
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'OutWiker')]
        return opener.open(url, timeout = self._timeout)


class Downloader (BaseDownloader):
    def __init__ (self, timeout=20):
        self._timeout = 20

        self._contentSrc = None
        self._pageTitle = None
        self._soup = None

        self._contentResult = None
        self._success = False


    def start (self, url, controller):
        self._success = False
        obj = self.download (url)
        self._soup = BeautifulSoup (obj.read(), "html.parser")
        self._contentSrc = self._soup.prettify()

        if self._soup.title is not None:
            self._pageTitle = self._soup.title.string

        self._downloadImages (self._soup, controller, url)
        self._downloadCSS (self._soup, controller, url)
        self._downloadScripts (self._soup, controller, url)

        self._improveResult (self._soup, url)

        self._contentResult = unicode (self._soup)
        self._success = True


    def _improveResult (self, soup, url):
        self._disableBaseTag (soup)


    def _disableBaseTag (self, soup):
        for basetag in soup.find_all (u'base'):
            if basetag.has_attr (u'href'):
                basetag[u'href'] = u''


    @property
    def success (self):
        return self._success


    def _downloadImages (self, soup, controller, url):
        images = soup.find_all (u'img')
        for image in images:
            controller.processImg (url, image['src'], image)


    def _downloadCSS (self, soup, controller, url):
        links = soup.find_all (u'link')
        for link in links:
            if (link.has_attr ('rel') and
                    link.has_attr ('href') and
                    link['rel'][0].lower() == u'stylesheet'):
                controller.processCSS (url, link['href'], link)


    def _downloadScripts (self, soup, controller, url):
        scripts = soup.find_all (u'script')
        for script in scripts:
            if script.has_attr ('src'):
                controller.processScript (url, script['src'], script)


    @property
    def contentSrc (self):
        return self._contentSrc


    @property
    def contentResult (self):
        return self._contentResult


    @property
    def pageTitle (self):
        return self._pageTitle



class BaseDownloadController (BaseDownloader):
    '''
    Instance the class select action for every downloaded file
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def processImg (self, startUrl, url, node):
        pass


    @abstractmethod
    def processCSS (self, startUrl, url, node):
        pass


    @abstractmethod
    def processScript (self, startUrl, url, node):
        pass


    def log (self, text):
        pass


    def _changeNodeUrl (self, node, url):
        if node is None:
            return

        if node.name == 'img':
            node['src'] = url
        elif node.name == 'link':
            node['href'] = url
        elif node.name == 'script':
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

        # Key - url from source HTML page,
        # value - relative path to downloaded file
        self._staticFiles = {}


    def processImg (self, startUrl, url, node):
        self._process (startUrl, url, node, self._processFuncNone)


    def processCSS (self, startUrl, url, node):
        self._process (startUrl, url, node, self._processFuncCSS)


    def processScript (self, startUrl, url, node):
        self._process (startUrl, url, node, self._processFuncNone)


    def _processFuncNone (self, startUrl, url, node, text):
        return text


    def _processFuncCSS (self, startUrl, url, node, text):
        regexp1 = re.compile (r'''^@import\s*
                              url\((?P<quote>['"])(?P<url>.*?)(?P=quote)\)
                              (?P<other>.*)$''',
                              re.X | re.U)

        regexp2 = re.compile (r'''^@import\s*
                              (?P<quote>['"])(?P<url>.*?)(?P=quote)
                              (?P<other>.*)$''',
                              re.X | re.U)

        regexp3 = re.compile (r'''^@import\s*
                              url\((?P<url>.*?)\)
                              (?P<other>.*)$''',
                              re.X | re.U)

        regexp_list = [regexp1, regexp2, regexp3]

        lines = text.split (u'\n')
        resultLines = []
        for line in lines:
            # success will be True if line match any of regexp_list regexp
            success = False

            for regexp in regexp_list:
                match = regexp.match (line)
                if match is not None:
                    importurl = match.group ('url')
                    relativeurl = os.path.dirname (url) + '/' + importurl
                    while relativeurl.startswith (u'/'):
                        relativeurl = relativeurl[1:]

                    relativeDownloadPath = self._process (startUrl,
                                                          relativeurl,
                                                          None,
                                                          self._processFuncNone)

                    resultLines.append (
                        u'@import url("{url}"){other}'.format (
                            url = os.path.basename (relativeDownloadPath),
                            other = match.group ('other')
                        )
                    )
                    success = True
                    break

            if not success:
                resultLines.append (line)

        return u'\n'.join (resultLines)


    def _process (self, startUrl, url, node, processFunc):
        # Create dir for downloading
        if not os.path.exists (self._fullStaticDir):
            os.mkdir (self._fullStaticDir)

        self.log (_(u'Download: {}\n').format (url))

        fullUrl = urljoin (startUrl, url)

        relativeDownloadPath = self._getRelativeDownloadPath (fullUrl)
        if fullUrl in self._staticFiles:
            return relativeDownloadPath

        self._staticFiles[fullUrl] = relativeDownloadPath
        fullDownloadPath = os.path.join (self._rootDownloadDir,
                                         relativeDownloadPath)

        try:
            obj = self.download (fullUrl)
            with open (fullDownloadPath, 'wb') as fp:
                text = processFunc (startUrl, url, node, obj.read())
                fp.write (text)

            if node is not None:
                self._changeNodeUrl (node, relativeDownloadPath)
        except (urllib2.URLError, IOError):
            self.log (_(u"Can't download {}\n").format (url))

        return relativeDownloadPath


    def _getRelativeDownloadPath (self, url):
        """
        Return relative path to download.
        For example: '__download/image.png'
        """
        path = urlparse (url).path
        if path.endswith (u'/'):
            path = path[:-1]

        slashpos = path.rfind ('/')
        if slashpos != -1:
            fname = path[slashpos + 1:]
        else:
            fname = path

        relativeDownloadPath = u'{}/{}'.format (self._staticDir, fname)
        result = relativeDownloadPath

        fullDownloadPath = os.path.join (self._rootDownloadDir,
                                         result)

        number = 1
        while os.path.exists (fullDownloadPath):
            dotpos = relativeDownloadPath.rfind (u'.')
            if dotpos == -1:
                newRelativePath = u'{}_{}'.format (relativeDownloadPath, number)
            else:
                newRelativePath = u'{}_{}{}'.format (
                    relativeDownloadPath[:dotpos],
                    number,
                    relativeDownloadPath[dotpos:]
                )

            result = newRelativePath
            fullDownloadPath = os.path.join (self._rootDownloadDir,
                                             newRelativePath)
            number += 1

        return result


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


    def processImg (self, startUrl, url, node):
        if self._runEvent.is_set():
            super (WebPageDownloadController, self).processImg (startUrl, url, node)


    def processCSS (self, startUrl, url, node):
        if self._runEvent.is_set():
            super (WebPageDownloadController, self).processCSS (startUrl, url, node)


    def processScript (self, startUrl, url, node):
        if self._runEvent.is_set():
            super (WebPageDownloadController, self).processScript (startUrl, url, node)


    def log (self, text):
        event = UpdateLogEvent (text=text)
        wx.PostEvent (self._dialog, event)
