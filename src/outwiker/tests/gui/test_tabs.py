"""Tests for the tabs with the opened pages."""

from collections.abc import Iterator
from os.path import basename
from pathlib import Path

import pytest

from outwiker.api.core.tree import (
    WikiDocument,
    WikiPage,
    createNotesTree,
    loadNotesTree,
)
from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.app.gui.mainwindow import MainWindow
from outwiker.app.gui.tabscontroller import TabsController
from outwiker.app.owapplication import OutWikerApplication
from outwiker.core.application import Application
from outwiker.pages.text.textpage import TextPageFactory


@pytest.fixture(scope="module")
def ow_application(ow_application_factory) -> OutWikerApplication:
    """Main window with the actions GUI, the tests check its menus."""
    return ow_application_factory(enableActionsGui=True)


@pytest.fixture
def wikiroot(application: Application, tmp_path: Path) -> Iterator[WikiDocument]:
    """Wiki with the pages used in the tests. It is closed after the test."""
    wikiroot = createNotesTree(tmp_path)

    factory = TextPageFactory()
    factory.create(wikiroot, "Страница 1", [])
    factory.create(wikiroot, "Страница 2", [])
    factory.create(wikiroot["Страница 2"], "Страница 3", [])
    factory.create(wikiroot["Страница 2/Страница 3"], "Страница 4", [])
    factory.create(wikiroot["Страница 1"], "Страница 5", [])

    yield wikiroot

    application.selectedPage = None
    application.wikiroot = None


@pytest.fixture
def tabs(main_window: MainWindow) -> TabsController:
    """Tabs controller of the main window."""
    return main_window.tabsController


@pytest.fixture
def opened_wiki(application: Application, wikiroot: WikiDocument) -> WikiDocument:
    """Wiki opened in the application with the first page selected."""
    application.wikiroot = wikiroot
    application.selectedPage = wikiroot["Страница 1"]
    return wikiroot


@pytest.fixture
def three_tabs(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """Wiki with three tabs opened: Страница 1, Страница 2, Страница 2/Страница 3."""
    tabs.openInTab(opened_wiki["Страница 2"], True)
    tabs.openInTab(opened_wiki["Страница 2/Страница 3"], True)


@pytest.fixture
def five_tabs(tabs: TabsController, opened_wiki: WikiDocument) -> list[WikiPage]:
    """
    Five pages opened in the tabs in the following order:

        Страница 1, Страница 2, Страница 2/Страница 3,
        Страница 2/Страница 3/Страница 4, Страница 1/Страница 5
    """
    pages = [
        opened_wiki["Страница 1"],
        opened_wiki["Страница 2"],
        opened_wiki["Страница 2/Страница 3"],
        opened_wiki["Страница 2/Страница 3/Страница 4"],
        opened_wiki["Страница 1/Страница 5"],
    ]

    for page in pages[1:]:
        tabs.addNewTab(page, False)

    return pages


def _get_history_state(application: Application) -> tuple[bool, bool]:
    """Whether the back and the forward history actions are enabled."""
    actionController = application.actionController
    info_back = actionController.getActionInfo(HistoryBackAction.stringId)
    info_forward = actionController.getActionInfo(HistoryForwardAction.stringId)

    return (info_back.menuItem.IsEnabled(), info_forward.menuItem.IsEnabled())


def _run_history_action(application: Application, action) -> None:
    """Run the history action by its string id."""
    application.actionController.getAction(action.stringId).run(None)


def test_init(tabs: TabsController) -> None:
    """There are no tabs while no wiki is opened."""
    assert tabs.getTabsCount() == 0


def test_clone_empty_01(tabs: TabsController) -> None:
    """The tab is not cloned while no wiki is opened."""
    assert tabs.getTabsCount() == 0

    tabs.cloneTab()

    assert tabs.getTabsCount() == 0


def test_clone_empty_02(
    tabs: TabsController, application: Application, wikiroot: WikiDocument
) -> None:
    """The tab without a page is cloned when no page is selected."""
    application.wikiroot = wikiroot
    application.selectedPage = None
    assert tabs.getTabsCount() == 1

    tabs.cloneTab()

    assert tabs.getTabsCount() == 2
    assert tabs.getPage(0) is None
    assert tabs.getPage(1) is None


def test_open_wiki(
    tabs: TabsController, application: Application, wikiroot: WikiDocument
) -> None:
    """The wiki without the saved tabs is opened with a single empty tab."""
    application.wikiroot = wikiroot

    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0
    assert tabs.getPage(0) is None
    # There is no selected page, so the tab title is the name of the wiki directory
    assert tabs.getTabTitle(0) == basename(wikiroot.path)


def test_selection(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The selected page is shown in the current tab."""
    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0
    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"

    application.selectedPage = opened_wiki["Страница 2/Страница 3"]
    assert tabs.getPage(0) == opened_wiki["Страница 2/Страница 3"]
    assert tabs.getTabTitle(0) == "Страница 3"

    application.selectedPage = opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getPage(0) == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getTabTitle(0) == "Страница 4"


def test_clone_tab_01(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """The cloned tab shows the page of the current tab."""
    tabs.cloneTab()

    assert tabs.getTabsCount() == 2
    assert tabs.getSelection() == 1
    assert tabs.getPage(1) == opened_wiki["Страница 1"]
    assert tabs.getTabTitle(1) == "Страница 1"

    tabs.cloneTab()

    assert tabs.getTabsCount() == 3
    assert tabs.getSelection() == 2


def test_clone_tab_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """Each tab shows the page that was selected when it was cloned."""
    tabs.cloneTab()
    application.selectedPage = opened_wiki["Страница 2"]
    tabs.cloneTab()
    application.selectedPage = opened_wiki["Страница 2/Страница 3/Страница 4"]

    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"

    assert tabs.getPage(1) == opened_wiki["Страница 2"]
    assert tabs.getTabTitle(1) == "Страница 2"

    assert tabs.getPage(2) == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getTabTitle(2) == "Страница 4"


def test_remove_selection(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """The tab becomes empty when the selected page is removed."""
    opened_wiki["Страница 1"].remove()

    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0
    assert tabs.getPage(0) is None
    assert tabs.getTabTitle(0) == basename(opened_wiki.path)


def test_remove_selection_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The tab of the removed parent page becomes empty."""
    tabs.cloneTab()
    application.selectedPage = opened_wiki["Страница 2/Страница 3/Страница 4"]

    opened_wiki["Страница 2"].remove()

    assert tabs.getTabsCount() == 2
    assert tabs.getSelection() == 1
    assert tabs.getPage(1) is None
    assert tabs.getTabTitle(1) == basename(opened_wiki.path)


def test_remove_selection_03(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The tab becomes empty when the selected page is removed with its children."""
    tabs.cloneTab()
    application.selectedPage = opened_wiki["Страница 2"]

    opened_wiki["Страница 2"].remove()

    assert tabs.getTabsCount() == 2
    assert tabs.getSelection() == 1
    assert tabs.getPage(1) is None
    assert tabs.getTabTitle(1) == basename(opened_wiki.path)


def test_rename_selection(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """The tab title follows the renamed selected page."""
    opened_wiki["Страница 1"].title = "Бла-бла-бла"

    assert tabs.getSelection() == 0
    assert tabs.getPage(0) == opened_wiki["Бла-бла-бла"]
    assert tabs.getTabTitle(0) == "Бла-бла-бла"


def test_rename(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """All the tabs with the renamed page change their titles."""
    tabs.cloneTab()
    tabs.cloneTab()
    opened_wiki["Страница 1"].title = "Бла-бла-бла"

    for index in range(3):
        assert tabs.getPage(index) == opened_wiki["Бла-бла-бла"]
        assert tabs.getTabTitle(index) == "Бла-бла-бла"


def test_remove_01(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """The cloned tabs of the removed page are closed, the current one is emptied."""
    tabs.cloneTab()
    tabs.cloneTab()

    opened_wiki["Страница 1"].remove()

    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0
    assert tabs.getPage(0) is None
    assert tabs.getTabTitle(0) == basename(opened_wiki.path)


def test_remove_02(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """The removed page closes all its tabs, the remained one keeps its page."""
    tabs.cloneTab()
    tabs.cloneTab()
    tabs.openInTab(opened_wiki["Страница 2"], True)

    opened_wiki["Страница 1"].remove()

    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0
    assert tabs.getPage(0) == opened_wiki["Страница 2"]
    assert tabs.getTabTitle(0) == "Страница 2"


def test_remove_03(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """The removed page closes the tabs that are not selected."""
    tabs.cloneTab()
    tabs.cloneTab()
    tabs.openInTab(opened_wiki["Страница 2"], False)

    opened_wiki["Страница 1"].remove()

    assert tabs.getTabsCount() == 2
    assert tabs.getSelection() == 0

    assert tabs.getPage(0) is None
    assert tabs.getTabTitle(0) == basename(opened_wiki.path)

    assert tabs.getPage(1) == opened_wiki["Страница 2"]
    assert tabs.getTabTitle(1) == "Страница 2"


def test_remove_04(tabs: TabsController, opened_wiki: WikiDocument) -> None:
    """All the tabs of the removed page are closed."""
    tabs.openInTab(opened_wiki["Страница 2"], False)
    tabs.openInTab(opened_wiki["Страница 2"], False)
    tabs.openInTab(opened_wiki["Страница 2"], False)

    opened_wiki["Страница 2"].remove()

    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0

    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"


def test_open_in_tab_01(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The selected page is opened in the new selected tab."""
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], True)

    assert application.selectedPage == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getSelection() == 1
    assert tabs.getPage(1) == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getTabTitle(1) == "Страница 4"


def test_open_in_tab_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The page is opened in the new tab that is not selected."""
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], False)

    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0

    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"

    assert tabs.getPage(1) == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getTabTitle(1) == "Страница 4"


def test_open_in_tab_03(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The new tab is inserted after the current tab."""
    tabs.cloneTab()
    tabs.cloneTab()

    tabs.setSelection(0)
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], True)

    assert application.selectedPage == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getSelection() == 1
    assert tabs.getPage(1) == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getTabTitle(1) == "Страница 4"


def test_set_selection(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The page of the selected tab becomes the selected page."""
    tabs.openInTab(opened_wiki["Страница 2"], False)
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], False)

    assert tabs.getSelection() == 0
    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"

    tabs.setSelection(2)
    assert application.selectedPage == opened_wiki["Страница 2"]
    assert tabs.getSelection() == 2
    assert tabs.getPage(2) == opened_wiki["Страница 2"]

    tabs.setSelection(1)
    assert application.selectedPage == opened_wiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getSelection() == 1
    assert tabs.getPage(1) == opened_wiki["Страница 2/Страница 3/Страница 4"]


def test_close_wiki(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """There are no tabs when the wiki is closed."""
    application.wikiroot = None

    assert tabs.getTabsCount() == 0


def test_save_tabs_01(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The current tab is restored after the wiki is reopened."""
    application.wikiroot = None
    assert tabs.getTabsCount() == 0

    otherwiki = loadNotesTree(opened_wiki.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 1
    assert tabs.getSelection() == 0
    assert tabs.getPage(0) == otherwiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"


def test_save_tabs_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """All the tabs are restored in the saved order after the wiki is reopened."""
    tabs.openInTab(opened_wiki["Страница 2"], False)
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], False)

    application.wikiroot = None
    assert tabs.getTabsCount() == 0

    otherwiki = loadNotesTree(opened_wiki.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 3
    assert tabs.getSelection() == 0

    assert tabs.getPage(0) == otherwiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"
    assert tabs.getPage(1) == otherwiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getPage(2) == otherwiki["Страница 2"]


def test_save_tabs_03(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The selected tab is restored after the wiki is reopened."""
    tabs.openInTab(opened_wiki["Страница 2"], False)
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], False)
    tabs.setSelection(1)

    application.wikiroot = None
    assert tabs.getTabsCount() == 0

    otherwiki = loadNotesTree(opened_wiki.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 3
    assert tabs.getSelection() == 1

    assert tabs.getPage(0) == otherwiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"
    assert tabs.getPage(1) == otherwiki["Страница 2/Страница 3/Страница 4"]
    assert tabs.getPage(2) == otherwiki["Страница 2"]


def test_save_tabs_04(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The page selected after the tab selection is restored too."""
    tabs.openInTab(opened_wiki["Страница 2"], False)
    tabs.openInTab(opened_wiki["Страница 2/Страница 3/Страница 4"], False)
    tabs.setSelection(1)
    application.selectedPage = opened_wiki["Страница 2/Страница 3"]

    application.wikiroot = None
    assert tabs.getTabsCount() == 0

    otherwiki = loadNotesTree(opened_wiki.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 3
    assert tabs.getSelection() == 1

    assert tabs.getPage(0) == otherwiki["Страница 1"]
    assert tabs.getTabTitle(0) == "Страница 1"
    assert tabs.getPage(1) == otherwiki["Страница 2/Страница 3"]
    assert tabs.getPage(2) == otherwiki["Страница 2"]


def test_save_tabs_05(
    tabs: TabsController, application: Application, wikiroot: WikiDocument
) -> None:
    """The tabs are saved after each change and not on the wiki closing."""
    wiki = loadNotesTree(wikiroot.path)
    application.wikiroot = wiki

    application.selectedPage = wiki["Страница 1"]
    tabs.cloneTab()
    tabs.openInTab(wiki["Страница 2"], True)
    assert tabs.getTabsCount() == 3

    # Load the wiki once more to check that the tabs state has not been changed
    otherwiki = loadNotesTree(wikiroot.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 3
    assert application.selectedPage == otherwiki["Страница 2"]


def test_save_after_remove(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The tabs of the removed page are not saved."""
    tabs.cloneTab()
    tabs.openInTab(opened_wiki["Страница 2"], True)
    tabs.cloneTab()
    tabs.cloneTab()
    tabs.cloneTab()

    opened_wiki["Страница 1"].remove()

    otherwiki = loadNotesTree(opened_wiki.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 4
    assert tabs.getSelection() == 3
    assert tabs.getPage(0) == otherwiki["Страница 2"]
    assert tabs.getPage(3) == otherwiki["Страница 2"]


def test_save_after_move(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The tabs follow the moved page."""
    tabs.cloneTab()
    tabs.openInTab(opened_wiki["Страница 2"], True)

    opened_wiki["Страница 1"].moveTo(opened_wiki["Страница 2"])

    otherwiki = loadNotesTree(opened_wiki.path)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 3
    assert tabs.getPage(0) == otherwiki["Страница 2/Страница 1"]
    assert tabs.getPage(1) == otherwiki["Страница 2/Страница 1"]
    assert tabs.getPage(2) == otherwiki["Страница 2"]


def test_move(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The tabs follow the moved page without reloading the wiki."""
    tabs.cloneTab()
    tabs.openInTab(opened_wiki["Страница 2"], True)
    tabs.setSelection(2)

    opened_wiki["Страница 1"].moveTo(opened_wiki["Страница 2"])

    assert opened_wiki["Страница 2/Страница 1"] == tabs.getPage(0)
    assert opened_wiki["Страница 2/Страница 1"] == tabs.getPage(1)

    tabs.setSelection(0)
    assert application.selectedPage == opened_wiki["Страница 2/Страница 1"]


def test_readonly(
    tabs: TabsController, application: Application, wikiroot: WikiDocument
) -> None:
    """The tabs state of the read only wiki is not changed."""
    wikiReadOnly = loadNotesTree(wikiroot.path, readonly=True)
    application.wikiroot = wikiReadOnly

    application.selectedPage = wikiReadOnly["Страница 1"]
    tabs.cloneTab()
    tabs.openInTab(wikiReadOnly["Страница 2"], True)
    assert tabs.getTabsCount() == 3

    # Load the wiki once more to check that the tabs state has not been changed
    otherwiki = loadNotesTree(wikiroot.path, readonly=True)
    application.wikiroot = otherwiki

    assert tabs.getTabsCount() == 1
    assert application.selectedPage is None


def test_close_last_tab(
    tabs: TabsController, application: Application, wikiroot: WikiDocument
) -> None:
    """The only tab can be closed."""
    application.wikiroot = wikiroot
    assert tabs.getTabsCount() == 1

    tabs.closeTab(0)

    assert tabs.getTabsCount() == 0


def test_close_tab_01(
    tabs: TabsController,
    application: Application,
    opened_wiki: WikiDocument,
    three_tabs,
) -> None:
    """The selected page is not changed when a not selected tab is closed."""
    assert tabs.getTabsCount() == 3
    assert application.selectedPage == opened_wiki["Страница 2/Страница 3"]

    tabs.closeTab(0)
    assert tabs.getTabsCount() == 2
    assert tabs.getPage(0) == opened_wiki["Страница 2"]
    assert tabs.getPage(1) == opened_wiki["Страница 2/Страница 3"]
    assert application.selectedPage == opened_wiki["Страница 2/Страница 3"]

    tabs.closeTab(0)
    assert tabs.getTabsCount() == 1
    assert tabs.getPage(0) == opened_wiki["Страница 2/Страница 3"]
    assert application.selectedPage == opened_wiki["Страница 2/Страница 3"]


def test_close_tab_02(
    tabs: TabsController,
    application: Application,
    opened_wiki: WikiDocument,
    three_tabs,
) -> None:
    """The previous tab becomes selected when the selected tab is closed."""
    assert tabs.getTabsCount() == 3

    tabs.closeTab(2)

    assert tabs.getTabsCount() == 2
    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert tabs.getPage(1) == opened_wiki["Страница 2"]
    assert application.selectedPage == opened_wiki["Страница 2"]

    tabs.closeTab(1)

    assert tabs.getTabsCount() == 1
    assert tabs.getPage(0) == opened_wiki["Страница 1"]
    assert application.selectedPage == opened_wiki["Страница 1"]


def test_close_last_tab_and_select_page(
    tabs: TabsController, application: Application, wikiroot: WikiDocument
) -> None:
    """A new tab is created when a page is selected after closing all the tabs."""
    application.wikiroot = wikiroot
    assert tabs.getTabsCount() == 1

    tabs.closeTab(0)
    assert tabs.getTabsCount() == 0

    application.selectedPage = wikiroot["Страница 1"]
    assert tabs.getTabsCount() == 1


def test_next_tab_01(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The next tab is selected while the last one is not reached."""
    tabs.openInTab(opened_wiki["Страница 2/Страница 3"], False)
    tabs.openInTab(opened_wiki["Страница 2"], False)

    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0

    tabs.nextTab()
    assert application.selectedPage == opened_wiki["Страница 2"]
    assert tabs.getSelection() == 1

    tabs.nextTab()
    assert application.selectedPage == opened_wiki["Страница 2/Страница 3"]
    assert tabs.getSelection() == 2

    tabs.nextTab()
    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0


def test_next_tab_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The only tab stays selected after switching to the next tab."""
    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0

    tabs.nextTab()

    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0


def test_prev_tab_01(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The previous tab is selected while the first one is not reached."""
    tabs.openInTab(opened_wiki["Страница 2/Страница 3"], False)
    tabs.openInTab(opened_wiki["Страница 2"], False)

    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0

    tabs.previousTab()
    assert application.selectedPage == opened_wiki["Страница 2/Страница 3"]
    assert tabs.getSelection() == 2

    tabs.previousTab()
    assert application.selectedPage == opened_wiki["Страница 2"]
    assert tabs.getSelection() == 1

    tabs.previousTab()
    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0


def test_prev_tab_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The only tab stays selected after switching to the previous tab."""
    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0

    tabs.previousTab()

    assert application.selectedPage == opened_wiki["Страница 1"]
    assert tabs.getSelection() == 0


@pytest.mark.parametrize(
    "method_name",
    [
        pytest.param("closeTab", id="close_tab"),
        pytest.param("getTabTitle", id="get_tab_title"),
        pytest.param("setSelection", id="set_selection"),
        pytest.param("getPage", id="get_page"),
    ],
)
@pytest.mark.parametrize(
    "index",
    [
        pytest.param(-1, id="negative"),
        pytest.param(3, id="too_big"),
        pytest.param(5, id="much_too_big"),
    ],
)
def test_invalid_index(
    tabs: TabsController, three_tabs, method_name: str, index: int
) -> None:
    """ValueError is raised for the invalid tab index."""
    with pytest.raises(ValueError):
        getattr(tabs, method_name)(index)


def test_history_empty(application: Application, opened_wiki: WikiDocument) -> None:
    """There is no history when the first page is selected."""
    assert _get_history_state(application) == (False, False)


def test_history_goto(application: Application, opened_wiki: WikiDocument) -> None:
    """The back action is enabled after switching to another page."""
    application.selectedPage = opened_wiki["Страница 2"]

    assert _get_history_state(application) == (True, False)


def test_history_close_wiki(
    application: Application, opened_wiki: WikiDocument
) -> None:
    """The history is cleared when the wiki is reopened."""
    application.selectedPage = opened_wiki["Страница 2"]

    application.wikiroot = None
    application.wikiroot = opened_wiki

    assert _get_history_state(application) == (False, False)


def test_history_several_tabs_01(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """Each tab has its own history."""
    application.selectedPage = opened_wiki["Страница 2"]

    tabs.openInTab(opened_wiki["Страница 2"], True)
    assert _get_history_state(application) == (False, False)

    application.selectedPage = opened_wiki["Страница 1"]
    assert _get_history_state(application) == (True, False)


def test_history_several_tabs_02(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The history is kept in the tab when another page is opened in a new tab."""
    application.selectedPage = opened_wiki["Страница 2"]

    tabs.openInTab(opened_wiki["Страница 2"], True)
    tabs.setSelection(0)

    assert _get_history_state(application) == (True, False)


def test_history_several_tabs_03(
    tabs: TabsController, application: Application, opened_wiki: WikiDocument
) -> None:
    """The history of the current tab is not changed by a not selected new tab."""
    application.selectedPage = opened_wiki["Страница 2"]

    tabs.openInTab(opened_wiki["Страница 2"], False)

    assert _get_history_state(application) == (True, False)


def test_history_back_01(application: Application, opened_wiki: WikiDocument) -> None:
    """The back action returns to the previous page of the tab."""
    application.selectedPage = opened_wiki["Страница 2"]

    _run_history_action(application, HistoryBackAction)

    assert application.selectedPage == opened_wiki["Страница 1"]
    assert _get_history_state(application) == (False, True)


def test_history_back_02(application: Application, opened_wiki: WikiDocument) -> None:
    """The back and forward actions work with the pages and the empty state."""
    application.selectedPage = None

    _run_history_action(application, HistoryBackAction)
    assert application.selectedPage == opened_wiki["Страница 1"]
    assert _get_history_state(application) == (False, True)

    _run_history_action(application, HistoryForwardAction)
    assert _get_history_state(application) == (True, False)


def test_history_back_forward_01(
    application: Application, opened_wiki: WikiDocument
) -> None:
    """The history is walked back and forward through the nested pages."""
    application.selectedPage = opened_wiki["Страница 2"]
    application.selectedPage = opened_wiki["Страница 2/Страница 3"]
    application.selectedPage = opened_wiki["Страница 2/Страница 3/Страница 4"]
    application.selectedPage = None

    expected_back = [
        opened_wiki["Страница 2/Страница 3/Страница 4"],
        opened_wiki["Страница 2/Страница 3"],
        opened_wiki["Страница 2"],
        opened_wiki["Страница 1"],
    ]
    for expected_page in expected_back:
        _run_history_action(application, HistoryBackAction)
        assert application.selectedPage == expected_page

    assert _get_history_state(application) == (False, True)

    expected_forward = [
        opened_wiki["Страница 2"],
        opened_wiki["Страница 2/Страница 3"],
        opened_wiki["Страница 2/Страница 3/Страница 4"],
        None,
    ]
    for expected_page in expected_forward:
        _run_history_action(application, HistoryForwardAction)
        assert application.selectedPage == expected_page

    assert _get_history_state(application) == (True, False)


def test_history_back_forward_02(
    application: Application, opened_wiki: WikiDocument
) -> None:
    """The history is walked back and forward through the empty states."""
    application.selectedPage = opened_wiki["Страница 2"]
    application.selectedPage = None
    application.selectedPage = opened_wiki["Страница 2/Страница 3/Страница 4"]
    application.selectedPage = None

    expected_back = [
        opened_wiki["Страница 2/Страница 3/Страница 4"],
        None,
        opened_wiki["Страница 2"],
        opened_wiki["Страница 1"],
    ]
    for expected_page in expected_back:
        _run_history_action(application, HistoryBackAction)
        assert application.selectedPage == expected_page

    assert _get_history_state(application) == (False, True)

    expected_forward = [
        opened_wiki["Страница 2"],
        None,
        opened_wiki["Страница 2/Страница 3/Страница 4"],
        None,
    ]
    for expected_page in expected_forward:
        _run_history_action(application, HistoryForwardAction)
        assert application.selectedPage == expected_page

    assert _get_history_state(application) == (True, False)


@pytest.mark.parametrize(
    "selection, move, expected_order, expected_selection",
    [
        pytest.param(None, (0, 0), [0, 1, 2, 3, 4], 0, id="not_changed"),
        pytest.param(
            None, (0, 1), [1, 0, 2, 3, 4], 1, id="first_selected_to_neighboring"
        ),
        pytest.param(None, (0, 2), [1, 2, 0, 3, 4], 2, id="first_selected_02"),
        pytest.param(None, (0, 4), [1, 2, 3, 4, 0], 4, id="first_selected_to_last"),
        pytest.param(1, (1, 0), [1, 0, 2, 3, 4], 0, id="second_selected_to_first"),
        pytest.param(1, (1, 4), [0, 2, 3, 4, 1], 4, id="second_selected_to_last"),
        pytest.param(None, (1, 0), [1, 0, 2, 3, 4], 1, id="second_to_first"),
        pytest.param(None, (1, 4), [0, 2, 3, 4, 1], 0, id="second_to_last"),
        pytest.param(None, (4, 0), [4, 0, 1, 2, 3], 1, id="last_to_first"),
        pytest.param(4, (4, 0), [4, 0, 1, 2, 3], 0, id="last_selected_to_first"),
        pytest.param(4, (0, 4), [1, 2, 3, 4, 0], 3, id="first_to_last_selected_last"),
        pytest.param(2, (4, 2), [0, 1, 4, 2, 3], 3, id="last_to_before_selection_01"),
        pytest.param(2, (4, 0), [4, 0, 1, 2, 3], 3, id="last_to_before_selection_02"),
    ],
)
def test_move_tab(
    tabs: TabsController,
    five_tabs: list[WikiPage],
    selection: int | None,
    move: tuple[int, int],
    expected_order: list[int],
    expected_selection: int,
) -> None:
    """The selected page stays selected in the moved tab."""
    if selection is not None:
        tabs.setSelection(selection)

    tabs.movePage(*move)

    assert [tabs.getPage(index).subpath for index in range(5)] == [
        five_tabs[index].subpath for index in expected_order
    ]
    assert tabs.getSelection() == expected_selection
