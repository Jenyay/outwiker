from outwiker.api.core.tree import loadNotesTree
from outwiker.core.tree import WikiDocument
from outwiker.tests.fixtures import wikiroot


def test_default(wikiroot: WikiDocument):
    assert not wikiroot.isExpanded()
    assert not wikiroot["Page 1"].isExpanded()
    assert not wikiroot["Page 2"].isExpanded()
    assert not wikiroot["Page 2/Page 3"].isExpanded()
    assert not wikiroot["Page 2/Page 3/Page 4"].isExpanded()


def test_toggle_expand(wikiroot: WikiDocument):
    pages = [
        wikiroot,
        wikiroot["Page 1"],
        wikiroot["Page 2"],
        wikiroot["Page 2/Page 3"],
        wikiroot["Page 2/Page 3/Page 4"],
    ]
    for page in pages:
        assert not page.isExpanded()

        page.expand(True)
        assert page.isExpanded()

        page.expand(False)
        assert not page.isExpanded()


def test_expand_load(wikiroot: WikiDocument):
    wikiroot["Page 1"].expand(True)
    wikiroot["Page 2"].expand(True)
    wikiroot["Page 2/Page 3/Page 4"].expand(True)

    loaded_wiki = loadNotesTree(wikiroot.path)

    assert loaded_wiki["Page 1"].isExpanded()
    assert loaded_wiki["Page 2"].isExpanded()
    assert not loaded_wiki["Page 2/Page 3"].isExpanded()
    assert loaded_wiki["Page 2/Page 3/Page 4"].isExpanded()


def test_expand_loaded(wikiroot: WikiDocument):
    loaded_wiki = loadNotesTree(wikiroot.path)

    loaded_wiki["Page 1"].expand(True)
    loaded_wiki["Page 2"].expand(True)
    loaded_wiki["Page 2/Page 3/Page 4"].expand(True)

    loaded_wiki_2 = loadNotesTree(wikiroot.path)

    assert loaded_wiki_2["Page 1"].isExpanded()
    assert loaded_wiki_2["Page 2"].isExpanded()
    assert not loaded_wiki_2["Page 2/Page 3"].isExpanded()
    assert loaded_wiki_2["Page 2/Page 3/Page 4"].isExpanded()


def test_expand_readonly(wikiroot: WikiDocument):
    loaded_wiki = loadNotesTree(wikiroot.path, readonly=True)

    loaded_wiki["Page 1"].expand(True)
    loaded_wiki["Page 2"].expand(True)
    loaded_wiki["Page 2/Page 3/Page 4"].expand(True)

    assert loaded_wiki["Page 1"].isExpanded()
    assert loaded_wiki["Page 2"].isExpanded()
    assert not loaded_wiki["Page 2/Page 3"].isExpanded()
    assert loaded_wiki["Page 2/Page 3/Page 4"].isExpanded()

    loaded_wiki_2 = loadNotesTree(wikiroot.path)

    assert not loaded_wiki_2["Page 1"].isExpanded()
    assert not loaded_wiki_2["Page 2"].isExpanded()
    assert not loaded_wiki_2["Page 2/Page 3"].isExpanded()
    assert not loaded_wiki_2["Page 2/Page 3/Page 4"].isExpanded()
