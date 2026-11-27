"""Fixtures for the Source plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture(scope="module")
def source_loader(
    ow_application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Source plugin loaded into the application with the main window.

    The plugin is loaded after the main window is created, so it registers
    its GUI actions too.
    """
    return plugins_loader("plugins/source")
