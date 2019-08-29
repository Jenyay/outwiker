# -*- coding: utf-8 -*-

import pytest

from outwiker.core.xmlversionparser import DataForLanguage


def test_init():
    data_for_language = DataForLanguage()
    assert data_for_language.get_languages() == []
    assert data_for_language.get('ru') is None
    assert data_for_language.get('ru', '') == ''
    assert data_for_language.is_empty()

    with pytest.raises(KeyError):
        _ = data_for_language['ru']


def test_set_get():
    test_data = 'hello'
    data_for_language = DataForLanguage()

    data_for_language.set_for_language('', test_data)
    assert data_for_language[''] == test_data
    assert data_for_language.get('') == test_data
    assert data_for_language.get('', None) == test_data
    assert data_for_language.is_empty() == False


def test_set_get_several():
    data_ru = 'Привет'
    data_en = 'Hello'
    data_for_language = DataForLanguage()

    data_for_language.set_for_language('en', data_en)
    data_for_language.set_for_language('ru', data_ru)

    assert data_for_language['en'] == data_en
    assert data_for_language.get('en') == data_en
    assert data_for_language.get('en', None) == data_en

    assert data_for_language['ru'] == data_ru
    assert data_for_language.get('ru') == data_ru
    assert data_for_language.get('ru', None) == data_ru


def test_get_imvalid():
    test_data = 'hello'
    data_for_language = DataForLanguage()

    data_for_language.set_for_language('en', test_data)

    assert data_for_language.get('ru') is None
    assert data_for_language.get('ru', '') == ''

    with pytest.raises(KeyError):
        _ = data_for_language['ru']


def test_test_languages():
    data_ru = 'Привет'
    data_en = 'Hello'
    data_for_language = DataForLanguage()
    data_for_language.set_for_language('en', data_en)
    data_for_language.set_for_language('ru', data_ru)

    assert 'en' in data_for_language.get_languages()
    assert 'ru' in data_for_language.get_languages()

    assert 'en' in data_for_language
    assert 'ru' in data_for_language
