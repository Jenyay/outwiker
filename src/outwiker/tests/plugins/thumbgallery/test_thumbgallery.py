# -*- coding: utf-8 -*-

"""Tests for the (:thumbgallery:) wiki command of the Thumb Gallery plugin."""

import os.path
from pathlib import Path

import pytest

from outwiker.core.attachment import Attachment
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.parser.wikiparser import Parser
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.api.core.tree import WikiPage


@pytest.fixture
def test_page(wikiroot) -> WikiPage:
    """Wiki page with the attachments used by the tests."""
    return WikiPageFactory().create(wikiroot, "Страница 1", [])


@pytest.fixture
def parser(
    test_page: WikiPage,
    application,
    thumbgallery_loader: PluginsLoader,
) -> Parser:
    """Wiki parser with the commands added by the Thumb Gallery plugin."""
    factory = ParserFactory()
    return factory.make(test_page, application)


def test_plugin_load(thumbgallery_loader: PluginsLoader):
    assert len(thumbgallery_loader) == 1


def test_content_parse_empty(parser):
    text = """Бла-бла-бла (:thumbgallery:) бла-бла-бла"""

    validResult = """Бла-бла-бла <div class="thumbgallery"></div> бла-бла-бла"""

    result = parser.toHtml(text)
    assert validResult == result
    assert "<table" not in result


def test_attach_full1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
    бла-бла-бла"""

    files = ["first.jpg"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert os.path.exists(os.path.join(test_page.path, "__attach", "__thumb"))
    assert "<table" not in result


def test_attach_thumbgallery_full2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_full2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_empty1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' not in result
    assert "__thumb" not in result
    assert "_first.jpg" not in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_empty1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' not in result
    assert "__thumb" not in result
    assert "_first.jpg" not in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        first.jpg
        particle_01.PNG
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:first.jpg
        Attach:particle_01.PNG
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_list2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:first.jpg
        Attach:particle_01.PNG
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list3(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)

        Attach:first.jpg


        Attach:particle_01.PNG


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery3(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)

        Attach:first.jpg


        Attach:particle_01.PNG


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list4_single_quotes(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:'first.jpg'
        Attach:'particle_01.PNG'
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery4_single_quotes(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:'first.jpg'
        Attach:'particle_01.PNG'
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list5_double_quotes(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:"first.jpg"
        Attach:"particle_01.PNG"
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery5_double_quotes(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:"first.jpg"
        Attach:"particle_01.PNG"
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_spaces1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)

        Attach:first.jpg


        Attach:картинка с пробелами.png


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
        "картинка с пробелами.png",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert "картинка с пробелами.png" in result
    assert "_картинка с пробелами.png" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_spaces2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)

        Attach:first.jpg


        картинка с пробелами.png


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
        "картинка с пробелами.png",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert "картинка с пробелами.png" in result
    assert "_картинка с пробелами.png" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_size1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery maxsize=100:)

        Attach:first.jpg


        Attach:particle_01.PNG
        Attach:картинка с пробелами.png

    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
        "картинка с пробелами.png",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "maxsize_100_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "maxsize_100_particle_01.PNG" in result

    assert "картинка с пробелами.png" in result
    assert "maxsize_100_картинка с пробелами.png" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "maxsize_100_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_gallery_size2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery px=100:)

        Attach:first.jpg


        Attach:particle_01.PNG


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "maxsize_100_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "maxsize_100_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "maxsize_100_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list_size1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery maxsize=100:)

        Attach:first.jpg


        Attach:particle_01.PNG


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "maxsize_100_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "maxsize_100_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "maxsize_100_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list_size2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery px=100:)

        Attach:first.jpg


        Attach:particle_01.PNG


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "maxsize_100_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "maxsize_100_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "maxsize_100_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list_comments1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery px=100:)

        Attach:first.jpg    | Первый


        Attach:particle_01.PNG|Комментарий к картинке


    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "maxsize_100_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "maxsize_100_particle_01.PNG" in result

    assert '<a href="__attach/image_01.JPG">' not in result
    assert "maxsize_100_image_01.JPG" not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list_comments2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:first.jpg    | Первый
        Attach:particle_01.PNG|Комментарий к картинке
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert '<a href="__attach/image_01.JPG">' not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list_comments3_single_quotes(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:'first.jpg'    | Первый
        Attach:'particle_01.PNG'|Комментарий к картинке
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert '<a href="__attach/image_01.JPG">' not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_attach_list_comments3_double_quotes(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:"first.jpg"    | Первый
        Attach:"particle_01.PNG"|Комментарий к картинке
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert '<a href="__attach/image_01.JPG">' not in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_table1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery cols=2:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert '<a href="__attach/image_01.JPG">' in result

    assert "html.txt" not in result

    assert "<table" in result

    # В таблице две строки
    assert len(result.split("<tr")) == 2 + 1


def test_table2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery cols=1:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "image_01.JPG",
        "particle_01.PNG",
        "image.png",
        "html.txt",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert '<a href="__attach/image_01.JPG">' in result

    assert "html.txt" not in result

    assert "<table" in result

    # В таблице две строки
    assert len(result.split("<tr")) == 4 + 1


def test_invalid_cols1(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery cols:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_invalid_cols2(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery cols=:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_invalid_cols3(test_page, parser, samplefiles_path):
    text = """Бла-бла-бла
    (:thumbgallery cols=abyrvalg:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result

    assert "html.txt" not in result
    assert "<table" not in result


def test_invalid_thumb_size_stream(test_page, parser, samplefiles_path):
    text = """Абырвалг
    (:thumbgallery px=abyrvalg:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)
    assert "бла-бла-бла" in result

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result


def test_invalid_thumb_size_table(test_page, parser, samplefiles_path):
    text = """Абырвалг
    (:thumbgallery px=abyrvalg сщды=3:)
    бла-бла-бла"""

    files = ["first.jpg", "image_01.JPG", "html.txt"]
    fullpath = [samplefiles_path / fname for fname in files]
    Attachment(test_page).attach(fullpath)

    result = parser.toHtml(text)
    assert "бла-бла-бла" in result

    assert '<a href="__attach/first.jpg">' in result
    assert "__thumb" in result
    assert "_first.jpg" in result

    assert '<a href="__attach/image_01.JPG">' in result
    assert "_image_01.JPG" in result


def test_subdir_forwardslash(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        subdir/first.jpg
        subdir/particle_01.PNG
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_forwardslash_comment(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        subdir/first.jpg | Comment
        subdir/particle_01.PNG | Comment
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_backslash(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        subdir\\first.jpg
        subdir\\particle_01.PNG
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_attach_backslash_single_quotes(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:'subdir\\first.jpg'
        Attach:'subdir\\particle_01.PNG'
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_attach_backslash_double_quotes(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:"subdir\\first.jpg"
        Attach:"subdir\\particle_01.PNG"
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_attach_forwardslash_single_quotes_comment(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:'subdir/first.jpg' | Comment
        Attach:'subdir/particle_01.PNG' | Comment
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_attach_forwardslash_single_quotes(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:'subdir/first.jpg'
        Attach:'subdir/particle_01.PNG'
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_attach_forwardslash_double_quotes(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:"subdir/first.jpg"
        Attach:"subdir/particle_01.PNG"
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_subdir_attach_forwardslash_double_quotes_comments(test_page, parser, samplefiles_path):
    subdir = "subdir"

    text = """Бла-бла-бла
    (:thumbgallery:)
        Attach:"subdir/first.jpg" | Comment
        Attach:"subdir/particle_01.PNG" | Comment
    (:thumbgalleryend:)
    бла-бла-бла"""

    files = [
        "first.jpg",
        "particle_01.PNG",
    ]
    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir)

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/subdir/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert Path(attach.getAttachPath(), "__thumb", subdir).exists()


def test_mask_all_root_single_star(test_page, parser, samplefiles_path):
    files = [
        "first.jpg",
        "particle_01.PNG",
        "filename.tmp",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        *
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert "filename.tmp" not in result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_all_root_single_star_attach(test_page, parser, samplefiles_path):
    files = [
        "first.jpg",
        "particle_01.PNG",
        "filename.tmp",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:*
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert "filename.tmp" not in result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_all_root_single_star_attach_single_quotes(test_page, parser, samplefiles_path):
    files = [
        "first.jpg",
        "particle_01.PNG",
        "filename.tmp",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:'*'
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert "filename.tmp" not in result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_all_root_single_star_attach_double_quotes(test_page, parser, samplefiles_path):
    files = [
        "first.jpg",
        "particle_01.PNG",
        "filename.tmp",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:"*"
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert "filename.tmp" not in result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_all_root_double_star(test_page, parser, samplefiles_path):
    files = [
        "first.jpg",
        "particle_01.PNG",
        "filename.tmp",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        *.*
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert "filename.tmp" not in result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_all_root_double_star_attach(test_page, parser, samplefiles_path):
    files = [
        "first.jpg",
        "particle_01.PNG",
        "filename.tmp",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:*.*
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/first.jpg">' in result, result
    assert "_first.jpg" in result
    assert "__thumb" in result

    assert '<a href="__attach/particle_01.PNG">' in result
    assert "_particle_01.PNG" in result

    assert "filename.tmp" not in result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_root(test_page, parser, samplefiles_path):
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        *.png
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/image.png">' in result, result
    assert '<a href="__attach/image_1.png">' in result, result
    assert '<a href="__attach/image_2.png">' in result, result
    assert '<a href="__attach/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_root_attach(test_page, parser, samplefiles_path):
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:*.png
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/image.png">' in result, result
    assert '<a href="__attach/image_1.png">' in result, result
    assert '<a href="__attach/image_2.png">' in result, result
    assert '<a href="__attach/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_root_attach_single_quotes(test_page, parser, samplefiles_path):
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:'*.png'
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/image.png">' in result, result
    assert '<a href="__attach/image_1.png">' in result, result
    assert '<a href="__attach/image_2.png">' in result, result
    assert '<a href="__attach/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_root_attach_double_quotes(test_page, parser, samplefiles_path):
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        Attach:"*.png"
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/image.png">' in result, result
    assert '<a href="__attach/image_1.png">' in result, result
    assert '<a href="__attach/image_2.png">' in result, result
    assert '<a href="__attach/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subdir(test_page, parser, samplefiles_path):
    subdir = "subdir"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery:)
        subdir/*.png
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/image.png">' in result, result
    assert '<a href="__attach/subdir/image_1.png">' in result, result
    assert '<a href="__attach/subdir/image_2.png">' in result, result
    assert '<a href="__attach/subdir/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subdir_attach(test_page, parser, samplefiles_path):
    subdir = "subdir"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery:)
        Attach:"subdir/*.png"
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/image.png">' in result, result
    assert '<a href="__attach/subdir/image_1.png">' in result, result
    assert '<a href="__attach/subdir/image_2.png">' in result, result
    assert '<a href="__attach/subdir/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subdir_all(test_page, parser, samplefiles_path):
    subdir = "subdir"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery:)
        subdir/*
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/image.png">' in result, result
    assert '<a href="__attach/subdir/image_1.png">' in result, result
    assert '<a href="__attach/subdir/image_2.png">' in result, result
    assert '<a href="__attach/subdir/image.jpg">' in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subdir_all_attach(test_page, parser, samplefiles_path):
    subdir = "subdir"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery:)
        Attach:"subdir/*"
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/image.png">' in result, result
    assert '<a href="__attach/subdir/image_1.png">' in result, result
    assert '<a href="__attach/subdir/image_2.png">' in result, result
    assert '<a href="__attach/subdir/image.jpg">' in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subsubdir(test_page, parser, samplefiles_path):
    subdir = "subdir1/subdir2/"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery:)
        **/*.png
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir1/subdir2/image.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image_1.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image_2.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subsubdir_attach(test_page, parser, samplefiles_path):
    subdir = "subdir1/subdir2/"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery:)
        Attach:"**/*.png"
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir1/subdir2/image.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image_1.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image_2.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image.jpg">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_subsubdir_skip_hidden_dirs(test_page, parser, samplefiles_path):
    subdir = "subdir1/subdir2/"
    subdir_hidden = "__hidden"

    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]
    fullpath = [samplefiles_path / fname for fname in files]

    files_hidden = ["add.png"]
    fullpath_hidden = [samplefiles_path / fname for fname in files_hidden]

    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.createSubdir(subdir_hidden)

    attach.attach(fullpath, subdir=subdir)
    attach.attach(fullpath_hidden, subdir=subdir_hidden)

    text = """
    (:thumbgallery:)
        **/*
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir1/subdir2/image.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image_1.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image_2.png">' in result, result
    assert '<a href="__attach/subdir1/subdir2/image.jpg">' in result, result
    assert '<a href="__attach/__hidden/add.png">' not in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()
    assert Path(attach.getAttachPath(), "__hidden").exists()
    assert Path(attach.getAttachPath(), subdir_hidden, files_hidden[0]).exists()


def test_not_hidden_files(test_page, parser, samplefiles_path):
    files = [
        "__image.png",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.attach(fullpath)
    text = """
    (:thumbgallery:)
        *
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/__image.png">' in result, result

    assert Path(attach.getAttachPath(), "__thumb").exists()


def test_mask_with_comments(test_page, parser, samplefiles_path):
    subdir = "subdir"
    files = [
        "image.png",
        "image_1.png",
        "image_2.png",
        "image.jpg",
    ]

    fullpath = [samplefiles_path / fname for fname in files]
    attach = Attachment(test_page)
    attach.createSubdir(subdir)
    attach.attach(fullpath, subdir=subdir)
    text = """
    (:thumbgallery cols=3:)
        Attach:"subdir/image_*.png" | Comment 1
        Attach:"subdir/*.jpg" | Comment 2
        Attach:"subdir/image.png" | Comment 3
    (:thumbgalleryend:)
    """

    result = parser.toHtml(text)

    assert '<a href="__attach/subdir/image.png">' in result, result
    assert '<a href="__attach/subdir/image_1.png">' in result, result
    assert '<a href="__attach/subdir/image_2.png">' in result, result
    assert '<a href="__attach/subdir/image.jpg">' in result, result

    assert (
        result.count('<div class="thumbgallery-table-comment">Comment 1</div>') == 2
    ), result
    assert (
        result.count('<div class="thumbgallery-table-comment">Comment 2</div>') == 1
    )
    assert (
        result.count('<div class="thumbgallery-table-comment">Comment 3</div>') == 1
    )

    assert Path(attach.getAttachPath(), "__thumb").exists()
