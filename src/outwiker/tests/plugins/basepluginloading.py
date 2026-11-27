"""Base class for the tests checking that a plugin is loaded and unloaded."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

from outwiker.api.core.tree import WikiDocument, createNotesTree
from outwiker.app.owapplication import OutWikerApplication
from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction
from outwiker.pages.html.htmlpage import HtmlPageFactory
from outwiker.pages.search.searchpage import SearchPageFactory
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory


class BasePluginLoadingTests(ABC):
    """
    Base class for the plugin loading tests.

    A subclass must return the plugin directory and the plugin name, for
    example:

        class TestDiagrammerLoading(BasePluginLoadingTests):
            def get_plugin_dir(self) -> str:
                return "plugins/diagrammer"

            def get_plugin_name(self) -> str:
                return "Diagrammer"
    """

    @abstractmethod
    def get_plugin_dir(self) -> str:
        """Return the path to the directory with the plugin sources."""

    @abstractmethod
    def get_plugin_name(self) -> str:
        """Return the plugin name as it is known to PluginsLoader."""

    def get_application_params(self) -> dict[str, Any]:
        """
        Return the parameters of the main window creation.

        The keys are the keyword arguments of the ow_application_factory
        fixture: enableActionsGui, createTreePanel, createAttachPanel,
        createTagsPanel and createBookmarksPanel.
        """
        return {}

    # The main window is extracted into a separate fixture so that it is not
    # created for every test by the loader fixture.
    @pytest.fixture(scope="module")
    def ow_application(self, ow_application_factory) -> OutWikerApplication:
        """Main window configured for the plugin under test."""
        return ow_application_factory(**self.get_application_params())

    @pytest.fixture
    def loader(self, ow_application: OutWikerApplication) -> Iterator[PluginsLoader]:
        """
        Loader with the tested plugin loaded.

        The plugin is loaded into the application with the created main
        window, as it happens in the real application. The wiki is detached
        from the application and the plugin is unloaded on teardown.
        """
        application = ow_application.application
        assert application is not None

        plugin_loader = PluginsLoader(application)
        plugin_loader.load([self.get_plugin_dir()])

        yield plugin_loader

        application.selectedPage = None
        application.wikiroot = None
        plugin_loader.clear()

    @pytest.fixture
    def plugin_wikiroot(self, tmp_path: Path) -> WikiDocument:
        """Wiki with the pages of different types opened in the destroy tests."""
        wikiroot = createNotesTree(tmp_path)

        WikiPageFactory().create(wikiroot, "Викистраница", [])
        TextPageFactory().create(wikiroot, "Текст", [])
        HtmlPageFactory().create(wikiroot, "HTML", [])
        SearchPageFactory().create(wikiroot, "Search", [])

        return wikiroot

    def test_plugin_loading(self, loader: PluginsLoader) -> None:
        """The only plugin from the directory is loaded."""
        assert len(loader) == 1
        assert loader[self.get_plugin_name()] is not None

    def test_destroy_without_wiki(
        self, application: Application, loader: PluginsLoader
    ) -> None:
        """The plugin is unloaded when no wiki is opened."""
        application.wikiroot = None
        loader.clear()

        assert len(loader) == 0

    @pytest.mark.parametrize(
        "page_name",
        [
            pytest.param(None, id="no_page"),
            pytest.param("Викистраница", id="wikipage"),
            pytest.param("Текст", id="textpage"),
            pytest.param("HTML", id="htmlpage"),
            pytest.param("Search", id="searchpage"),
        ],
    )
    def test_destroy_with_opened_wiki(
        self,
        application: Application,
        plugin_wikiroot: WikiDocument,
        loader: PluginsLoader,
        page_name: str | None,
    ) -> None:
        """The plugin is unloaded when a wiki is opened with a page selected."""
        application.wikiroot = plugin_wikiroot
        application.selectedPage = (
            plugin_wikiroot[page_name] if page_name is not None else None
        )

        loader.clear()

        assert len(loader) == 0

    @pytest.mark.parametrize(
        "page_name",
        [
            pytest.param("Викистраница", id="wikipage"),
            pytest.param("HTML", id="htmlpage"),
        ],
    )
    def test_switch_code_result_with_disabled_plugin(
        self,
        application: Application,
        plugin_wikiroot: WikiDocument,
        loader: PluginsLoader,
        page_name: str,
    ) -> None:
        """The page action works when the plugin is only disabled."""
        application.wikiroot = plugin_wikiroot
        application.selectedPage = plugin_wikiroot[page_name]
        loader.disable(self.get_plugin_name())

        self._run_switch_code_result(application)
        loader.clear()

        assert len(loader) == 0

    @pytest.mark.parametrize(
        "page_name",
        [
            pytest.param("Викистраница", id="wikipage"),
            pytest.param("HTML", id="htmlpage"),
        ],
    )
    def test_switch_code_result_with_unloaded_plugin(
        self,
        application: Application,
        plugin_wikiroot: WikiDocument,
        loader: PluginsLoader,
        page_name: str,
    ) -> None:
        """The page action works when the plugin is already unloaded."""
        application.wikiroot = plugin_wikiroot
        application.selectedPage = plugin_wikiroot[page_name]
        loader.clear()

        self._run_switch_code_result(application)

        assert len(loader) == 0

    def _run_switch_code_result(self, application: Application) -> None:
        """Run the action switching the code and the result of a page."""
        action = application.actionController.getAction(SwitchCodeResultAction.stringId)
        action.run(None)
