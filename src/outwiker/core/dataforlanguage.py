# -*- coding: utf-8 -*-

from typing import Dict, Generic, TypeVar, List, Optional


T = TypeVar('T')


class DataForLanguage(Generic[T]):
    def __init__(self):
        # Key - language, value - data
        self._data = {}             # type: Dict[str, T]

    def set_for_language(self, language: str, data: T) -> None:
        self._data[language] = data

    def __getitem__(self, language: str) -> T:
        return self._data[language]

    def __contains__(self, language: str) -> bool:
        return language in self._data

    def get_languages(self) -> List[str]:
        return list(self._data.keys())

    def is_empty(self) -> bool:
        return len(self._data) == 0

    def get(self, language: str, default: Optional[T] = None) -> T:
        DEFAULT_LANGUAGE = ''
        # lang_list example: ['ru_RU', 'ru', '']
        lang_list = [language]
        underscore_pos = language.find('_')
        if underscore_pos != -1:
            lang_list.append(language[: underscore_pos])
        lang_list.append(DEFAULT_LANGUAGE)

        for current_lang in lang_list:
            if current_lang in self:
                return self[current_lang]

        return default
