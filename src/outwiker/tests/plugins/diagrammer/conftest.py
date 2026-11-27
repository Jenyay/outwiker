"""Fixtures for the Diagrammer plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture(scope="module")
def diagrammer_loader(
    ow_application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Diagrammer plugin loaded into the application with the main window.

    The plugin is loaded after the main window is created, so it registers
    its GUI actions and initializes the node shapes too.
    """
    return plugins_loader("plugins/diagrammer")
