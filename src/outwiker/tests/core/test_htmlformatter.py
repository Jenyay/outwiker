# -*- coding=utf-8 -*-

import pytest

from outwiker.core.htmlformatter import HtmlFormatter
from outwiker.gui.cssclasses import CSS_ERROR, CSS_IMAGE


def test_image_no_common_classes():
    content = 'image.png'
    formatter = HtmlFormatter()

    expected = f'<img class="{CSS_IMAGE}" src="{content}" />'
    assert formatter.image(content) == expected


def test_image_with_common_classes():
    content = 'image.png'
    classes = ['class-1', 'class-2']
    formatter = HtmlFormatter(classes)

    expected = f'<img class="class-1 class-2 {CSS_IMAGE}" src="{content}" />'
    assert formatter.image(content) == expected


def test_error_no_common_classes():
    content = 'bla-bla-bla'
    formatter = HtmlFormatter()

    expected = f'<div class="{CSS_ERROR}">{content}</div>'
    assert formatter.error(content) == expected


def test_error_with_common_classes():
    content = 'bla-bla-bla'
    classes = ['class-1', 'class-2']
    formatter = HtmlFormatter(classes)

    expected = f'<div class="class-1 class-2 {CSS_ERROR}">{content}</div>'
    assert formatter.error(content) == expected


def test_block_no_classes():
    content = 'bla-bla-bla'
    formatter = HtmlFormatter()

    expected = f'<div class="">{content}</div>'
    assert formatter.block(content) == expected


def test_block_with_common_classes():
    content = 'bla-bla-bla'
    common_classes = ['class-1', 'class-2']
    formatter = HtmlFormatter(common_classes)

    expected = f'<div class="class-1 class-2">{content}</div>'
    assert formatter.block(content) == expected


def test_block_with_common_classes_with_other_classes():
    content = 'bla-bla-bla'
    common_classes = ['class-1', 'class-2']
    other_classes = ['class-3', 'class-4']
    formatter = HtmlFormatter(common_classes)

    expected = f'<div class="class-1 class-2 class-3 class-4">{content}</div>'
    assert formatter.block(content, other_classes) == expected
