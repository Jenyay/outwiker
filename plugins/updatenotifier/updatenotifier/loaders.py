# -*- coding: utf-8 -*-
"""
Модуль с классами, предназначенными для загрузки страницы из интернета
или эмуляции этого процесса
"""

import os.path
import urllib.request
import urllib.error

from outwiker.utilites.textfile import readTextFile


class NormalLoader(object):
    """
    Класс для загрузки страницы из интернета
    """
    def load(self, url):
        """
        Метод может бросать исключения urllib2.HTTPError и urllib2.URLError
        """
        if os.path.isfile(url):
            return readTextFile(url)

        fp = urllib.request.urlopen(url, timeout=10)
        text = None
        try:
            text = fp.read().decode('utf-8')
        finally:
            fp.close()

        return text


class DisconnectedLoader(object):
    """
    Класс загрузчика, эмулирующий отсутствие интернета
    """
    def load(self, url):
        raise urllib.error.URLError("Disconnected")
