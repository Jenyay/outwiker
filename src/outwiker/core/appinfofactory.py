# -*- coding: utf-8 -*-

from .xmlversionparser import XmlAppInfo, DataForLanguage, T
from .appinfo import AppInfo


class AppInfoFactory:
    '''
    Class to create AppInfo instance
    '''
    DEFAULT_LANGUAGE = ''

    @classmethod
    def extractDataForLanguage(cls,
                               data: DataForLanguage[T],
                               language: str,
                               default: T) -> T:
        # lang_list example: ['ru_RU', 'ru', '']
        lang_list = [language]
        underscore_pos = language.find('_')
        if underscore_pos != -1:
            lang_list.append(language[: underscore_pos])
        lang_list.append(cls.DEFAULT_LANGUAGE)

        for current_lang in lang_list:
            if current_lang in data:
                return data[current_lang]

        return default

    @classmethod
    def fromXmlAppInfo(cls,
                       xmlAppInfo: XmlAppInfo,
                       language: str) -> AppInfo:
        app_info_url = xmlAppInfo.app_info_url
        app_name = cls.extractDataForLanguage(
            xmlAppInfo.app_name, language, '')
        website = cls.extractDataForLanguage(xmlAppInfo.website, language, '')
        description = cls.extractDataForLanguage(
            xmlAppInfo.description, language, '')

        result = AppInfo(app_info_url=app_info_url,
                         app_name=app_name,
                         website=website,
                         description=description
                         )
        return result
