# coding: utf-8

import io

from buildtools.versionstools import InitUpdater


def test_set_version_01():
    text_src = io.StringIO('''
__version__ = (3, 1, 0, 891)
__status__ = ''
__api_version__ = (3, 890)''')

    version = [1, 2, 3, 4]
    status = ''

    text_expected = '''
__version__ = (1, 2, 3, 4)
__status__ = ''
__api_version__ = (3, 890)'''

    updater = InitUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_02():
    text_src = io.StringIO('''
__status__ = ''
__version__ = (3, 1, 0, 891)
__api_version__ = (3, 890)''')

    version = [1, 2, 3, 4]
    status = ''

    text_expected = '''
__status__ = ''
__version__ = (1, 2, 3, 4)
__api_version__ = (3, 890)'''

    updater = InitUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_03():
    text_src = io.StringIO('''
__version__ = (3, 1, 0, 891)
__status__ = 'beta'
__api_version__ = (3, 890)''')

    version = [1, 2, 3, 4]
    status = 'dev'

    text_expected = '''
__version__ = (1, 2, 3, 4)
__status__ = 'dev'
__api_version__ = (3, 890)'''

    updater = InitUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_04():
    text_src = io.StringIO('''
__version__ = (3, 1, 0, 891)
__status__ = ''
__api_version__ = (3, 890)''')

    version = [1, 2, 3, 4]
    status = 'dev'

    text_expected = '''
__version__ = (1, 2, 3, 4)
__status__ = 'dev'
__api_version__ = (3, 890)'''

    updater = InitUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_05():
    text_src = io.StringIO('''
__version__ = (3, 1, 0, 891)
__status__ = "beta"
__api_version__ = (3, 890)''')

    version = [1, 2, 3, 4]
    status = 'dev'

    text_expected = '''
__version__ = (1, 2, 3, 4)
__status__ = 'dev'
__api_version__ = (3, 890)'''

    updater = InitUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected


def test_set_version_06():
    text_src = io.StringIO('''
    __version__ = (3, 1, 0, 891)
    __status__ = "beta"
    __api_version__ = (3, 890)''')

    version = [1, 2, 3, 4]
    status = 'dev'

    text_expected = '''
    __version__ = (1, 2, 3, 4)
    __status__ = 'dev'
    __api_version__ = (3, 890)'''

    updater = InitUpdater()
    new_content = updater.set_version(text_src, version, status)

    assert new_content == text_expected
