# -*- coding: utf-8 -*-

from typing import Union, Tuple, Iterator


class LangList:
    def __init__(self, translate_func=None):
        from .pygments.lexers._mapping import LEXERS

        if translate_func is None:
            translate_func = self._empty_translate

        # Key - full language name,
        # Value - tuple of designations of the language
        self._languages = {translate_func(lexer[1]): lexer[2]
                           for lexer
                           in LEXERS.values()}

    def _empty_translate(self, text: str) -> str:
        return text

    def allNames(self) -> Iterator[str]:
        '''
        Return list iterator of names of the all languages
        '''
        return self._languages.keys()

    def getAllDesignations(self, lang_name: str) -> Union[Tuple[str], None]:
        '''
        Return all designations for lang_name or None if it is not exists
        '''
        return self._languages.get(lang_name)

    def getDesignation(self, lang_name: str) -> Union[str, None]:
        '''
        Return a first designations for lang_name or None if it is not exists
        '''
        all_designations = self.getAllDesignations(lang_name)
        if all_designations is not None:
            return all_designations[0]

        return None

    def getLangName(self, designation: str) -> Union[str, None]:
        '''
        Return name of the language by designation
        '''
        designation = designation.lower()

        for name, designations in self._languages.items():
            if designation in designations:
                return name

        return None
