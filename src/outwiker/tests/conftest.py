# -*- coding=utf-8 -*-

from collections.abc import Iterator
import locale
from tempfile import mkdtemp
from gettext import NullTranslations

import pytest
import wx

from outwiker.api.core.tree import createNotesTree
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


@pytest.fixture
def wikipage():
    path = mkdtemp(prefix="outwiker_wiki")
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


@pytest.fixture(scope="module")
def application(tmp_path_factory) -> Iterator[Application]:
    lang = "en"
    NullTranslations().install()
    config_file_name = str(tmp_path_factory.mktemp("outwiker") / "outwiker.ini")
    application = Application()
    application.clear()
    application.init(config_file_name)
    application.testMode = True
    i18config = I18nConfig(application.config)
    i18config.languageOption.value = lang

    yield application

    application.clear()


@pytest.fixture(scope="module")
def wxapp() -> Iterator[wx.App]:
    app = wx.App()
    locale.setlocale(locale.LC_ALL, "")

    yield app

    app.MainLoop()
    app.Destroy()


@pytest.fixture
def empty_window(wxapp) -> Iterator[wx.Frame]:
    frame = wx.Frame(None)
    wxapp.SetTopWindow(frame)

    yield frame

    if frame:
        frame.Close()
    wx.SafeYield()
