# -*- coding: UTF-8 -*-


class DictsFinder (object):
    """
    Class for searching spell dictionaries in many folders
    """
    def __init__ (self, config):
        self._config = config


    def getLangList (self):
        """
        Return list of languages ("ru_RU, "en_US", etc) from all spell folders
        """
        result = []
        return result


    def getFolderForLang (self, lang):
        """
        Return folder which contains dictionary for lang language.
        Return None if lang will not be found
        """
        return None
