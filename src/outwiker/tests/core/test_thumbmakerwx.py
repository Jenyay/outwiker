# -*- coding: utf-8 -*-

"""
Tests for ThumbmakerWx
"""

import os

import pytest

from outwiker.core.thumbmakerwx import ThumbmakerWx
from outwiker.core.thumbexception import ThumbException
from outwiker.tests.utils import getImageSize

IMAGES_DIR = "testdata/images"


def test_wx_thumb_width_jpeg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.jpg")

    thumbmaker = ThumbmakerWx()
    newwidth = 250
    newheight = 182

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_width_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "outwiker_1.1.0_02.png")
    fname_out = str(tmp_path / "outwiker_1.1.0_02_th.png")

    thumbmaker = ThumbmakerWx()
    newwidth = 250
    newheight = 215

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_width_png_jpg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "outwiker_1.1.0_02.png")
    fname_out = str(tmp_path / "outwiker_1.1.0_02_th.jpeg")

    thumbmaker = ThumbmakerWx()
    newwidth = 250
    newheight = 215

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_width_tiff(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "outwiker_1.1.0_02.tiff")
    fname_out = str(tmp_path / "outwiker_1.1.0_02_th.png")

    thumbmaker = ThumbmakerWx()
    newwidth = 250
    newheight = 215

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_height_jpeg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.jpg")

    thumbmaker = ThumbmakerWx()
    newheight = 180
    newwidth = 246

    thumbmaker.thumbByHeight(fname_in, newheight, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_height_jpeg_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.png")

    thumbmaker = ThumbmakerWx()
    newheight = 180
    newwidth = 246

    thumbmaker.thumbByHeight(fname_in, newheight, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_jpeg_1(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.jpg")

    thumbmaker = ThumbmakerWx()
    newsize = 250

    newwidth = 250
    newheight = 182

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_jpeg_2(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first_vertical.jpeg")
    fname_out = str(tmp_path / "first_vertical_th.jpg")

    thumbmaker = ThumbmakerWx()
    newsize = 250

    newwidth = 182
    newheight = 250

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_raises(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first_vertical_error.jpeg")
    fname_out = str(tmp_path / "first_vertical_error_th.jpg")
    newsize = 250

    thumbmaker = ThumbmakerWx()

    with pytest.raises(ThumbException):
        thumbmaker.thumbByWidth(fname_in, newsize, fname_out)

    with pytest.raises(ThumbException):
        thumbmaker.thumbByHeight(fname_in, newsize, fname_out)

    with pytest.raises(ThumbException):
        thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out)
