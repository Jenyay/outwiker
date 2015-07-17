# -*- coding: UTF-8 -*-


class EnchantWrapper (object):
    """
    Wrapper around pyenchant (http://pythonhosted.org/pyenchant/)
    """
    def __init__ (self, langlist):
        """
        langlist - list of the languages ("ru_RU", "en_US", etc)
        """
        self._checkers = []


    def check (self, word):
        return False
