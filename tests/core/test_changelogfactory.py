# -*- coding: utf-8 -*-

from outwiker.core.xmlappinfoparser import (
    XmlChangeLogVersionInfo, XmlChangeItem, XmlDownload,
    XmlRequirements, XmlChangeLog)
from outwiker.core.appinfofactory import ChangeLogFactory
from outwiker.core.version import Version, StatusSet

xmlexample = '''<?xml version="1.1" encoding="UTF-8" ?>
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
'''


def test_fromXmlChangeLog_versions_simple():
    xmlChangeLog = XmlChangeLog()
    version_1 = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)
    version_2 = XmlChangeLogVersionInfo(number='2.0', status='beta', date=None)

    xmlChangeLog.versions.append(version_1)
    xmlChangeLog.versions.append(version_2)

    language = ''
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions) == 2

    assert changelog.versions[0].version == Version(1, 0, status=StatusSet.DEV)
    assert changelog.versions[0].downloads == []
    assert changelog.versions[0].changes == []

    assert changelog.versions[1].version == Version(
        2, 0, status=StatusSet.BETA)
    assert changelog.versions[1].downloads == []
    assert changelog.versions[1].changes == []


def test_fromXmlChangeLog_versions_invalid_number():
    xmlChangeLog = XmlChangeLog()
    version_1 = XmlChangeLogVersionInfo(number='xxx')
    version_2 = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)

    xmlChangeLog.versions.append(version_1)
    xmlChangeLog.versions.append(version_2)

    language = ''
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions) == 1

    assert changelog.versions[0].version == Version(1, 0, status=StatusSet.DEV)
    assert changelog.versions[0].downloads == []
    assert changelog.versions[0].changes == []


def test_fromXmlChangeLog_versions_invalid_status():
    xmlChangeLog = XmlChangeLog()
    version_1 = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)
    version_2 = XmlChangeLogVersionInfo(number='2.0', status='xxx')

    xmlChangeLog.versions.append(version_1)
    xmlChangeLog.versions.append(version_2)

    language = ''
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions) == 2

    assert changelog.versions[0].version == Version(1, 0, status=StatusSet.DEV)
    assert changelog.versions[0].downloads == []
    assert changelog.versions[0].changes == []

    assert changelog.versions[1].version == Version(2, 0)
    assert changelog.versions[1].downloads == []
    assert changelog.versions[1].changes == []


def test_fromXmlChangeLog_versions_changes():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)

    changes_en = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    version.changes.set_for_language('en', changes_en)

    xmlChangeLog.versions.append(version)

    language = 'en'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions[0].changes) == 2
    assert changelog.versions[0].changes[0].description == 'Change 1'
    assert changelog.versions[0].changes[1].description == 'Change 2'


def test_fromXmlChangeLog_versions_changes_language_default():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)

    changes_default = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    changes_en = [XmlChangeItem('Change 1 En'), XmlChangeItem('Change 2 En')]
    version.changes.set_for_language('', changes_default)
    version.changes.set_for_language('en', changes_en)

    xmlChangeLog.versions.append(version)

    language = 'ru'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions[0].changes) == 2
    assert changelog.versions[0].changes[0].description == 'Change 1'
    assert changelog.versions[0].changes[1].description == 'Change 2'


def test_fromXmlChangeLog_versions_changes_language_alternative():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)

    changes_ru = [XmlChangeItem('Изменение 1'), XmlChangeItem('Изменение 2')]
    changes_en = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    version.changes.set_for_language('ru', changes_ru)
    version.changes.set_for_language('en', changes_en)

    xmlChangeLog.versions.append(version)

    language = 'ru_RU'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions[0].changes) == 2
    assert changelog.versions[0].changes[0].description == 'Изменение 1'
    assert changelog.versions[0].changes[1].description == 'Изменение 2'


def test_fromXmlChangeLog_versions_changes_change_list():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)

    changes_en = [XmlChangeItem('Change 1'), XmlChangeItem('Change 2')]
    version.changes.set_for_language('en', changes_en)

    xmlChangeLog.versions.append(version)

    language = 'en'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)
    changes_en.append(XmlChangeItem('Change 3'))

    assert len(changelog.versions[0].changes) == 2
    assert changelog.versions[0].changes[0].description == 'Change 1'
    assert changelog.versions[0].changes[1].description == 'Change 2'


def test_fromXmlChangeLog_versions_downloads_href():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)
    download = XmlDownload('https://example.com/download.zip')
    version.downloads.append(download)
    xmlChangeLog.versions.append(version)

    language = 'en'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert len(changelog.versions[0].downloads) == 1
    assert changelog.versions[0].downloads[0].href == 'https://example.com/download.zip'
    assert changelog.versions[0].downloads[0].requirements.os_list == []
    assert changelog.versions[0].downloads[0].requirements.api_list == []


def test_fromXmlChangeLog_versions_downloads_requirements_single():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)
    requirements = XmlRequirements(['Windows'], [(3, 868)])
    download = XmlDownload('https://example.com/download.zip', requirements)
    version.downloads.append(download)
    xmlChangeLog.versions.append(version)

    language = 'en'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert changelog.versions[0].downloads[0].requirements.os_list == [
        'Windows']
    assert changelog.versions[0].downloads[0].requirements.api_list == [(3, 868)]


def test_fromXmlChangeLog_versions_downloads_requirements_several():
    xmlChangeLog = XmlChangeLog()
    version = XmlChangeLogVersionInfo(number='1.0', status='dev', date=None)
    requirements = XmlRequirements(['Windows', 'Linux'], [(3, 868), (2, 800)])
    download = XmlDownload('https://example.com/download.zip', requirements)
    version.downloads.append(download)
    xmlChangeLog.versions.append(version)

    language = 'en'
    changelog = ChangeLogFactory.fromXmlChangeLog(xmlChangeLog, language)

    assert changelog.versions[0].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changelog.versions[0].downloads[0].requirements.api_list == [
        (3, 868), (2, 800)]


def test_fromString_lang_ru():
    changeLog = ChangeLogFactory.fromString(xmlexample, language='ru')

    assert changeLog.versions[0].version == Version(
        1, 0, status=StatusSet.BETA)
    assert changeLog.versions[0].changes[0].description == 'Исправлена ошибка'
    assert changeLog.versions[0].changes[1].description == 'Исправлена другая ошибка'
    assert changeLog.versions[0].downloads[0].href == 'http://example.com/application_v1_01.zip'
    assert changeLog.versions[0].downloads[1].href == 'http://example.com/application_v1_02.zip'
    assert changeLog.versions[0].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changeLog.versions[0].downloads[1].requirements.os_list == [
        'Windows']
    assert changeLog.versions[0].downloads[0].requirements.api_list == [
        (3, 666), (3, 777)]
    assert changeLog.versions[0].downloads[1].requirements.api_list == [
        (3, 888)]

    assert changeLog.versions[1].version == Version(2, 0)
    assert changeLog.versions[1].changes[0].description == 'Исправлена ошибка - 2'
    assert changeLog.versions[1].changes[1].description == 'Исправлена другая ошибка - 2'
    assert changeLog.versions[1].downloads[0].href == 'http://example.com/application_v2_01.zip'
    assert changeLog.versions[1].downloads[1].href == 'http://example.com/application_v2_02.zip'
    assert changeLog.versions[1].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changeLog.versions[1].downloads[1].requirements.os_list == [
        'Windows']
    assert changeLog.versions[1].downloads[0].requirements.api_list == [
        (3, 999), (3, 1111)]
    assert changeLog.versions[1].downloads[1].requirements.api_list == [
        (3, 2222)]


def test_fromString_lang_ru_RU():
    changeLog = ChangeLogFactory.fromString(xmlexample, language='ru_RU')

    assert changeLog.versions[0].version == Version(
        1, 0, status=StatusSet.BETA)
    assert changeLog.versions[0].changes[0].description == 'Исправлена ошибка'
    assert changeLog.versions[0].changes[1].description == 'Исправлена другая ошибка'
    assert changeLog.versions[0].downloads[0].href == 'http://example.com/application_v1_01.zip'
    assert changeLog.versions[0].downloads[1].href == 'http://example.com/application_v1_02.zip'
    assert changeLog.versions[0].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changeLog.versions[0].downloads[1].requirements.os_list == [
        'Windows']
    assert changeLog.versions[0].downloads[0].requirements.api_list == [
        (3, 666), (3, 777)]
    assert changeLog.versions[0].downloads[1].requirements.api_list == [
        (3, 888)]

    assert changeLog.versions[1].version == Version(2, 0)
    assert changeLog.versions[1].changes[0].description == 'Исправлена ошибка - 2'
    assert changeLog.versions[1].changes[1].description == 'Исправлена другая ошибка - 2'
    assert changeLog.versions[1].downloads[0].href == 'http://example.com/application_v2_01.zip'
    assert changeLog.versions[1].downloads[1].href == 'http://example.com/application_v2_02.zip'
    assert changeLog.versions[1].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changeLog.versions[1].downloads[1].requirements.os_list == [
        'Windows']
    assert changeLog.versions[1].downloads[0].requirements.api_list == [
        (3, 999), (3, 1111)]
    assert changeLog.versions[1].downloads[1].requirements.api_list == [
        (3, 2222)]


def test_fromString_lang_default():
    changeLog = ChangeLogFactory.fromString(xmlexample, language='jp')

    assert changeLog.versions[0].version == Version(
        1, 0, status=StatusSet.BETA)
    assert changeLog.versions[0].changes[0].description == 'Fix bug'
    assert changeLog.versions[0].changes[1].description == 'Fix other bug'
    assert changeLog.versions[0].downloads[0].href == 'http://example.com/application_v1_01.zip'
    assert changeLog.versions[0].downloads[1].href == 'http://example.com/application_v1_02.zip'
    assert changeLog.versions[0].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changeLog.versions[0].downloads[1].requirements.os_list == [
        'Windows']
    assert changeLog.versions[0].downloads[0].requirements.api_list == [
        (3, 666), (3, 777)]
    assert changeLog.versions[0].downloads[1].requirements.api_list == [
        (3, 888)]

    assert changeLog.versions[1].version == Version(2, 0)
    assert changeLog.versions[1].changes[0].description == 'Fix bug - 2'
    assert changeLog.versions[1].changes[1].description == 'Fix other bug - 2'
    assert changeLog.versions[1].downloads[0].href == 'http://example.com/application_v2_01.zip'
    assert changeLog.versions[1].downloads[1].href == 'http://example.com/application_v2_02.zip'
    assert changeLog.versions[1].downloads[0].requirements.os_list == [
        'Windows', 'Linux']
    assert changeLog.versions[1].downloads[1].requirements.os_list == [
        'Windows']
    assert changeLog.versions[1].downloads[0].requirements.api_list == [
        (3, 999), (3, 1111)]
    assert changeLog.versions[1].downloads[1].requirements.api_list == [
        (3, 2222)]


def test_fromString_empty():
    changeLog = ChangeLogFactory.fromString('', language='ru')

    assert changeLog.versions == []
