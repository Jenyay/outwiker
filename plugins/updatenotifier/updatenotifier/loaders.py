# -*- coding: UTF-8 -*-
"""
Модуль с классами, предназначенными для загрузки страницы из интернета или эмуляции этого процесса
"""

import urllib2


class NormalLoader (object):
    """
    Класс для честной загрузки страницы из интернета
    """
    def load (self, url):
        """
        Метод может бросать исключения urllib2.HTTPError и urllib2.URLError
        """
        fp = urllib2.urlopen (url)

        try:
            text = fp.read()
        finally:
            fp.close()

        return text



class DisconnectedLoader (object):
    """
    Класс загрузчика, эмулирующий отсутствие интернета
    """
    def load (self, url):
        raise urllib2.URLError("Disconnected")
