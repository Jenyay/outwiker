# -*- coding=utf-8 -*-

from collections.abc import Iterator
import locale
from pathlib import Path
from tempfile import mkdtemp
from gettext import NullTranslations

# from typing import Protocol

import pytest
import wx

from outwiker.api.core.tree import createNotesTree, WikiPage
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.core import defines
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir
from outwiker.app.owapplication import OutWikerApplication
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester


@pytest.fixture(scope="session")
def samplefiles_path() -> Path:
    """Directory with the sample files used in tests."""
    return Path("testdata/samplefiles/")


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


def _make_application(
    tmp_path_factory,
    *,
    lang: str = "en",
    createTreePanel: bool = False,
    createAttachPanel: bool = False,
    createTagsPanel: bool = False,
    createBookmarksPanel: bool = False,
) -> Application:
    NullTranslations().install()
    config_file_name = str(tmp_path_factory.mktemp("outwiker") / "outwiker.ini")
    application = Application()
    application.clear()
    application.init(config_file_name)
    application.testMode = True
    i18config = I18nConfig(application.config)
    i18config.languageOption.value = lang

    application.sharedData[defines.APP_DATA_CREATE_TREE_PANEL] = createTreePanel
    application.sharedData[defines.APP_DATA_CREATE_ATTACH_PANEL] = createAttachPanel
    application.sharedData[defines.APP_DATA_CREATE_TAGS_PANEL] = createTagsPanel
    application.sharedData[defines.APP_DATA_CREATE_TAGS_PANEL] = createTagsPanel
    application.sharedData[defines.APP_DATA_CREATE_BOOKMARKS_PANEL] = (
        createBookmarksPanel
    )
    return application


@pytest.fixture(scope="module")
def application(tmp_path_factory) -> Iterator[Application]:
    application = _make_application(tmp_path_factory)

    yield application

    application.clear()


# class _OWApplicationFactory(Protocol):
#     def __call__(
#         self,
#         *,
#         lang: str = "en",
#         enableActionsGui: bool = False,
#         createTreePanel: bool = False,
#         createAttachPanel: bool = False,
#         createTagsPanel: bool = False,
#         createBookmarksPanel: bool = False,
#     ) -> tuple[Application, OutWikerApplication]: ...


# @pytest.fixture
# def ow_application_factory(tmp_path_factory) -> Iterator[_OWApplicationFactory]:
#     applications: list[Application] = []
#     ow_applications: list[OutWikerApplication] = []

#     def _make(
#         *,
#         lang: str = "en",
#         enableActionsGui: bool = False,
#         createTreePanel: bool = False,
#         createAttachPanel: bool = False,
#         createTagsPanel: bool = False,
#         createBookmarksPanel: bool = False,
#     ) -> tuple[Application, OutWikerApplication]:
#         if len(applications):
#             application = applications[0]
#             ow_application = ow_applications[0]
#         else:
#             application = _make_application(
#                 tmp_path_factory,
#                 lang=lang,
#                 createTreePanel=createTreePanel,
#                 createAttachPanel=createAttachPanel,
#                 createTagsPanel=createTagsPanel,
#                 createBookmarksPanel=createBookmarksPanel,
#             )
#             applications.append(application)

#             ow_application = OutWikerApplication(application)
#             ow_application.use_fake_html_render = True
#             ow_application.enableActionsGui = enableActionsGui
#             ow_application.initMainWindow()
#             ow_applications.append(ow_application)

#             generalConfig = GeneralGuiConfig(application.config)
#             generalConfig.askBeforeExit.value = False
#             wx.Log.SetLogLevel(0)
#             Tester.dialogTester.clear()

#         return application, ow_application

#     yield _make

#     Tester.dialogTester.clear()

#     ow_application = ow_applications[0]
#     ow_application.destroyMainWindow()
#     wx.SafeYield()
#     ow_application.MainLoop()

#     application = applications[0]
#     application.clear()


@pytest.fixture(scope="module")
def ow_application(application) -> Iterator[OutWikerApplication]:
    enableActionsGui = False

    ow_application = OutWikerApplication(application)
    ow_application.use_fake_html_render = True
    ow_application.enableActionsGui = enableActionsGui
    ow_application.initMainWindow()

    generalConfig = GeneralGuiConfig(application.config)
    generalConfig.askBeforeExit.value = False
    wx.Log.SetLogLevel(0)
    Tester.dialogTester.clear()

    yield ow_application

    Tester.dialogTester.clear()

    ow_application.destroyMainWindow()
    wx.SafeYield()
    ow_application.MainLoop()


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


@pytest.fixture
def main_window(ow_application: OutWikerApplication) -> MainWindow:
    window = ow_application.getMainWindow()
    assert window is not None
    return window


@pytest.fixture
def selected_page(
    ow_application: OutWikerApplication, wikipage: WikiPage
) -> Iterator[WikiPage]:
    """
    Page opened and selected in the application under test.

    The application is shared between the tests of a module, so the wiki is
    closed on teardown.
    """
    application = ow_application.application
    assert application is not None

    Tester.dialogTester.clear()
    application.wikiroot = wikipage.root
    application.selectedPage = wikipage

    yield wikipage

    application.selectedPage = None
    application.wikiroot = None
    Tester.dialogTester.clear()
