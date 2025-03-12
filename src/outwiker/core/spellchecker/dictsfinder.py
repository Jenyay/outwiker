# -*- coding: utf-8 -*-

import os
import os.path

from .defines import CUSTOM_DICT_LANG


class DictsFinder:
    """
    Class for searching spell dictionaries in many folders
    """
    dictExtensions = [".aff", ".dic"]

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
        result = []
        for path in self._dirlist:
            fname_1 = os.path.join(path, lang + self.dictExtensions[0])
            fname_2 = os.path.join(path, lang + self.dictExtensions[1])

            if os.path.exists(fname_1) and os.path.exists(fname_2):
                result.append(path)

        return result

    def _findLangs(self, path):
        langs = set()
        if not os.path.exists(path):
            return langs

        for fname in os.listdir(path):
            if fname.endswith(self.dictExtensions[0]):
                lang = fname[:-len(self.dictExtensions[0])]
                if lang == CUSTOM_DICT_LANG:
                    continue

                fname_dic = lang + self.dictExtensions[1]
                if os.path.exists(os.path.join(path, fname_dic)):
                    langs.add(lang)

        return langs
