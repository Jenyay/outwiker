# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import urllib2

from bs4 import BeautifulSoup


class Downloader (object):
    def __init__ (self, staticDirName, controller, timeout=20):
        self._staticDir = staticDirName
        self._controller = controller
        self._timeout = 20

        self._content_src = None


    def start (self, url):
        obj = urllib2.urlopen (url, timeout=self._timeout)
        soup = BeautifulSoup(obj.read(), 'html.parser')
        self._content_src = soup.prettify()


    def nextFile (self):
        pass


    @property
    def content_src (self):
        return self._content_src



class BaseDownloadController (object):
    '''
    Instance the class select action for every downloaded file
    '''
    __metaclass__ = ABCMeta

    @abstractmethod
    def process (self, url, node):
        pass
