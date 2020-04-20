from buildtools.linter import (LinterStatus, check_release_date,
                               check_versions_list, check_even_versions,
                               check_download_plugin_url, check_changelog_list)


def test_check_release_date_ok():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev" date="20.04.2020">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_release_date(text)

    assert len(report) == 0


def test_check_release_date_error():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_release_date(text)

    assert len(report) == 1
    assert report[0].status == LinterStatus.ERROR


def test_check_release_date_error_several():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>

    <version number="3.0.0.870" status="dev">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_release_date(text)

    assert len(report) == 2
    assert report[0].status == LinterStatus.ERROR
    assert report[1].status == LinterStatus.ERROR


def test_check_versions_list_ok():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev" date="20.04.2020">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_versions_list(text)

    assert len(report) == 0


def test_check_versions_list_error():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
</versions>
'''

    report = check_versions_list(text)

    assert len(report) == 1
    assert report[0].status == LinterStatus.ERROR


def test_check_even_version_ok():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev" date="20.04.2020">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_even_versions(text)

    assert len(report) == 0


def test_check_even_version_error():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.871" status="dev" date="20.04.2020">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_even_versions(text)

    assert len(report) == 1
    assert report[0].status == LinterStatus.ERROR


def test_check_download_plugin_url_ok():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="1.6.1" date="23.02.2020">
        <download href="https://jenyay.net/uploads/Outwiker/WebPage/webpage-1.6.1.zip">
            <requirements>
                <api>3.868</api>
            </requirements>
        </download>
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_download_plugin_url(text)
    assert len(report) == 0


def test_check_download_plugin_url_error():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="1.6.1" date="23.02.2020">
        <download href="https://jenyay.net/uploads/Outwiker/WebPage/webpage-1.6.zip">
            <requirements>
                <api>3.868</api>
            </requirements>
        </download>
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_download_plugin_url(text)

    assert len(report) == 1
    assert report[0].status == LinterStatus.ERROR


def test_check_download_plugin_url_error_several():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="1.6.1" date="23.02.2020">
        <download href="https://jenyay.net/uploads/Outwiker/WebPage/webpage-1.6.zip">
            <requirements>
                <api>3.868</api>
            </requirements>
        </download>

        <download href="https://jenyay.net/uploads/Outwiker/WebPage/webpage-1.5.zip">
            <requirements>
                <api>3.868</api>
            </requirements>
        </download>

        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_download_plugin_url(text)

    assert len(report) == 2
    assert report[0].status == LinterStatus.ERROR
    assert report[1].status == LinterStatus.ERROR


def test_check_changelog_list_ok():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev" date="20.04.2020">
        <changes>
            <change>bla-bla-bla.</change>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_changelog_list(text)

    assert len(report) == 0


def test_check_changelog_list_error_01():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev" date="20.04.2020">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_changelog_list(text)

    assert len(report) == 1
    assert report[0].status == LinterStatus.ERROR


def test_check_changelog_list_error_02():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
    <version number="3.0.0.872" status="dev" date="20.04.2020">
        <changes lang="ru">
            <change>Бла-бла-бла.</change>
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    report = check_changelog_list(text)

    assert len(report) == 1
    assert report[0].status == LinterStatus.ERROR
