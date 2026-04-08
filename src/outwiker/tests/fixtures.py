# -*- coding=utf-8 -*-

from tempfile import mkdtemp

import pytest

from outwiker.api.core.tree import createNotesTree
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


@pytest.fixture
def wikipage():
    path = mkdtemp(prefix='outwiker_wiki')
    factory = TextPageFactory()
    wikiroot = createNotesTree(path)
    page = factory.create(wikiroot, "Страница 1", [])

    yield page

    removeDir(path)


@pytest.fixture
def wikiroot():
    path = mkdtemp()
    root = createNotesTree(path)

    factory = TextPageFactory()
    factory.create(root, "Page 1", [])
    factory.create(root, "Page 2", [])
    factory.create(root["Page 2"], "Page 3", [])
    factory.create(root["Page 2/Page 3"], "Page 4", [])

    yield root

    removeDir(path)
