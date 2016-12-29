# -*- coding: UTF-8 -*-

import urllib2
from StringIO import StringIO
import gzip


class Downloader (object):
    '''
    Class to downloading web pages.

    Added in OutWiker 2.0.0.797
    '''

    def __init__(self, timeout):
        """
        timeout - timeout in seconds.
        """
        self._timeout = timeout
        self._headers = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 OutWiker/1'),
                         ('Accept-encoding', 'gzip')]

    def download(self, url):
        opener = urllib2.build_opener()
        opener.addheaders = self._headers

        response = opener.open(url, timeout=self._timeout)
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(response.read())
            zipfile = gzip.GzipFile(fileobj=buf)
            result = zipfile.read()
        else:
            result = response.read()
        return result.decode('utf8')
