# -*- coding: utf-8 -*-

"""
Tests for ThumbmakerPil
"""

import os

import pytest

from outwiker.core.thumbmakerpil import ThumbmakerPil
from outwiker.core.thumbexception import ThumbException
from outwiker.tests.utils import getImageSize

IMAGES_DIR = "testdata/images"


def test_wx_thumb_width_jpeg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.jpg")

    thumbmaker = ThumbmakerPil()
    newwidth = 250
    newheight = 182

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_width_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "outwiker_1.1.0_02.png")
    fname_out = str(tmp_path / "outwiker_1.1.0_02_th.png")

    thumbmaker = ThumbmakerPil()
    newwidth = 250
    newheight = 215

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_width_png_jpg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "outwiker_1.1.0_02.png")
    fname_out = str(tmp_path / "outwiker_1.1.0_02_th.jpeg")

    thumbmaker = ThumbmakerPil()
    newwidth = 250
    newheight = 215

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_width_tiff(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "outwiker_1.1.0_02.tiff")
    fname_out = str(tmp_path / "outwiker_1.1.0_02_th.png")

    thumbmaker = ThumbmakerPil()
    newwidth = 250
    newheight = 215

    thumbmaker.thumbByWidth(fname_in, newwidth, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_height_jpeg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.jpg")

    thumbmaker = ThumbmakerPil()
    newheight = 180
    newwidth = 246

    thumbmaker.thumbByHeight(fname_in, newheight, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_height_jpeg_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.png")

    thumbmaker = ThumbmakerPil()
    newheight = 180
    newwidth = 246

    thumbmaker.thumbByHeight(fname_in, newheight, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_01_jpeg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first.jpg")
    fname_out = str(tmp_path / "first_th.jpg")

    thumbmaker = ThumbmakerPil()
    newsize = 250

    newwidth = 250
    newheight = 182

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_02_jpeg(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first_vertical.jpeg")
    fname_out = str(tmp_path / "first_vertical_th.jpg")

    thumbmaker = ThumbmakerPil()
    newsize = 250

    newwidth = 182
    newheight = 250

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_03_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "8x8.png")
    fname_out = str(tmp_path / "_thumb.png")

    thumbmaker = ThumbmakerPil()
    newsize = 16

    newwidth = 8
    newheight = 8

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out, larger=False)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_04_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "8x8.png")
    fname_out = str(tmp_path / "_thumb.png")

    thumbmaker = ThumbmakerPil()
    newsize = 16

    newwidth = 16
    newheight = 16

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out, larger=True)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_05_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "16x8.png")
    fname_out = str(tmp_path / "_thumb.png")

    thumbmaker = ThumbmakerPil()
    newsize = 16

    newwidth = 16
    newheight = 8

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out, larger=False)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_06_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "16x8.png")
    fname_out = str(tmp_path / "_thumb.png")

    thumbmaker = ThumbmakerPil()
    newsize = 16

    newwidth = 16
    newheight = 8

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out, larger=True)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_07_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "8x16.png")
    fname_out = str(tmp_path / "_thumb.png")

    thumbmaker = ThumbmakerPil()
    newsize = 16

    newwidth = 8
    newheight = 16

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out, larger=True)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_max_size_08_png(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "8x16.png")
    fname_out = str(tmp_path / "_thumb.png")

    thumbmaker = ThumbmakerPil()
    newsize = 16

    newwidth = 8
    newheight = 16

    thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out, larger=False)

    (width, height) = getImageSize(fname_out)

    assert width == newwidth
    assert height == newheight


def test_wx_thumb_raises(wxapp, tmp_path):
    fname_in = os.path.join(IMAGES_DIR, "first_vertical_error.jpeg")
    fname_out = str(tmp_path / "first_vertical_error_th.jpg")
    newsize = 250

    thumbmaker = ThumbmakerPil()

    with pytest.raises(ThumbException):
        thumbmaker.thumbByWidth(fname_in, newsize, fname_out)

    with pytest.raises(ThumbException):
        thumbmaker.thumbByHeight(fname_in, newsize, fname_out)

    with pytest.raises(ThumbException):
        thumbmaker.thumbByMaxSize(fname_in, newsize, fname_out)
