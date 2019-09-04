# -*- coding: utf-8 -*-

from outwiker.core.xmlversionparser import (
    XmlAppInfo, XmlAuthorInfo, XmlVersionInfo, XmlChangeItem, XmlDownload,
    XmlRequirements, DataForLanguage)
from outwiker.core.appinfofactory import AppInfoFactory
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

    <versions>
        <version number="1.0" status="beta">
            <changes>
                <change>Fix bug</change>
                <change>Fix other bug</change>
            </changes>

            <changes lang="ru">
                <change>Исправлена ошибка</change>
                <change>Исправлена другая ошибка</change>
            </changes>

            <download href="http://example.com/application_v1_01.zip">
                <requirements>
                    <os>Windows</os>
                    <os>Linux</os>
                    <api>3.666</api>
                    <api>3.777</api>
                </requirements>
            </download>

            <download href="http://example.com/application_v1_02.zip">
                <requirements>
                    <os>Windows</os>
                    <api>3.888</api>
                </requirements>
            </download>
        </version>

        <version number="2.0">
            <changes>
                <change>Fix bug - 2</change>
                <change>Fix other bug - 2</change>
            </changes>

            <changes lang="ru">
                <change>Исправлена ошибка - 2</change>
                <change>Исправлена другая ошибка - 2</change>
            </changes>

            <download href="http://example.com/application_v2_01.zip">
                <requirements>
                    <os>Windows</os>
                    <os>Linux</os>
                    <api>3.999</api>
                    <api>3.1111</api>
                </requirements>
            </download>

            <download href="http://example.com/application_v2_02.zip">
                <requirements>
                    <os>Windows</os>
                    <api>3.2222</api>
                </requirements>
            </download>
        </version>
    </versions>
</info>
'''


def test_extractDataForLanguage_empty():
    data = DataForLanguage()
    assert AppInfoFactory.extractDataForLanguage(
        data, '', 'default') == 'default'


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
    assert AppInfoFactory.extractDataForLanguage(
        data, 'en_US', '') == 'John Smith'


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


def test_fromXmlAppInfo_author():
    xmlAppInfo = XmlAppInfo()
    author_en = XmlAuthorInfo(
        name='John', email='john@example.com', website='http://example.com')
    xmlAppInfo.author.set_for_language('en', author_en)

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.author.name == 'John'
    assert appInfo.author.email == 'john@example.com'
    assert appInfo.author.website == 'http://example.com'


def test_fromXmlAppInfo_author_default():
    xmlAppInfo = XmlAppInfo()

    author_default = XmlAuthorInfo(
        name='John',
        email='john@example.com',
        website='http://example.com')
    xmlAppInfo.author.set_for_language('', author_default)

    author_ru = XmlAuthorInfo(
        name='Джон',
        email='john_ru@example.com',
        website='http://example.com/ru')
    xmlAppInfo.author.set_for_language('ru', author_ru)

    language = 'jp'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.author.name == 'John'
    assert appInfo.author.email == 'john@example.com'
    assert appInfo.author.website == 'http://example.com'


def test_fromXmlAppInfo_author_language_alternative():
    xmlAppInfo = XmlAppInfo()

    author_en = XmlAuthorInfo(
        name='John',
        email='john@example.com',
        website='http://example.com')
    xmlAppInfo.author.set_for_language('en', author_en)

    language = 'en_US'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.author.name == 'John'
    assert appInfo.author.email == 'john@example.com'
    assert appInfo.author.website == 'http://example.com'


def test_fromXmlAppInfo_versions_simple():
    xmlAppInfo = XmlAppInfo()
    version_1 = XmlVersionInfo(number='1.0', status='dev', date=None)
    version_2 = XmlVersionInfo(number='2.0', status='beta', date=None)

    xmlAppInfo.versions.append(version_1)
    xmlAppInfo.versions.append(version_2)

    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions) == 2

    assert appInfo.versions[0].version == Version(1, 0, status=StatusSet.DEV)
    assert appInfo.versions[0].downloads == []
    assert appInfo.versions[0].changes == []

    assert appInfo.versions[1].version == Version(2, 0, status=StatusSet.BETA)
    assert appInfo.versions[1].downloads == []
    assert appInfo.versions[1].changes == []


def test_fromXmlAppInfo_versions_invalid_number():
    xmlAppInfo = XmlAppInfo()
    version_1 = XmlVersionInfo(number='xxx')
    version_2 = XmlVersionInfo(number='1.0', status='dev', date=None)

    xmlAppInfo.versions.append(version_1)
    xmlAppInfo.versions.append(version_2)

    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions) == 1

    assert appInfo.versions[0].version == Version(1, 0, status=StatusSet.DEV)
    assert appInfo.versions[0].downloads == []
    assert appInfo.versions[0].changes == []


def test_fromXmlAppInfo_versions_invalid_status():
    xmlAppInfo = XmlAppInfo()
    version_1 = XmlVersionInfo(number='1.0', status='dev', date=None)
    version_2 = XmlVersionInfo(number='2.0', status='xxx')

    xmlAppInfo.versions.append(version_1)
    xmlAppInfo.versions.append(version_2)

    language = ''
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions) == 2

    assert appInfo.versions[0].version == Version(1, 0, status=StatusSet.DEV)
    assert appInfo.versions[0].downloads == []
    assert appInfo.versions[0].changes == []

    assert appInfo.versions[1].version == Version(2, 0)
    assert appInfo.versions[1].downloads == []
    assert appInfo.versions[1].changes == []


def test_fromXmlAppInfo_versions_changes():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)

    changes_en = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    version.changes.set_for_language('en', changes_en)

    xmlAppInfo.versions.append(version)

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions[0].changes) == 2
    assert appInfo.versions[0].changes[0].description == 'Change 1'
    assert appInfo.versions[0].changes[1].description == 'Change 2'


def test_fromXmlAppInfo_versions_changes_language_default():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)

    changes_default = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    changes_en = [XmlChangeItem('Change 1 En'), XmlChangeItem('Change 2 En')]
    version.changes.set_for_language('', changes_default)
    version.changes.set_for_language('en', changes_en)

    xmlAppInfo.versions.append(version)

    language = 'ru'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions[0].changes) == 2
    assert appInfo.versions[0].changes[0].description == 'Change 1'
    assert appInfo.versions[0].changes[1].description == 'Change 2'


def test_fromXmlAppInfo_versions_changes_language_alternative():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)

    changes_ru = [XmlChangeItem('Изменение 1'), XmlChangeItem('Изменение 2')]
    changes_en = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    version.changes.set_for_language('ru', changes_ru)
    version.changes.set_for_language('en', changes_en)

    xmlAppInfo.versions.append(version)

    language = 'ru_RU'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions[0].changes) == 2
    assert appInfo.versions[0].changes[0].description == 'Изменение 1'
    assert appInfo.versions[0].changes[1].description == 'Изменение 2'


def test_fromXmlAppInfo_versions_changes_change_list():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)

    changes_en = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    version.changes.set_for_language('en', changes_en)

    xmlAppInfo.versions.append(version)

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)
    changes_en.append(XmlChangeItem('Change 3'))

    assert len(appInfo.versions[0].changes) == 2
    assert appInfo.versions[0].changes[0].description == 'Change 1'
    assert appInfo.versions[0].changes[1].description == 'Change 2'


def test_fromXmlAppInfo_versions_downloads_href():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)
    download = XmlDownload('https://example.com/download.zip')
    version.downloads.append(download)
    xmlAppInfo.versions.append(version)

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert len(appInfo.versions[0].downloads) == 1
    assert appInfo.versions[0].downloads[0].href == 'https://example.com/download.zip'
    assert appInfo.versions[0].downloads[0].requirements.os_list == []
    assert appInfo.versions[0].downloads[0].requirements.api_list == []


def test_fromXmlAppInfo_versions_downloads_requirements_single():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)
    requirements = XmlRequirements(['Windows'], ['3.868'])
    download = XmlDownload('https://example.com/download.zip', requirements)
    version.downloads.append(download)
    xmlAppInfo.versions.append(version)

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.versions[0].downloads[0].requirements.os_list == ['Windows']
    assert appInfo.versions[0].downloads[0].requirements.api_list == [
        Version(3, 868)]


def test_fromXmlAppInfo_versions_downloads_requirements_several():
    xmlAppInfo = XmlAppInfo()
    version = XmlVersionInfo(number='1.0', status='dev', date=None)
    requirements = XmlRequirements(['Windows', 'Linux'], ['3.868', '2.800'])
    download = XmlDownload('https://example.com/download.zip', requirements)
    version.downloads.append(download)
    xmlAppInfo.versions.append(version)

    language = 'en'
    appInfo = AppInfoFactory.fromXmlAppInfo(xmlAppInfo, language)

    assert appInfo.versions[0].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert appInfo.versions[0].downloads[0].requirements.api_list == [
        Version(3, 868), Version(2, 800)]


def test_fromString_lang_ru():
    appinfo = AppInfoFactory.fromString(xmlexample, language='ru')

    assert appinfo.app_info_url == 'http://example.com/updates.xml'
    assert appinfo.app_name == 'Имя приложения'
    assert appinfo.website == 'http://jenyay.net/ru/'
    assert appinfo.description == 'Описание'
    assert appinfo.author.name == 'Джон'
    assert appinfo.author.email == 'john_ru@example.com'
    assert appinfo.author.website == 'http://example.com/ru'

    assert appinfo.versions[0].version == Version(1, 0, status=StatusSet.BETA)
    assert appinfo.versions[0].changes[0].description  == 'Исправлена ошибка'
    assert appinfo.versions[0].changes[1].description  == 'Исправлена другая ошибка'
    assert appinfo.versions[0].downloads[0].href == 'http://example.com/application_v1_01.zip'
    assert appinfo.versions[0].downloads[1].href == 'http://example.com/application_v1_02.zip'
    assert appinfo.versions[0].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert appinfo.versions[0].downloads[1].requirements.os_list == ['Windows']
    assert appinfo.versions[0].downloads[0].requirements.api_list == [
        Version(3, 666), Version(3, 777)]
    assert appinfo.versions[0].downloads[1].requirements.api_list == [
        Version(3, 888)]

    assert appinfo.versions[1].version == Version(2, 0)
    assert appinfo.versions[1].changes[0].description  == 'Исправлена ошибка - 2'
    assert appinfo.versions[1].changes[1].description  == 'Исправлена другая ошибка - 2'
    assert appinfo.versions[1].downloads[0].href == 'http://example.com/application_v2_01.zip'
    assert appinfo.versions[1].downloads[1].href == 'http://example.com/application_v2_02.zip'
    assert appinfo.versions[1].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert appinfo.versions[1].downloads[1].requirements.os_list == ['Windows']
    assert appinfo.versions[1].downloads[0].requirements.api_list == [
        Version(3, 999), Version(3, 1111)]
    assert appinfo.versions[1].downloads[1].requirements.api_list == [
        Version(3, 2222)]
