# coding: utf-8

import io

from buildtools.versionstools import VersionsXmlUpdater


def test_set_version_01():
    text_src = io.StringIO('''<?xml version="1.0" encoding="UTF-8"?>
<versions>
    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    version = [1, 2, 3, 4]
    status = ''

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="1.2.3.4">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_02():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    version = [1, 2, 3, 4]
    status = 'beta'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="1.2.3.4" status="beta">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_03():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    version = [1, 2, 3, 4]
    status = 'beta'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="1.2.3.4" status="beta">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_04():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>

    <version number="3.1.0.890" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    version = [1, 2, 3, 4]
    status = 'beta'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="1.2.3.4" status="beta">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>

    <version number="3.1.0.890" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_add_version_01():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    version = [1, 2, 3, 4]
    status = ''

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="1.2.3.4">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>

    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.add_version(text_src, version, status)

    assert new_content == text_expected


def test_add_version_02():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    version = [1, 2, 3, 4]
    status = 'beta'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="1.2.3.4" status="beta">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>

    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.add_version(text_src, version, status)

    assert new_content == text_expected


def test_set_release_date_01():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    date_str = '08.07.2021'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev" date="08.07.2021">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.set_release_date(text_src, date_str)

    assert new_content == text_expected


def test_set_release_date_02():
    text_src = io.StringIO('''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev" date="01.01.2021">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>''')

    date_str = '08.07.2021'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<versions>
    <version number="3.1.0.891" status="dev" date="08.07.2021">
        <changes>
        </changes>

        <changes lang="ru">
        </changes>
    </version>
</versions>'''

    updater = VersionsXmlUpdater()
    new_content = updater.set_release_date(text_src, date_str)

    assert new_content == text_expected
