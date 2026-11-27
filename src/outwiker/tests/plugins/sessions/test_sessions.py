# -*- coding: utf-8 -*-

"""Tests for the Sessions plugin."""

import os.path
from collections.abc import Iterator
from tempfile import mkdtemp

import pytest

from outwiker.api.core.tree import WikiDocument, createNotesTree, loadNotesTree
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.tests.utils import removeDir


@pytest.fixture
def tabs_controller(main_window):
    """Tabs controller of the main window."""
    return main_window.tabsController


@pytest.fixture(autouse=True)
def clear_sessions_config(application) -> Iterator[None]:
    """Configuration section with the saved sessions is empty for each test."""
    from sessions.sessionstorage import SessionStorage

    application.config.remove_section(SessionStorage.SECTION_NAME)

    yield

    application.config.remove_section(SessionStorage.SECTION_NAME)


@pytest.fixture
def wiki(application, ow_application) -> Iterator[WikiDocument]:
    """
    Wiki with the pages used by the tests, opened in the application.

    The main window is created before the wiki is opened.
    """
    path = mkdtemp(prefix="outwiker_sessions")
    root = createNotesTree(path)
    factory = TextPageFactory()
    factory.create(root, "Страница 1", [])
    factory.create(root, "Страница 2", [])
    factory.create(root["Страница 1"], "Страница 3", [])
    factory.create(root["Страница 1/Страница 3"], "Страница 4", [])

    application.wikiroot = root

    yield root

    application.wikiroot = None
    removeDir(path)


@pytest.fixture
def other_wiki_path() -> Iterator[str]:
    """Path to the second wiki used by the restore tests."""
    path = mkdtemp(prefix="Абырвалг абырвалг")
    root = createNotesTree(path)
    factory = TextPageFactory()
    factory.create(root, "Page 1", [])
    factory.create(root, "Page 2", [])

    yield path

    removeDir(path)


@pytest.fixture
def make_storage(sessions_loader: PluginsLoader, application):
    """Factory for the SessionStorage instances reloaded from the config."""
    from sessions.sessionstorage import SessionStorage

    return lambda: SessionStorage(application.config)


@pytest.fixture
def controller(sessions_loader: PluginsLoader, application):
    """Sessions controller working with the current application state."""
    from sessions.sessioncontroller import SessionController

    return SessionController(application)


def _get_page_link(page) -> str:
    """Link to the page that is stored in the sessions."""
    return "page://" + page.getUid(generate=True)


def test_plugin_load(sessions_loader: PluginsLoader):
    assert len(sessions_loader) == 1


def test_empty_sessions(make_storage):
    storage = make_storage()

    assert storage.getSessions() == {}


def test_session_single_tab(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]
    session_name = "Имя сессии"

    storage = make_storage()
    storage.save(controller.getCurrentSession(), session_name)

    sessions = storage.getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 1
    assert sessions[session_name].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name].currentTab == 0


def test_save_session_root(application, wiki, make_storage, controller):
    application.selectedPage = None
    session_name = "Имя сессии"

    make_storage().save(controller.getCurrentSession(), session_name)
    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 1
    assert sessions[session_name].pages[0] is None
    assert sessions[session_name].currentTab == 0


def test_save_session_01(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]
    session_name = "Имя сессии"

    make_storage().save(controller.getCurrentSession(), session_name)
    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 1
    assert sessions[session_name].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name].currentTab == 0


def test_save_session_02(application, wiki, tabs_controller, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], False)

    session_name = "Имя сессии"

    make_storage().save(controller.getCurrentSession(), session_name)
    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 2
    assert sessions[session_name].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name].pages[1] == _get_page_link(wiki["Страница 2"])
    assert sessions[session_name].currentTab == 0


def test_save_session_02_root(
    application, wiki, tabs_controller, make_storage, controller
):
    application.selectedPage = None
    tabs_controller.openInTab(wiki["Страница 2"], False)

    session_name = "Имя сессии"

    make_storage().save(controller.getCurrentSession(), session_name)
    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 2
    assert sessions[session_name].pages[0] is None
    assert sessions[session_name].pages[1] == _get_page_link(wiki["Страница 2"])
    assert sessions[session_name].currentTab == 0


def test_save_session_03(application, wiki, tabs_controller, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)

    session_name = "Имя сессии"

    make_storage().save(controller.getCurrentSession(), session_name)
    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 2
    assert sessions[session_name].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name].pages[1] == _get_page_link(wiki["Страница 2"])
    assert sessions[session_name].currentTab == 1


def test_save_session_04(application, wiki, tabs_controller, make_storage, controller):
    session_name1 = "Имя сессии 1"
    session_name2 = "Имя сессии 2"

    application.selectedPage = wiki["Страница 1"]

    # Save the session with one page
    make_storage().save(controller.getCurrentSession(), session_name1)

    # Save the session with two pages
    tabs_controller.openInTab(wiki["Страница 2"], True)
    make_storage().save(controller.getCurrentSession(), session_name2)

    sessions = make_storage().getSessions()

    assert len(sessions) == 2

    assert len(sessions[session_name1].pages) == 1
    assert sessions[session_name1].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name1].currentTab == 0

    assert len(sessions[session_name2].pages) == 2
    assert sessions[session_name2].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name2].pages[1] == _get_page_link(wiki["Страница 2"])
    assert sessions[session_name2].currentTab == 1


def test_save_session_05(application, wiki, tabs_controller, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)

    session_name = "Имя сессии"
    session = controller.getCurrentSession()

    # Save the same session twice with the same name
    make_storage().save(session, session_name)
    make_storage().save(session, session_name)

    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 2
    assert sessions[session_name].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions[session_name].pages[1] == _get_page_link(wiki["Страница 2"])
    assert sessions[session_name].currentTab == 1
    assert not sessions[session_name].readonly


def test_save_session_06(application, wiki, tabs_controller, make_storage, controller):
    uid1 = _get_page_link(wiki["Страница 1"])
    uid2 = _get_page_link(wiki["Страница 2"])

    readonly_wiki = loadNotesTree(wiki.path, True)
    application.wikiroot = readonly_wiki

    application.selectedPage = readonly_wiki["Страница 1"]
    tabs_controller.openInTab(readonly_wiki["Страница 2"], True)

    session_name = "Имя сессии"
    session = controller.getCurrentSession()

    # Save the same session twice with the same name
    make_storage().save(session, session_name)
    make_storage().save(session, session_name)

    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 2
    assert sessions[session_name].pages[0] == uid1
    assert sessions[session_name].pages[1] == uid2
    assert sessions[session_name].currentTab == 1
    assert sessions[session_name].readonly


def test_save_session_07(application, wiki, tabs_controller, make_storage, controller):
    # Create the UIDs and then check that they are read correctly in the
    # read-only mode
    _get_page_link(wiki["Страница 1"])
    _get_page_link(wiki["Страница 2"])

    readonly_wiki = loadNotesTree(wiki.path, True)
    application.wikiroot = readonly_wiki

    application.selectedPage = readonly_wiki["Страница 1"]
    tabs_controller.openInTab(readonly_wiki["Страница 2"], True)

    session_name = "Имя сессии"
    session = controller.getCurrentSession()

    # Save the same session twice with the same name
    storage = make_storage()

    storage.save(session, session_name)
    storage.save(session, session_name)

    sessions = make_storage().getSessions()

    assert len(sessions) == 1
    assert len(sessions[session_name].pages) == 2
    assert sessions[session_name].pages[0] == _get_page_link(
        readonly_wiki["Страница 1"]
    )
    assert sessions[session_name].pages[1] == _get_page_link(
        readonly_wiki["Страница 2"]
    )
    assert sessions[session_name].currentTab == 1
    assert sessions[session_name].readonly


def test_save_session_08(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    sessions = make_storage().getSessions()

    assert len(sessions) == 2

    assert len(sessions["session1"].pages) == 1
    assert sessions["session1"].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions["session1"].currentTab == 0

    assert len(sessions["session2"].pages) == 1
    assert sessions["session2"].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions["session2"].currentTab == 0


def test_save_session_09(application, wiki, tabs_controller, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")

    tabs_controller.openInTab(wiki["Страница 2"], True)
    storage.save(controller.getCurrentSession(), "session2")

    sessions = make_storage().getSessions()

    assert len(sessions) == 2

    assert len(sessions["session1"].pages) == 1
    assert sessions["session1"].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions["session1"].currentTab == 0

    assert len(sessions["session2"].pages) == 2
    assert sessions["session2"].pages[0] == _get_page_link(wiki["Страница 1"])
    assert sessions["session2"].pages[1] == _get_page_link(wiki["Страница 2"])
    assert sessions["session2"].currentTab == 1


def test_remove_session_01(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    assert len(make_storage().getSessions()) == 2

    # Remove a non-existent session. Nothing should happen
    storage.remove("session_invalid")

    assert len(make_storage().getSessions()) == 2


def test_remove_session_02(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    assert len(make_storage().getSessions()) == 2

    storage.remove("session1")

    other_storage = make_storage()
    sessions = other_storage.getSessions()
    assert len(sessions) == 1
    assert list(sessions.keys())[0] == "session2"

    sessions = storage.getSessions()
    assert len(sessions) == 1
    assert list(sessions.keys())[0] == "session2"


def test_rename_01(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    with pytest.raises(KeyError):
        storage.rename("invalid", "Абырвалг")


def test_rename_02(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")
    storage.rename("session1", "Абырвалг")

    sessions = make_storage().getSessions()
    assert len(sessions) == 2
    assert sorted(sessions.keys())[0] == "session2"
    assert sorted(sessions.keys())[1] == "Абырвалг"

    sessions = storage.getSessions()
    assert len(sessions) == 2
    assert sorted(sessions.keys())[0] == "session2"
    assert sorted(sessions.keys())[1] == "Абырвалг"


def test_rename_03(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")
    storage.rename("session1", "session1")

    sessions = make_storage().getSessions()
    assert len(sessions) == 2
    assert sorted(sessions.keys())[0] == "session1"
    assert sorted(sessions.keys())[1] == "session2"

    sessions = storage.getSessions()
    assert len(sessions) == 2
    assert sorted(sessions.keys())[0] == "session1"
    assert sorted(sessions.keys())[1] == "session2"


def test_rename_04(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    with pytest.raises(ValueError):
        storage.rename("session1", "session2")


def test_rename_05(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    with pytest.raises(ValueError):
        storage.rename("session1", "session2   ")


def test_rename_06(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    with pytest.raises(ValueError):
        storage.rename("session1", "")


def test_rename_07(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")

    with pytest.raises(ValueError):
        storage.rename("session1", "   ")


def test_rename_08(application, wiki, make_storage, controller):
    application.selectedPage = wiki["Страница 1"]

    storage = make_storage()

    storage.save(controller.getCurrentSession(), "session1")
    storage.save(controller.getCurrentSession(), "session2")
    storage.rename("session1", "Абырвалг   ")

    sessions = make_storage().getSessions()
    assert len(sessions) == 2
    assert sorted(sessions.keys())[0] == "session2"
    assert sorted(sessions.keys())[1] == "Абырвалг"

    sessions = storage.getSessions()
    assert len(sessions) == 2
    assert sorted(sessions.keys())[0] == "session2"
    assert sorted(sessions.keys())[1] == "Абырвалг"


def test_get_session_info_01(application, wiki, controller):
    application.selectedPage = wiki["Страница 1"]

    session = controller.getCurrentSession()

    assert os.path.realpath(session.path) == os.path.realpath(wiki.path)
    assert len(session.pages) == 1
    assert session.pages[0] == _get_page_link(wiki["Страница 1"])
    assert session.currentTab == 0


def test_get_session_info_02(application, wiki, tabs_controller, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], False)

    session = controller.getCurrentSession()

    assert os.path.realpath(session.path) == os.path.realpath(wiki.path)
    assert len(session.pages) == 2
    assert session.pages[0] == _get_page_link(wiki["Страница 1"])
    assert session.pages[1] == _get_page_link(wiki["Страница 2"])
    assert session.currentTab == 0


def test_get_session_info_03(application, wiki, tabs_controller, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)

    session = controller.getCurrentSession()

    assert os.path.realpath(session.path) == os.path.realpath(wiki.path)
    assert len(session.pages) == 2
    assert session.pages[0] == _get_page_link(wiki["Страница 1"])
    assert session.pages[1] == _get_page_link(wiki["Страница 2"])
    assert session.currentTab == 1


def test_invalid_session_01(application, controller):
    """There is no opened wiki."""
    application.wikiroot = None

    session = controller.getCurrentSession()

    assert session.path == ""
    assert len(session.pages) == 0
    assert session.currentTab == 0


def test_restore_01(application, wiki, tabs_controller, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)

    session = controller.getCurrentSession()

    uid1 = _get_page_link(wiki["Страница 1"])
    uid2 = _get_page_link(wiki["Страница 2"])

    application.wikiroot = None
    assert tabs_controller.getTabsCount() == 0

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert tabs_controller.getTabsCount() == 2
    assert tabs_controller.getSelection() == 1

    new_session = controller.getCurrentSession()
    assert new_session.pages[0] == uid1
    assert new_session.pages[1] == uid2


def test_restore_02(application, wiki, tabs_controller, controller):
    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)
    tabs_controller.openInTab(wiki["Страница 1/Страница 3/Страница 4"], True)
    tabs_controller.openInTab(wiki["Страница 1/Страница 3"], False)

    session = controller.getCurrentSession()

    uid1 = _get_page_link(wiki["Страница 1"])
    uid2 = _get_page_link(wiki["Страница 2"])
    uid3 = _get_page_link(wiki["Страница 1/Страница 3/Страница 4"])
    uid4 = _get_page_link(wiki["Страница 1/Страница 3"])

    application.wikiroot = None
    assert tabs_controller.getTabsCount() == 0

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert tabs_controller.getTabsCount() == 4
    assert tabs_controller.getSelection() == 2

    new_session = controller.getCurrentSession()
    assert new_session.pages[0] == uid1
    assert new_session.pages[1] == uid2
    assert new_session.pages[2] == uid3
    assert new_session.pages[3] == uid4

    assert tabs_controller.getPage(0).title == "Страница 1"
    assert tabs_controller.getPage(1).title == "Страница 2"
    assert tabs_controller.getPage(2).title == "Страница 4"
    assert tabs_controller.getPage(3).title == "Страница 3"


def test_restore_03(application, wiki, tabs_controller, controller):
    opened_wiki = loadNotesTree(wiki.path, readonly=False)
    application.wikiroot = opened_wiki
    application.selectedPage = opened_wiki["Страница 1"]

    tabs_controller.openInTab(opened_wiki["Страница 2"], True)
    tabs_controller.openInTab(opened_wiki["Страница 1/Страница 3/Страница 4"], True)
    tabs_controller.openInTab(opened_wiki["Страница 1/Страница 3"], False)

    session = controller.getCurrentSession()

    tabs_controller.closeTab(1)
    tabs_controller.closeTab(1)
    tabs_controller.closeTab(1)

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert not application.wikiroot.readonly

    assert tabs_controller.getTabsCount() == 4
    assert tabs_controller.getSelection() == 2

    assert tabs_controller.getPage(0).title == "Страница 1"
    assert tabs_controller.getPage(1).title == "Страница 2"
    assert tabs_controller.getPage(2).title == "Страница 4"
    assert tabs_controller.getPage(3).title == "Страница 3"


def test_restore_04(application, wiki, tabs_controller, other_wiki_path, controller):
    second_wiki = loadNotesTree(other_wiki_path, False)

    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)

    session = controller.getCurrentSession()

    uid1 = _get_page_link(wiki["Страница 1"])
    uid2 = _get_page_link(wiki["Страница 2"])

    application.wikiroot = second_wiki
    assert tabs_controller.getTabsCount() == 1

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert tabs_controller.getTabsCount() == 2
    assert tabs_controller.getSelection() == 1

    new_session = controller.getCurrentSession()
    assert new_session.pages[0] == uid1
    assert new_session.pages[1] == uid2


def test_restore_05(application, wiki, tabs_controller, other_wiki_path, controller):
    second_wiki = loadNotesTree(other_wiki_path, True)

    application.selectedPage = wiki["Страница 1"]
    tabs_controller.openInTab(wiki["Страница 2"], True)

    session = controller.getCurrentSession()

    uid1 = _get_page_link(wiki["Страница 1"])
    uid2 = _get_page_link(wiki["Страница 2"])

    application.wikiroot = second_wiki
    assert tabs_controller.getTabsCount() == 1

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert tabs_controller.getTabsCount() == 2
    assert tabs_controller.getSelection() == 1

    new_session = controller.getCurrentSession()
    assert new_session.pages[0] == uid1
    assert new_session.pages[1] == uid2


def test_restore_readonly_01(application, wiki, tabs_controller, controller):
    readonly_wiki = loadNotesTree(wiki.path, readonly=True)
    application.wikiroot = readonly_wiki
    application.selectedPage = readonly_wiki["Страница 1"]

    tabs_controller.openInTab(readonly_wiki["Страница 2"], True)
    tabs_controller.openInTab(
        readonly_wiki["Страница 1/Страница 3/Страница 4"], True
    )
    tabs_controller.openInTab(readonly_wiki["Страница 1/Страница 3"], False)

    session = controller.getCurrentSession()

    application.wikiroot = None
    assert tabs_controller.getTabsCount() == 0

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert application.wikiroot.readonly

    assert tabs_controller.getTabsCount() == 4
    assert tabs_controller.getSelection() == 2

    assert tabs_controller.getPage(0).title == "Страница 1"
    assert tabs_controller.getPage(1).title == "Страница 2"
    assert tabs_controller.getPage(2).title == "Страница 4"
    assert tabs_controller.getPage(3).title == "Страница 3"


def test_restore_readonly_02(application, wiki, tabs_controller, controller):
    readonly_wiki = loadNotesTree(wiki.path, readonly=True)
    application.wikiroot = readonly_wiki
    application.selectedPage = readonly_wiki["Страница 1"]

    tabs_controller.openInTab(readonly_wiki["Страница 2"], True)
    tabs_controller.openInTab(
        readonly_wiki["Страница 1/Страница 3/Страница 4"], True
    )
    tabs_controller.openInTab(readonly_wiki["Страница 1/Страница 3"], False)

    session = controller.getCurrentSession()

    tabs_controller.closeTab(1)
    tabs_controller.closeTab(1)
    tabs_controller.closeTab(1)

    controller.restore(session)

    assert os.path.realpath(application.wikiroot.path) == os.path.realpath(wiki.path)
    assert application.wikiroot.readonly

    assert tabs_controller.getTabsCount() == 4
    assert tabs_controller.getSelection() == 2

    assert tabs_controller.getPage(0).title == "Страница 1"
    assert tabs_controller.getPage(1).title == "Страница 2"
    assert tabs_controller.getPage(2).title == "Страница 4"
    assert tabs_controller.getPage(3).title == "Страница 3"
