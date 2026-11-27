"""Fixtures for the Sessions plugin tests."""

from collections.abc import Callable

import pytest

from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture(scope="module")
def sessions_loader(
    ow_application,
    plugins_loader: Callable[..., PluginsLoader],
) -> PluginsLoader:
    """
    Sessions plugin loaded into the application with the main window.

    Unlike the other plugins, this one needs the main window to be loaded:
    it creates a ``wx.Menu`` while loading, which requires the ``wx.App``
    created together with the main window, and ``SessionController`` works
    only with the created tabs controller.
    """
    return plugins_loader("plugins/sessions")
