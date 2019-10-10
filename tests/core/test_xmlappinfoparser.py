# -*- coding: utf-8 -*-

from datetime import datetime

from outwiker.core.xmlappinfoparser import (XmlAppInfoParser, XmlAppInfo,
                                            XmlChangelogParser)


def _assert_XmlAppInfo_empty(appinfo):
    assert appinfo.app_info_url == ""
    assert appinfo.authors.is_empty()
    assert appinfo.app_name.is_empty()
    assert appinfo.version is None
    assert appinfo.requirements.os_list == []
    assert appinfo.requirements.api_list == []
    assert appinfo.description.is_empty()
    assert appinfo.website.is_empty()


def test_empty_01():
    text = ""
    result = XmlAppInfoParser().parse(text)     # type: XmlAppInfo

    assert isinstance(result, XmlAppInfo)
    _assert_XmlAppInfo_empty(result)


def test_empty_02():
    text = '<?xml version="1.1" encoding="UTF-8" ?>'
    result = XmlAppInfoParser().parse(text)

    assert isinstance(result, XmlAppInfo)
    _assert_XmlAppInfo_empty(result)


def test_empty_03():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info></info>'''
    result = XmlAppInfoParser().parse(text)

    assert isinstance(result, XmlAppInfo)
    _assert_XmlAppInfo_empty(result)


def test_name_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <name></name>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.app_name.get_languages() == ['']
    assert result.app_name[''] == ''


def test_name_no_language():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <name>Application name</name>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.app_name.get_languages() == ['']
    assert result.app_name[''] == 'Application name'


def test_name_en():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <name lang="en">Application name</name>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.app_name.get_languages() == ['en']
    assert result.app_name['en'] == 'Application name'


def test_name_en_ru():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <name lang="en">Application name</name>
    <name lang="ru">Имя приложения</name>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert 'en' in result.app_name.get_languages()
    assert 'ru' in result.app_name.get_languages()
    assert len(result.app_name.get_languages()) == 2
    assert result.app_name['en'] == 'Application name'
    assert result.app_name['ru'] == 'Имя приложения'


def test_website_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <website></website>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.website.get_languages() == ['']
    assert result.website[''] == ''


def test_website_no_language():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <website>http://jenyay.net</website>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.website.get_languages() == ['']
    assert result.website[''] == 'http://jenyay.net'


def test_website_en():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <website lang="en">http://jenyay.net</website>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.website.get_languages() == ['en']
    assert result.website['en'] == 'http://jenyay.net'


def test_website_en_ru():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <website lang="en">http://jenyay.net/en/</website>
    <website lang="ru">http://jenyay.net/ru/</website>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert 'en' in result.website.get_languages()
    assert 'ru' in result.website.get_languages()
    assert len(result.website.get_languages()) == 2
    assert result.website['en'] == 'http://jenyay.net/en/'
    assert result.website['ru'] == 'http://jenyay.net/ru/'


def test_description_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <description></description>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.description.get_languages() == ['']
    assert result.description[''] == ''


def test_description_no_language():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <description>Description</description>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.description.get_languages() == ['']
    assert result.description[''] == 'Description'


def test_description_en():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <description lang="en">Description</description>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.description.get_languages() == ['en']
    assert result.description['en'] == 'Description'


def test_description_en_ru():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <description lang="en">Description</description>
    <description lang="ru">Описание</description>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert 'en' in result.description.get_languages()
    assert 'ru' in result.description.get_languages()
    assert len(result.description.get_languages()) == 2
    assert result.description['en'] == 'Description'
    assert result.description['ru'] == 'Описание'


def test_app_info_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <updates></updates>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.app_info_url == ''


def test_app_updates_url():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <updates_url>http://example.com/updates.xml</updates_url>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.app_updates_url == 'http://example.com/updates.xml'


def test_app_info_url():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<info>
    <info_url>http://example.com/info.xml</info_url>
</info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.app_info_url == 'http://example.com/info.xml'


def test_authors_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
            <author></author>
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.authors[''][0].name == ''
    assert result.authors[''][0].email == ''
    assert result.authors[''][0].website == ''


def test_authors_empty_en():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
            <author lang='en'></author>
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.authors['en'][0].name == ''
    assert result.authors['en'][0].email == ''
    assert result.authors['en'][0].website == ''


def test_authors_empty_en_no_lang():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
            <author></author>
            <author lang='en'></author>
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.authors[''][0].name == ''
    assert result.authors[''][0].email == ''
    assert result.authors[''][0].website == ''

    assert result.authors['en'][0].name == ''
    assert result.authors['en'][0].email == ''
    assert result.authors['en'][0].website == ''


def test_authors_empty_ru_no_lang_full():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
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
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert '' in result.authors.get_languages()
    assert 'ru' in result.authors.get_languages()
    assert len(result.authors.get_languages()) == 2

    assert result.authors[''][0].name == 'John'
    assert result.authors[''][0].email == 'john@example.com'
    assert result.authors[''][0].website == 'http://example.com'

    assert result.authors['ru'][0].name == 'Джон'
    assert result.authors['ru'][0].email == 'john_ru@example.com'
    assert result.authors['ru'][0].website == 'http://example.com/ru'


def test_authors_several():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
            <author>
                <name>John</name>
                <email>john@example.com</email>
                <website>http://example.com/john/en</website>
            </author>

            <author lang='ru'>
                <name>Джон</name>
                <email>john_ru@example.com</email>
                <website>http://example.com/john/ru</website>
            </author>

            <author>
                <name>Andrey</name>
                <email>andrey@example.com</email>
                <website>http://example.com/andrey/en</website>
            </author>

            <author lang='ru'>
                <name>Андрей</name>
                <email>andrey_ru@example.com</email>
                <website>http://example.com/andrey/ru</website>
            </author>
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert '' in result.authors.get_languages()
    assert 'ru' in result.authors.get_languages()
    assert len(result.authors.get_languages()) == 2

    assert result.authors[''][0].name == 'John'
    assert result.authors[''][0].email == 'john@example.com'
    assert result.authors[''][0].website == 'http://example.com/john/en'

    assert result.authors['ru'][0].name == 'Джон'
    assert result.authors['ru'][0].email == 'john_ru@example.com'
    assert result.authors['ru'][0].website == 'http://example.com/john/ru'

    assert result.authors[''][1].name == 'Andrey'
    assert result.authors[''][1].email == 'andrey@example.com'
    assert result.authors[''][1].website == 'http://example.com/andrey/en'

    assert result.authors['ru'][1].name == 'Андрей'
    assert result.authors['ru'][1].email == 'andrey_ru@example.com'
    assert result.authors['ru'][1].website == 'http://example.com/andrey/ru'


def test_versions_list_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions></versions>'''
    result = XmlChangelogParser.parse(text)

    assert result.versions == []


def test_versions_empty_internal():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version></version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert result.versions == []


def test_versions_attributes():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0" status="dev" date="29.08.2019"></version>
            <version number="1.1" status="beta" date="30.08.2019"></version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert len(result.versions) == 2
    assert result.versions[0].number == '1.0'
    assert result.versions[0].status == 'dev'
    assert result.versions[0].date == datetime(2019, 8, 29)
    assert result.versions[0].changes.is_empty()

    assert result.versions[1].number == '1.1'
    assert result.versions[1].status == 'beta'
    assert result.versions[1].date == datetime(2019, 8, 30)
    assert result.versions[1].changes.is_empty()


def test_versions_no_number():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0" status="dev" date="29.08.2019"></version>
            <version status="beta" date="30.08.2019"></version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert len(result.versions) == 1
    assert result.versions[0].number == '1.0'
    assert result.versions[0].status == 'dev'
    assert result.versions[0].date == datetime(2019, 8, 29)
    assert result.versions[0].changes.is_empty()


def test_versions_changes_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <changes></changes>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert len(result.versions) == 1
    assert result.versions[0].changes.get_languages() == ['']
    assert result.versions[0].changes[''] == []


def test_versions_changes_languages_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <changes></changes>
                <changes lang="ru"></changes>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert len(result.versions) == 1
    assert len(result.versions[0].changes.get_languages()) == 2
    assert '' in result.versions[0].changes.get_languages()
    assert 'ru' in result.versions[0].changes.get_languages()
    assert result.versions[0].changes[''] == []
    assert result.versions[0].changes['ru'] == []


def test_versions_changes_items():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <changes>
                    <change>Fix bug</change>
                    <change>Fix other bug</change>
                </changes>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert '' in result.versions[0].changes.get_languages()
    assert result.versions[0].changes[''][0].description == 'Fix bug'
    assert result.versions[0].changes[''][1].description == 'Fix other bug'


def test_versions_changes_lang_en():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <changes lang="en">
                    <change>Fix bug</change>
                    <change>Fix other bug</change>
                </changes>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert 'en' in result.versions[0].changes.get_languages()
    assert result.versions[0].changes['en'][0].description == 'Fix bug'
    assert result.versions[0].changes['en'][1].description == 'Fix other bug'


def test_versions_changes_lang_default_ru():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <changes>
                    <change>Fix bug</change>
                    <change>Fix other bug</change>
                </changes>

                <changes lang="ru">
                    <change>Исправлена ошибка</change>
                    <change>Исправлена другая ошибка</change>
                </changes>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert '' in result.versions[0].changes.get_languages()
    assert 'ru' in result.versions[0].changes.get_languages()

    assert result.versions[0].changes[''][0].description == 'Fix bug'
    assert result.versions[0].changes[''][1].description == 'Fix other bug'

    assert result.versions[0].changes['ru'][0].description == 'Исправлена ошибка'
    assert result.versions[0].changes['ru'][1].description == 'Исправлена другая ошибка'


def test_versions_download_empty():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download></download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert result.versions[0].downloads == []


def test_versions_download_url():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download href="http://example.com/application.zip"></download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert len(result.versions[0].downloads) == 1
    assert result.versions[0].downloads[0].href == 'http://example.com/application.zip'
    assert not result.versions[0].downloads[0].requirements.os_list
    assert not result.versions[0].downloads[0].requirements.api_list


def test_versions_download_url_several():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download href="http://example.com/application.zip"></download>
                <download href="http://example.com/application_2.zip"></download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert len(result.versions[0].downloads) == 2
    assert result.versions[0].downloads[0].href == 'http://example.com/application.zip'
    assert not result.versions[0].downloads[0].requirements.os_list
    assert not result.versions[0].downloads[0].requirements.api_list

    assert result.versions[0].downloads[1].href == 'http://example.com/application_2.zip'
    assert not result.versions[0].downloads[0].requirements.os_list
    assert not result.versions[0].downloads[0].requirements.api_list


def test_versions_download_requirements():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download href="http://example.com/application.zip">
                    <requirements>
                    </requirements>
                </download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert not result.versions[0].downloads[0].requirements.os_list
    assert not result.versions[0].downloads[0].requirements.api_list


def test_versions_download_requirements_os():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download href="http://example.com/application.zip">
                    <requirements>
                        <os>Windows</os>
                        <os>Linux</os>
                    </requirements>
                </download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert 'Windows' in result.versions[0].downloads[0].requirements.os_list
    assert 'Linux' in result.versions[0].downloads[0].requirements.os_list
    assert not result.versions[0].downloads[0].requirements.api_list


def test_versions_download_requirements_api():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download href="http://example.com/application.zip">
                    <requirements>
                        <api>3.666</api>
                        <api>3.667</api>
                    </requirements>
                </download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert not result.versions[0].downloads[0].requirements.os_list
    assert (3, 666) in result.versions[0].downloads[0].requirements.api_list
    assert (3, 667) in result.versions[0].downloads[0].requirements.api_list


def test_versions_download_requirements_os_api():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <versions>
            <version number="1.0">
                <download href="http://example.com/application.zip">
                    <requirements>
                        <os>Windows</os>
                        <os>Linux</os>
                        <api>3.666</api>
                        <api>3.667</api>
                    </requirements>
                </download>
            </version>
        </versions>'''
    result = XmlChangelogParser.parse(text)

    assert 'Windows' in result.versions[0].downloads[0].requirements.os_list
    assert 'Linux' in result.versions[0].downloads[0].requirements.os_list
    assert (3, 666) in result.versions[0].downloads[0].requirements.api_list
    assert (3, 667) in result.versions[0].downloads[0].requirements.api_list


def test_requirements_os_api():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
            <requirements>
                <os>Windows</os>
                <os>Linux</os>
                <api>3.666</api>
                <api>3.667</api>
            </requirements>
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert 'Windows' in result.requirements.os_list
    assert 'Linux' in result.requirements.os_list
    assert (3, 666) in result.requirements.api_list
    assert (3, 667) in result.requirements.api_list


def test_version():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
        <info>
            <version number="1.0" status="dev"/>
        </info>'''
    result = XmlAppInfoParser().parse(text)

    assert result.version.number == '1.0'
    assert result.version.status == 'dev'
