"""Fixtures for the Diagrammer plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture(scope="module")
def diagrammer_loader(
    application: Application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Diagrammer plugin loaded into the application without the main window.

    The plugin itself does not need the main window to be loaded: it
    initializes the node shapes and subscribes to the wiki parser events.
    The GUI part (actions, menu items and toolbar buttons) is skipped by the
    plugin when there is no main window, so the tests that need the dialogs
    request the main window through their own fixtures.
    """
    return plugins_loader("plugins/diagrammer")
