from buildtools.linter import LinterResult, LinterForOutWiker


def test_check_versison_number_ok():
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

    linter = LinterForOutWiker()
    assert linter.check_release_date(text) == (LinterResult.OK, '')


def test_check_check_release_date_error():
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

    linter = LinterForOutWiker()
    assert linter.check_release_date(text)[0] == LinterResult.ERROR


def test_check_check_release_date_error_several():
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

    <version number="3.0.0.870" status="dev" date="23.02.2020">
        <changes>
            <change>bla-bla-bla.</change>
        </changes>

        <changes lang="ru">
            <change>Бла-бла-бла.</change>
        </changes>
    </version>
</versions>
'''

    linter = LinterForOutWiker()
    assert linter.check_release_date(text)[0] == LinterResult.ERROR


def test_check_versisos_list_ok():
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

    linter = LinterForOutWiker()
    assert linter.check_versions_list(text) == (LinterResult.OK, '')


def test_check_versisos_list_error():
    text = '''<?xml version="1.1" encoding="UTF-8" ?>
<versions>
</versions>
'''

    linter = LinterForOutWiker()
    assert linter.check_versions_list(text)[0] == LinterResult.ERROR


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

    linter = LinterForOutWiker()
    assert linter.check_even_versions(text) == (LinterResult.OK, '')


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

    linter = LinterForOutWiker()
    assert linter.check_even_versions(text)[0] == LinterResult.ERROR
