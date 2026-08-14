# -*- coding=utf-8 -*-

import os
from tempfile import NamedTemporaryFile, mkdtemp

import pytest

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
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


@pytest.fixture
def application():
    lang = "en"
    with NamedTemporaryFile(prefix="outwiker_config_", delete=False) as tmp_fp:
        config_file_name = tmp_fp.name

    application = Application()
    application.clear()
    application.init(config_file_name)
    application.testMode = True
    i18config = I18nConfig(application.config)
    i18config.languageOption.value = lang

    yield application

    application.clear()

    if os.path.exists(config_file_name):
        os.remove(config_file_name)
