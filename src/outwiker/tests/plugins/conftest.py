"""Common fixtures for the plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.app.owapplication import OutWikerApplication
from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


def _plugin_dir(request: pytest.FixtureRequest) -> str:
    """Directory of the plugin whose tests request the fixture."""
    return f"plugins/{request.node.path.parent.name}"


@pytest.fixture(scope="module")
def plugin_loader(
    request: pytest.FixtureRequest,
    application: Application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Plugin under test loaded into the application without the main window.

    The plugin directory is taken from the directory of the test module, so
    the tests do not need a conftest.py of their own. The plugins reacting to
    the wiki parser events and creating no wx objects while loading work
    without the main window; their GUI part is added when a page view is
    created.
    """
    return plugins_loader(_plugin_dir(request))


@pytest.fixture(scope="module")
def plugin_loader_gui(
    request: pytest.FixtureRequest,
    ow_application: OutWikerApplication,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Plugin under test loaded into the application with the main window.

    The main window is required by the plugins that create wx objects or
    register GUI actions while loading (the Sessions plugin creates a
    wx.Menu in its GUI creator, for example).
    """
    return plugins_loader(_plugin_dir(request))
