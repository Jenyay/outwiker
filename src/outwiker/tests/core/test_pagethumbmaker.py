# -*- coding: utf-8 -*-

"""
Tests for PageThumbmaker
"""

import os

import pytest

from outwiker.api.core.tree import createNotesTree
from outwiker.core.attachment import Attachment
from outwiker.pages.text.textpage import TextPageFactory
from outwiker.pages.wiki.parser.pagethumbmaker import PageThumbmaker
from outwiker.tests.utils import getImageSize

IMAGES_DIR = "testdata/images"


@pytest.fixture
def wikiroot(tmp_path):
    root = createNotesTree(tmp_path)

    factory = TextPageFactory()
    factory.create(root, "Страница 1", [])

    return root


def test_thumb_by_width_jpeg(wxapp, wikiroot):
    fname_in = "first.jpg"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    newwidth = 250
    newheight = 182

    thumb_fname = thumbmaker.createThumbByWidth(page, fname_in, newwidth)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight


def test_thumb_by_width_png(wxapp, wikiroot):
    fname_in = "outwiker_1.1.0_02.png"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    newwidth = 250
    newheight = 215

    thumb_fname = thumbmaker.createThumbByWidth(page, fname_in, newwidth)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight


def test_thumb_by_height_jpeg(wxapp, wikiroot):
    fname_in = "first.jpg"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    newwidth = 249
    newheight = 182

    thumb_fname = thumbmaker.createThumbByHeight(page, fname_in, newheight)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight


def test_thumb_by_height_png(wxapp, wikiroot):
    fname_in = "outwiker_1.1.0_02.png"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    newwidth = 249
    newheight = 215

    thumb_fname = thumbmaker.createThumbByHeight(page, fname_in, newheight)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight


def test_thumb_by_max_size_jpeg_1(wxapp, wikiroot):
    fname_in = "first.jpg"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    maxsize = 250

    newwidth = 250
    newheight = 182

    thumb_fname = thumbmaker.createThumbByMaxSize(page, fname_in, maxsize)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight


def test_thumb_by_max_size_jpeg_2(wxapp, wikiroot):
    fname_in = "first_vertical.jpeg"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    maxsize = 250

    newwidth = 182
    newheight = 250

    thumb_fname = thumbmaker.createThumbByMaxSize(page, fname_in, maxsize)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight


def test_thumb_by_max_size_png(wxapp, wikiroot):
    fname_in = "outwiker_1.1.0_02.png"
    page = wikiroot["Страница 1"]

    Attachment(page).attach([os.path.join(IMAGES_DIR, fname_in)])

    thumbmaker = PageThumbmaker()
    maxsize = 250

    newwidth = 250
    newheight = 215

    thumb_fname = thumbmaker.createThumbByMaxSize(page, fname_in, maxsize)
    thumb_path = os.path.join(page.path, thumb_fname)

    (width, height) = getImageSize(thumb_path)

    assert os.path.exists(thumb_path), thumb_path
    assert width == newwidth
    assert height == newheight
