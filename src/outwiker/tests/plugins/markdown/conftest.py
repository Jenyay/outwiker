"""Fixtures for the Markdown plug-in tests."""

from collections.abc import Iterator

import pytest

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader


@pytest.fixture(scope="module")
def markdown_plugin(application: Application) -> Iterator[PluginsLoader]:
    loader = PluginsLoader(application)
    loader.load(["plugins/markdown"])

    yield loader

    loader.clear()
