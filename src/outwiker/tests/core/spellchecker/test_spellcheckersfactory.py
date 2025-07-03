from outwiker.core.spellchecker.spellcheckersfactory import SpellCheckersFactory

from .fixtures import spell_factory


def test_empty_collection(spell_factory: SpellCheckersFactory):
    assert not spell_factory.isCreated("ru_RU")


def test_create_checker(spell_factory: SpellCheckersFactory):
    langlist = ["ru_RU", "en_US"]
    checker_1 = spell_factory.getSpellChecker(langlist)
    assert len(checker_1.realCheckers) == 2

    for lang in langlist:
        assert spell_factory.isCreated(lang)

    checker_2 = spell_factory.getSpellChecker(langlist)
    assert checker_1.realCheckers[0] is checker_2.realCheckers[0]
    assert checker_1.realCheckers[1] is checker_2.realCheckers[1]


def test_create_checker_with_custom_dict(spell_factory: SpellCheckersFactory):
    langlist = ["ru_RU", "en_US"]
    checker = spell_factory.getSpellChecker(langlist, use_custom_dict=True)
    assert spell_factory.isCreated("")
    assert len(checker.realCheckers) == 2
    assert checker.customDictChecker is not None


def test_create_checker_without_custom_dict(spell_factory: SpellCheckersFactory):
    langlist = ["ru_RU", "en_US"]
    checker = spell_factory.getSpellChecker(langlist, use_custom_dict=False)
    assert not spell_factory.isCreated("")
    assert len(checker.realCheckers) == 2
    assert checker.customDictChecker is None


def test_lang_order(spell_factory: SpellCheckersFactory):
    langlist_1 = ["ru_RU", "en_US"]
    langlist_2 = ["en_US", "ru_RU"]

    checker_1 = spell_factory.getSpellChecker(langlist_1)
    checker_2 = spell_factory.getSpellChecker(langlist_2)
    assert checker_1.realCheckers[0] is checker_2.realCheckers[1]
    assert checker_1.realCheckers[1] is checker_2.realCheckers[0]


def test_lang_case(spell_factory: SpellCheckersFactory):
    langlist_1 = ["ru_RU", "en_US"]
    langlist_2 = ["RU_RU", "EN_US"]

    checker_1 = spell_factory.getSpellChecker(langlist_1)
    checker_2 = spell_factory.getSpellChecker(langlist_2)
    assert checker_1.realCheckers[0] is checker_2.realCheckers[0]
    assert checker_1.realCheckers[1] is checker_2.realCheckers[1]


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
    for lang in langlist:
        assert not spell_factory.isCreated(lang)
