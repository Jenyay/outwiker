from outwiker.core.spellchecker.spellcheckersfactory import SpellCheckersFactory

from .fixtures import spell_factory


def test_empty_collection(spell_factory: SpellCheckersFactory):
    langlist = ["ru_RU", "en_US"]
    assert not spell_factory.isCreated(langlist)


def test_create_checker(spell_factory: SpellCheckersFactory):
    langlist = ["ru_RU", "en_US"]
    checker_1 = spell_factory.getSpellChecker(langlist)
    assert spell_factory.isCreated(langlist)

    checker_2 = spell_factory.getSpellChecker(langlist)
    assert checker_1 is checker_2


def test_lang_order(spell_factory: SpellCheckersFactory):
    langlist_1 = ["ru_RU", "en_US"]
    langlist_2 = ["en_US", "ru_RU"]

    checker_1 = spell_factory.getSpellChecker(langlist_1)
    checker_2 = spell_factory.getSpellChecker(langlist_2)
    assert checker_1 is checker_2


def test_lang_case(spell_factory: SpellCheckersFactory):
    langlist_1 = ["ru_RU", "en_US"]
    langlist_2 = ["RU_RU", "EN_US"]

    checker_1 = spell_factory.getSpellChecker(langlist_1)
    checker_2 = spell_factory.getSpellChecker(langlist_2)
    assert checker_1 is checker_2


def test_other_lang(spell_factory: SpellCheckersFactory):
    langlist_1 = ["ru_RU"]
    langlist_2 = ["en_US"]

    checker_1 = spell_factory.getSpellChecker(langlist_1)
    checker_2 = spell_factory.getSpellChecker(langlist_2)
    assert checker_1 is not checker_2


def test_clear(spell_factory: SpellCheckersFactory):
    langlist = ["ru_RU", "en_US"]
    spell_factory.getSpellChecker(langlist)
    spell_factory.clear()
    assert not spell_factory.isCreated(langlist)
