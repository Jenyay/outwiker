# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import urllib2
from urlparse import urljoin

from bs4 import BeautifulSoup


class Downloader (object):
    def __init__ (self, staticDirName, timeout=20):
        self._staticDir = staticDirName
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
            src = urljoin (url, image['src'])
            controller.process (src, image)


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
    def process (self, url, node):
        pass
