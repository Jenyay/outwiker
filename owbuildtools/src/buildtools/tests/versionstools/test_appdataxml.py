# coding: utf-8

from io import StringIO

from buildtools.versionstools import AppDataXmlUpdater


def test_set_version_01():
    text_src = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" date="2021-01-01" />
  </releases>
</component>'''

    version = [1, 2, 3, 4]
    status = None

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="1.2.3.4" date="2021-01-01" />
  </releases>
</component>'''

    updater = AppDataXmlUpdater()
    new_content = updater.set_version(StringIO(text_src), version, status)

    assert new_content == text_expected


def test_set_version_02():
    text_src = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" />
  </releases>
</component>'''

    version = [1, 2, 3, 4]
    status = None

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="1.2.3.4" />
  </releases>
</component>'''

    updater = AppDataXmlUpdater()
    new_content = updater.set_version(StringIO(text_src), version, status)

    assert new_content == text_expected


def test_add_version_01():
    text_src = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" date="2021-01-01" />
  </releases>
</component>'''

    version = [3, 2, 0, 900]
    status = None

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.2.0.900" />
    <release version="3.1.0.891" date="2021-01-01" />
  </releases>
</component>'''

    updater = AppDataXmlUpdater()
    new_content = updater.add_version(StringIO(text_src), version, status)

    assert new_content == text_expected


def test_set_date_01():
    text_src = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" date="2021-01-01" />
  </releases>
</component>'''

    date_str = '2022-07-11'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" date="2022-07-11" />
  </releases>
</component>'''

    updater = AppDataXmlUpdater()
    new_content = updater.set_release_date(StringIO(text_src), date_str)

    assert new_content == text_expected


def test_set_date_02():
    text_src = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" />
  </releases>
</component>'''

    date_str = '2022-07-11'

    text_expected = '''<?xml version='1.0' encoding='UTF-8'?>
<component type="desktop">
  <releases>
    <release version="3.1.0.891" date="2022-07-11" />
  </releases>
</component>'''

    updater = AppDataXmlUpdater()
    new_content = updater.set_release_date(StringIO(text_src), date_str)

    assert new_content == text_expected
