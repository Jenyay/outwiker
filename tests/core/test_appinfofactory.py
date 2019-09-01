# -*- coding: utf-8 -*-

from outwiker.core.xmlversionparser import XmlAppInfo, DataForLanguage
from outwiker.core.appinfofactory import AppInfoFactory


def test_extractDataForLanguage_empty():
    data = DataForLanguage()
    assert AppInfoFactory.extractDataForLanguage(data, '', 'default') == 'default'


def test_extractDataForLanguage_01():
    data = DataForLanguage()
    data.set_for_language('en', 'John')
    assert AppInfoFactory.extractDataForLanguage(data, 'en', '') == 'John'


def test_extractDataForLanguage_02():
    data = DataForLanguage()
    data.set_for_language('en', 'John')
    assert AppInfoFactory.extractDataForLanguage(data, 'en_US', '') == 'John'


def test_extractDataForLanguage_03():
    data = DataForLanguage()
    data.set_for_language('en', 'John')
    data.set_for_language('en_US', 'John Smith')
    assert AppInfoFactory.extractDataForLanguage(data, 'en_US', '') == 'John Smith'


def test_extractDataForLanguage_04():
    data = DataForLanguage()
    data.set_for_language('', 'John')
    data.set_for_language('en_US', 'John Smith')
    assert AppInfoFactory.extractDataForLanguage(data, 'ru', '') == 'John'


def test_extractDataForLanguage_05():
    data = DataForLanguage()
    data.set_for_language('en_US', 'John Smith')
    assert AppInfoFactory.extractDataForLanguage(data, 'ru', '') == ''


def test_fromXmlAppInfo_empty():
    xmlAppInfo = XmlAppInfo()
    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == ''
    assert appInfo.app_info_url == ''
    assert appInfo.website == ''
    assert appInfo.description == ''
    assert appInfo.versions == []
    assert appInfo.author is not None
    assert appInfo.author.name == ''
    assert appInfo.author.email == ''
    assert appInfo.author.website == ''


def test_fromXmlAppInfo_app_info_url():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_info_url = 'https://example.com'
    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_info_url == xmlAppInfo.app_info_url


def test_fromXmlAppInfo_app_name():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_name.set_for_language('en', 'John')
    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == 'John'


def test_fromXmlAppInfo_app_name_alternative_01():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_name.set_for_language('en', 'John')
    xmlAppInfo.app_name.set_for_language('', 'John Smith')
    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == 'John'


def test_fromXmlAppInfo_app_name_alternative_02():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_name.set_for_language('en', 'John')
    xmlAppInfo.app_name.set_for_language('en_US', 'John Smith')
    language = 'en_US'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == 'John Smith'


def test_fromXmlAppInfo_app_name_alternative_03():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_name.set_for_language('en', 'John')
    xmlAppInfo.app_name.set_for_language('ru', 'Джон')
    language = 'en_US'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == 'John'


def test_fromXmlAppInfo_app_name_alternative_04():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_name.set_for_language('', 'John')
    xmlAppInfo.app_name.set_for_language('ru', 'Джон')
    language = 'en_US'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == 'John'


def test_fromXmlAppInfo_website():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.website.set_for_language('en', 'http://example.com')
    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.website == 'http://example.com'


def test_fromXmlAppInfo_website_missing():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.website.set_for_language('en', 'http://example.com')
    language = 'ru'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.website == ''


def test_fromXmlAppInfo_website_lang():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.website.set_for_language('en', 'http://example.com')
    xmlAppInfo.website.set_for_language('ru', 'http://example.com/ru')
    language = 'ru'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.website == 'http://example.com/ru'


def test_fromXmlAppInfo_website_lang_alternative():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.website.set_for_language('en', 'http://example.com')
    xmlAppInfo.website.set_for_language('ru', 'http://example.com/ru')
    language = 'ru_RU'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.website == 'http://example.com/ru'


def test_fromXmlAppInfo_website_default():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.website.set_for_language('', 'http://example.com')
    xmlAppInfo.website.set_for_language('jp', 'http://example.com/jp')
    language = 'ru_RU'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.website == 'http://example.com'


def test_fromXmlAppInfo_description():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.description.set_for_language('en', 'bla-bla-bla')
    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.description == 'bla-bla-bla'


def test_fromXmlAppInfo_description_ru_RU():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.description.set_for_language('en', 'bla-bla-bla')
    xmlAppInfo.description.set_for_language('ru', 'бла-бла-бла')
    language = 'ru_RU'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.description == 'бла-бла-бла'


def test_fromXmlAppInfo_description_default():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.description.set_for_language('', 'bla-bla-bla')
    xmlAppInfo.description.set_for_language('ru', 'бла-бла-бла')
    language = 'jp'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.description == 'bla-bla-bla'
