# -*- coding: utf-8 -*-

import os
import os.path

from .defines import CUSTOM_DICT_LANG


class DictsFinder (object):
    """
    Class for searching spell dictionaries in many folders
    """
    dictExtensions = [u".aff", u".dic"]

    def __init__(self, dirlist):
        self._dirlist = dirlist

    def getLangList(self):
        """
        Return list of languages ("ru_RU, "en_US", etc) from all spell folders
        """
        result = set()
        for path in self._dirlist:
            result.update(self._findLangs(path))
        return list(result)

    def getFoldersForLang(self, lang):
        """
        Return a list of folders which contains dictionary for lang language.
        """
        return [path
                for path in self._dirlist
                if (os.path.exists(os.path.join(path, lang + self.dictExtensions[0])) and
                    os.path.exists(os.path.join(path, lang + self.dictExtensions[1])))]

    def _findLangs(self, path):
        langs = set()
        for fname in os.listdir(path):
            if fname.endswith(self.dictExtensions[0]):
                lang = fname[:-len(self.dictExtensions[0])]
                if lang == CUSTOM_DICT_LANG:
                    continue

                fname_dic = lang + self.dictExtensions[1]
                if os.path.exists(os.path.join(path, fname_dic)):
                    langs.add(lang)

        return langs
