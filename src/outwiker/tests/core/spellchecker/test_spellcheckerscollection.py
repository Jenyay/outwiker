import os
import os.path
import shutil
from tempfile import mkdtemp

import pytest

from outwiker.core.spellchecker.spellcheckerscollection import SpellCheckersCollection
from outwiker.tests.utils import removeDir


@pytest.fixture
def spell_collection():
    dst_path_to_dicts = mkdtemp(prefix='tmp spell test')

    if not os.path.exists(dst_path_to_dicts):
        os.mkdir(dst_path_to_dicts)

    src_dict_path = os.path.join('src', 'outwiker', 'data', 'spell')
    _copy_dict_from("ru_RU", src_dict_path, dst_path_to_dicts)
    _copy_dict_from("en_US", src_dict_path, dst_path_to_dicts)

    yield SpellCheckersCollection([dst_path_to_dicts])

    removeDir(dst_path_to_dicts)


def _copy_dict_from(lang, src_dict_path, dst_path_to_dicts):
    fname_dic = os.path.join(src_dict_path, lang + ".dic")
    fname_aff = os.path.join(src_dict_path, lang + ".aff")

    shutil.copy(fname_dic, dst_path_to_dicts)
    shutil.copy(fname_aff, dst_path_to_dicts)

def test_empty_collection(spell_collection: SpellCheckersCollection):
    langlist = ["ru_RU", "en_US"]
    assert not spell_collection.isCreated(langlist)


def test_create_checker(spell_collection: SpellCheckersCollection):
    langlist = ["ru_RU", "en_US"]
    checker_1 = spell_collection.getSpellChecker(langlist)
    assert spell_collection.isCreated(langlist)

    checker_2 = spell_collection.getSpellChecker(langlist)
    assert checker_1 is checker_2


def test_lang_order(spell_collection: SpellCheckersCollection):
    langlist_1 = ["ru_RU", "en_US"]
    langlist_2 = ["en_US", "ru_RU"]

    checker_1 = spell_collection.getSpellChecker(langlist_1)
    checker_2 = spell_collection.getSpellChecker(langlist_2)
    assert checker_1 is checker_2


def test_lang_case(spell_collection: SpellCheckersCollection):
    langlist_1 = ["ru_RU", "en_US"]
    langlist_2 = ["RU_RU", "EN_US"]

    checker_1 = spell_collection.getSpellChecker(langlist_1)
    checker_2 = spell_collection.getSpellChecker(langlist_2)
    assert checker_1 is checker_2


def test_other_lang(spell_collection: SpellCheckersCollection):
    langlist_1 = ["ru_RU"]
    langlist_2 = ["en_US"]

    checker_1 = spell_collection.getSpellChecker(langlist_1)
    checker_2 = spell_collection.getSpellChecker(langlist_2)
    assert checker_1 is not checker_2
