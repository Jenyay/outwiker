# -*- coding: utf-8 -*-

from outwiker.core.xmlappinfoparser import (
    XmlAppInfo, XmlAuthorInfo, XmlVersionInfo, DataForLanguage)
from outwiker.core.appinfofactory import (AppInfoFactory,
                                          extractDataForLanguage)
from outwiker.core.version import Version, StatusSet

xmlexample = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <updates>http://example.com/updates.xml</updates>

    <name>Application name</name>
    <name lang="ru">Имя приложения</name>

    <website>http://jenyay.net/en/</website>
    <website lang="ru">http://jenyay.net/ru/</website>

    <description>Description</description>
    <description lang="ru">Описание</description>

    <author>
        <name>John</name>
        <email>john@example.com</email>
        <website>http://example.com</website>
    </author>

    <author lang='ru'>
        <name>Джон</name>
        <email>john_ru@example.com</email>
        <website>http://example.com/ru</website>
    </author>

    <author>
        <name>Andrey</name>
        <email>andrey@example.com</email>
        <website>http://example.com/andrey</website>
    </author>

    <author lang='ru'>
        <name>Андрей</name>
        <email>andrey_ru@example.com</email>
        <website>http://example.com/andrey/ru</website>
    </author>

    <requirements>
        <os>Windows</os>
        <os>Linux</os>
        <api>2.222</api>
        <api>3.333</api>
    </requirements>
    <version number="2.0" status="dev"/>
</info>
'''


def test_extractDataForLanguage_empty():
    data = DataForLanguage()
    assert extractDataForLanguage(
        data, '', 'default') == 'default'


def test_extractDataForLanguage_01():
    data = DataForLanguage()
    data.set_for_language('en', 'John')
    assert extractDataForLanguage(data, 'en', '') == 'John'


def test_extractDataForLanguage_02():
    data = DataForLanguage()
    data.set_for_language('en', 'John')
    assert extractDataForLanguage(data, 'en_US', '') == 'John'


def test_extractDataForLanguage_03():
    data = DataForLanguage()
    data.set_for_language('en', 'John')
    data.set_for_language('en_US', 'John Smith')
    assert extractDataForLanguage(data, 'en_US', '') == 'John Smith'


def test_extractDataForLanguage_04():
    data = DataForLanguage()
    data.set_for_language('', 'John')
    data.set_for_language('en_US', 'John Smith')
    assert extractDataForLanguage(data, 'ru', '') == 'John'


def test_extractDataForLanguage_05():
    data = DataForLanguage()
    data.set_for_language('en_US', 'John Smith')
    assert extractDataForLanguage(data, 'ru', '') == ''


def test_fromXmlAppInfo_empty():
    xmlAppInfo = XmlAppInfo()
    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_name == ''
    assert appInfo.app_info_url == ''
    assert appInfo.website == ''
    assert appInfo.description == ''
    assert appInfo.authors == []
    assert appInfo.requirements.os_list == []
    assert appInfo.requirements.api_list == []
    assert appInfo.version is None


def test_fromXmlAppInfo_app_info_url():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.app_info_url = 'https://example.com'
    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.app_info_url == xmlAppInfo.app_info_url


def test_fromXmlAppInfo_app_info_version():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.version = XmlVersionInfo('1.0.1', status='beta')
    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.version == Version(1, 0, 1, status=StatusSet.BETA)


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


def test_fromXmlAppInfo_authors():
    xmlAppInfo = XmlAppInfo()
    author_en = XmlAuthorInfo(
        name='John', email='john@example.com', website='http://example.com')
    xmlAppInfo.authors.set_for_language('en', [author_en])

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.authors[0].name == 'John'
    assert appInfo.authors[0].email == 'john@example.com'
    assert appInfo.authors[0].website == 'http://example.com'


def test_fromXmlAppInfo_authors_default():
    xmlAppInfo = XmlAppInfo()

    author_default = XmlAuthorInfo(
        name='John',
        email='john@example.com',
        website='http://example.com')
    xmlAppInfo.authors.set_for_language('', [author_default])

    author_ru = XmlAuthorInfo(
        name='Джон',
        email='john_ru@example.com',
        website='http://example.com/ru')
    xmlAppInfo.authors.set_for_language('ru', [author_ru])

    language = 'jp'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.authors[0].name == 'John'
    assert appInfo.authors[0].email == 'john@example.com'
    assert appInfo.authors[0].website == 'http://example.com'


def test_fromXmlAppInfo_authors_language_alternative():
    xmlAppInfo = XmlAppInfo()

    author_en = XmlAuthorInfo(
        name='John',
        email='john@example.com',
        website='http://example.com')
    xmlAppInfo.authors.set_for_language('en', [author_en])

    language = 'en_US'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.authors[0].name == 'John'
    assert appInfo.authors[0].email == 'john@example.com'
    assert appInfo.authors[0].website == 'http://example.com'


def test_fromXmlAppInfo_requirements_single():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.requirements.os_list = ['Windows']
    xmlAppInfo.requirements.api_list = ['3.868']

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.requirements.os_list == ['Windows']
    assert appInfo.requirements.api_list == [Version(3, 868)]


def test_fromXmlAppInfo_requirements_several():
    xmlAppInfo = XmlAppInfo()
    xmlAppInfo.requirements.os_list = ['Windows', 'Linux']
    xmlAppInfo.requirements.api_list = ['3.868', '2.800']

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.requirements.os_list == ['Windows', 'Linux']
    assert appInfo.requirements.api_list == [Version(3, 868), Version(2, 800)]


def test_fromString_lang_ru():
    appinfo = AppInfoFactory.fromString(xmlexample, language='ru')

    assert appinfo.app_info_url == 'http://example.com/updates.xml'
    assert appinfo.app_name == 'Имя приложения'
    assert appinfo.website == 'http://jenyay.net/ru/'
    assert appinfo.description == 'Описание'

    assert appinfo.authors[0].name == 'Джон'
    assert appinfo.authors[0].email == 'john_ru@example.com'
    assert appinfo.authors[0].website == 'http://example.com/ru'

    assert appinfo.authors[1].name == 'Андрей'
    assert appinfo.authors[1].email == 'andrey_ru@example.com'
    assert appinfo.authors[1].website == 'http://example.com/andrey/ru'

    assert appinfo.version == Version(2, 0, status=StatusSet.DEV)

    assert appinfo.requirements.os_list == ['Windows', 'Linux']
    assert appinfo.requirements.api_list == [Version(2, 222), Version(3, 333)]


def test_fromString_lang_ru_RU():
    appinfo = AppInfoFactory.fromString(xmlexample, language='ru_RU')

    assert appinfo.app_info_url == 'http://example.com/updates.xml'
    assert appinfo.app_name == 'Имя приложения'
    assert appinfo.website == 'http://jenyay.net/ru/'
    assert appinfo.description == 'Описание'

    assert appinfo.authors[0].name == 'Джон'
    assert appinfo.authors[0].email == 'john_ru@example.com'
    assert appinfo.authors[0].website == 'http://example.com/ru'

    assert appinfo.authors[1].name == 'Андрей'
    assert appinfo.authors[1].email == 'andrey_ru@example.com'
    assert appinfo.authors[1].website == 'http://example.com/andrey/ru'

    assert appinfo.version == Version(2, 0, status=StatusSet.DEV)

    assert appinfo.requirements.os_list == ['Windows', 'Linux']
    assert appinfo.requirements.api_list == [Version(2, 222), Version(3, 333)]


def test_fromString_lang_default():
    appinfo = AppInfoFactory.fromString(xmlexample, language='jp')

    assert appinfo.app_info_url == 'http://example.com/updates.xml'
    assert appinfo.app_name == 'Application name'
    assert appinfo.website == 'http://jenyay.net/en/'
    assert appinfo.description == 'Description'

    assert appinfo.authors[0].name == 'John'
    assert appinfo.authors[0].email == 'john@example.com'
    assert appinfo.authors[0].website == 'http://example.com'

    assert appinfo.authors[1].name == 'Andrey'
    assert appinfo.authors[1].email == 'andrey@example.com'
    assert appinfo.authors[1].website == 'http://example.com/andrey'

    assert appinfo.version == Version(2, 0, status=StatusSet.DEV)

    assert appinfo.requirements.os_list == ['Windows', 'Linux']
    assert appinfo.requirements.api_list == [Version(2, 222), Version(3, 333)]


def test_fromString_empty():
    appInfo = AppInfoFactory.fromString('', language='ru')

    assert appInfo.app_name == ''
    assert appInfo.app_info_url == ''
    assert appInfo.website == ''
    assert appInfo.description == ''
    assert appInfo.version is None
    assert appInfo.authors == []
