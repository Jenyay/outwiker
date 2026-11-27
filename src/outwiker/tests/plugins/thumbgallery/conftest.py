"""Fixtures for the Thumb Gallery plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture(scope="module")
def thumbgallery_loader(
    application: Application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Thumb Gallery plugin loaded into the application.

    The plugin does not create its GUI without the main window, so the
    application fixture is enough.
    """
    return plugins_loader("plugins/thumbgallery")
