"""Fixtures for the Markdown plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture
def markdown_loader(
    application: Application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Markdown plugin loaded into the application.

    The editor fixture requests the main window before this loader, so the
    plugin is loaded after the main window is created.
    """
    return plugins_loader("plugins/markdown")
