import locale
from collections.abc import Callable, Iterator
from gettext import NullTranslations
from pathlib import Path

import pytest
import wx

from outwiker.api.core.tree import WikiDocument, WikiPage, createNotesTree
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.app.owapplication import OutWikerApplication
from outwiker.core import defines
from outwiker.core.application import Application
from outwiker.core.i18n import I18nConfig
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.gui.guiconfig import GeneralGuiConfig
from outwiker.gui.tester import Tester
from outwiker.pages.text.textpage import TextPageFactory


@pytest.fixture(scope="session")
def samplefiles_path() -> Path:
    """Directory with the sample files used in tests."""
    return Path("testdata/samplefiles/")


@pytest.fixture
def wikipage(tmp_path: Path) -> WikiPage:
    """Wiki with a single text page."""
    wikiroot = createNotesTree(tmp_path)
    return TextPageFactory().create(wikiroot, "Страница 1", [])


@pytest.fixture
def wikiroot(tmp_path: Path) -> WikiDocument:
    """Wiki with a tree of text pages."""
    wikiroot = createNotesTree(tmp_path)

    factory = TextPageFactory()
    factory.create(wikiroot, "Page 1", [])
    factory.create(wikiroot, "Page 2", [])
    factory.create(wikiroot["Page 2"], "Page 3", [])
    factory.create(wikiroot["Page 2/Page 3"], "Page 4", [])

    return wikiroot


def _set_panel_flags(
    application: Application,
    *,
    createTreePanel: bool = False,
    createAttachPanel: bool = False,
    createTagsPanel: bool = False,
    createBookmarksPanel: bool = False,
) -> None:
    """Choose the panels created together with the main window."""
    application.sharedData[defines.APP_DATA_CREATE_TREE_PANEL] = createTreePanel
    application.sharedData[defines.APP_DATA_CREATE_ATTACH_PANEL] = createAttachPanel
    application.sharedData[defines.APP_DATA_CREATE_TAGS_PANEL] = createTagsPanel
    application.sharedData[defines.APP_DATA_CREATE_BOOKMARKS_PANEL] = (
        createBookmarksPanel
    )


@pytest.fixture(scope="module")
def application(tmp_path_factory) -> Iterator[Application]:
    """Application without the main window, shared by the tests of a module."""
    NullTranslations().install()
    config_file_name = str(tmp_path_factory.mktemp("outwiker") / "outwiker.ini")

    application = Application()
    application.clear()
    application.init(config_file_name)
    application.testMode = True

    i18config = I18nConfig(application.config)
    i18config.languageOption.value = "en"

    _set_panel_flags(application)

    yield application

    application.clear()


@pytest.fixture(scope="module")
def plugins_loader(
    application: Application,
) -> Iterator[Callable[..., PluginsLoader]]:
    """
    Factory fixture for loading the plugins used by the tests of a module.

    The plugins are loaded once per module (repeated calls for the same
    directories return the same loader) and unloaded after its tests.
    """
    loaders: dict[str, PluginsLoader] = {}

    def _load(*plugin_dirs: str) -> PluginsLoader:
        key = "/".join(plugin_dirs)

        if key not in loaders:
            loader = PluginsLoader(application)
            loader.load(list(plugin_dirs))
            loaders[key] = loader

        return loaders[key]

    yield _load

    for loader in loaders.values():
        loader.clear()


@pytest.fixture(scope="module")
def ow_application_factory(
    application: Application,
) -> Iterator[Callable[..., OutWikerApplication]]:
    """
    Factory creating the OutWiker application with main window over the application fixture.

    The panels are configured through application.sharedData before the main
    window is created, so the tests of a module can choose their own set. All
    the calls inside one module share the same OutWikerApplication.
    """
    created: list[OutWikerApplication] = []

    def _make(
        *,
        enableActionsGui: bool = False,
        createTreePanel: bool = False,
        createAttachPanel: bool = False,
        createTagsPanel: bool = False,
        createBookmarksPanel: bool = False,
    ) -> OutWikerApplication:
        if not created:
            _set_panel_flags(
                application,
                createTreePanel=createTreePanel,
                createAttachPanel=createAttachPanel,
                createTagsPanel=createTagsPanel,
                createBookmarksPanel=createBookmarksPanel,
            )

            ow_application = OutWikerApplication(application)
            ow_application.use_fake_html_render = True
            ow_application.enableActionsGui = enableActionsGui
            ow_application.initMainWindow()
            created.append(ow_application)

            generalConfig = GeneralGuiConfig(application.config)
            generalConfig.askBeforeExit.value = False
            wx.Log.SetLogLevel(0)
            Tester.dialogTester.clear()

        return created[0]

    yield _make

    Tester.dialogTester.clear()

    if created:
        created[0].destroyMainWindow()
        wx.SafeYield()
        created[0].MainLoop()


@pytest.fixture(scope="module")
def ow_application(ow_application_factory) -> OutWikerApplication:
    """Main window of the application with the default parameters."""
    return ow_application_factory()


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
