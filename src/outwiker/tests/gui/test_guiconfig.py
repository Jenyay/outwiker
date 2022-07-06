# -*- coding=utf-8 -*-

import tempfile
from pathlib import Path

import pytest

from outwiker.core.config import Config
from outwiker.gui.guiconfig import GuiConfig
from outwiker.tests.utils import removeDir


@pytest.fixture
def config() -> Config:
    tempdir = tempfile.mkdtemp()
    path = Path(tempdir, "testconfig.ini")
    yield Config(path)
    removeDir(tempdir)


@pytest.fixture
def gui_config(config: Config) -> GuiConfig:
    yield GuiConfig(config)


def test_load_window_size_default(gui_config: GuiConfig):
    prefix = 'test'
    default_width = 10000
    default_height = 20000

    width, height = gui_config.loadWindowSize(
            prefix, default_width, default_height
    )

    assert width == default_width
    assert height == default_height


def test_save_size(gui_config: GuiConfig):
    prefix = 'test'
    default_width = 10000
    default_height = 20000

    new_width = 150
    new_height = 250

    gui_config.saveWindowSize(prefix, new_width, new_height)

    width, height = gui_config.loadWindowSize(
            prefix, default_width, default_height
    )

    assert width == new_width
    assert height == new_height


def test_default_width(gui_config: GuiConfig):
    prefix = 'test'
    default_width = 10000
    default_height = 20000

    new_width = 0
    new_height = 250

    gui_config.saveWindowSize(prefix, new_width, new_height)

    width, height = gui_config.loadWindowSize(
            prefix, default_width, default_height
    )

    assert width == default_width
    assert height == new_height


def test_default_height(gui_config: GuiConfig):
    prefix = 'test'
    default_width = 10000
    default_height = 20000

    new_width = 150
    new_height = 0

    gui_config.saveWindowSize(prefix, new_width, new_height)

    width, height = gui_config.loadWindowSize(
            prefix, default_width, default_height
    )

    assert width == new_width
    assert height == default_height
