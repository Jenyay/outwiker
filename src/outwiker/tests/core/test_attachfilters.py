# -*- coding=utf-8 -*-

from pathlib import Path

import pytest

from outwiker.core.attachfilters import (getImagesOnlyFilter,
                                         getDirOnlyFilter,
                                         getHiddenFilter,
                                         andFilter,
                                         orFilter,
                                         notFilter,
                                         getImageRecursiveFilter)
from outwiker.core.attachment import Attachment
from outwiker.tests.fixtures import wikipage


@pytest.mark.parametrize('fname,expected',
                         [
                             ('image.png', True),
                             ('image.jpg', True),
                             ('image.jpeg', True),
                             ('image.gif', True),
                             ('image.webp', True),
                             ('image.bmp', True),
                             ('file.txt', False),
                         ])
def test_images_filter(wikipage, fname, expected):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    with open(Path(attach_dir, fname), 'w'):
        pass

    filter_func = getImagesOnlyFilter()
    assert filter_func(Path(attach_dir, fname)) == expected


def test_images_dir_filter(wikipage):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)
    dir_name = 'image.png'

    attach.createSubdir(dir_name)

    filter_func = getImagesOnlyFilter()
    assert not filter_func(Path(attach_dir, dir_name))


@pytest.mark.parametrize('fname,expected',
                         [
                             ('image.png', True),
                             ('image.jpg', True),
                             ('file.txt', False),
                             ('subdir_1', True),
                             ('subdir_1/image.png', True),
                             ('subdir_1/image.jpg', True),
                             ('subdir_1/file.txt', False),
                             ('subdir_1/subdir_2', True),
                             ('subdir_1/subdir_2/image.png', True),
                             ('subdir_1/subdir_2/image.jpg', True),
                             ('subdir_1/subdir_2/file.txt', False),
                         ])
def test_images_recursive_filter(wikipage, fname, expected):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    # Root attach dir
    for attach_fname in ['image.png', 'image.jpg', 'file.txt']:
        with open(Path(attach_dir, attach_fname), 'w'):
            pass

    # Subdir
    dir_name_1 = 'subdir_1'
    attach.createSubdir(dir_name_1)

    for attach_fname in ['image_1.png', 'image_1.jpg', 'file_1.txt']:
        with open(Path(attach_dir, dir_name_1, attach_fname), 'w'):
            pass

    # Sub-subdir
    dir_name_2 = Path('subdir_1', 'subdir_2')
    attach.createSubdir(dir_name_2)

    for attach_fname in ['image_1.png', 'image_1.jpg', 'file_1.txt']:
        with open(Path(attach_dir, dir_name_2, attach_fname), 'w'):
            pass

    filter_func = getImageRecursiveFilter()
    assert filter_func(Path(attach_dir, fname)) == expected


@pytest.mark.parametrize('directory',
                         [
                             Path('dir'),
                             Path('dir_1', 'dir_2'),
                         ])
def test_dir_only_filter_ok(wikipage, directory):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    attach.createSubdir(directory)

    filter_func = getDirOnlyFilter()
    assert filter_func(Path(attach_dir, directory))


def test_dir_only_filter_fail(wikipage):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    fname = 'file.txt'
    with open(Path(attach_dir, fname), 'w'):
        pass

    filter_func = getDirOnlyFilter()
    assert not filter_func(Path(attach_dir, fname))


def test_dir_hidden_filter_file(wikipage):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    fname = '__file.txt'
    with open(Path(attach_dir, fname), 'w'):
        pass

    filter_func = getHiddenFilter(wikipage)
    assert not filter_func(Path(attach_dir, fname))


def test_dir_hidden_filter_dir(wikipage):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    dirname = '__dir'
    attach.createSubdir(dirname)

    filter_func = getHiddenFilter(wikipage)
    assert filter_func(Path(attach_dir, dirname))


def test_dir_hidden_filter_subdir(wikipage):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    dirname = Path('subdir', '__dir')
    attach.createSubdir(dirname)

    filter_func = getHiddenFilter(wikipage)
    assert not filter_func(Path(attach_dir, dirname))


def test_dir_hidden_filter_dir_not_hidden(wikipage):
    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    dirname = 'dir'
    attach.createSubdir(dirname)

    filter_func = getHiddenFilter(wikipage)
    assert not filter_func(Path(attach_dir, dirname))


def test_not_filter():
    true_filter = lambda path: True
    false_filter = lambda path: False

    assert not notFilter(true_filter)(Path('xxx'))
    assert notFilter(false_filter)(Path('xxx'))


def test_and_filter():
    true_filter = lambda path: True
    false_filter = lambda path: False

    assert andFilter(true_filter, true_filter)(Path('xxx'))
    assert not andFilter(false_filter, true_filter)(Path('xxx'))
    assert not andFilter(true_filter, false_filter)(Path('xxx'))
    assert not andFilter(false_filter, false_filter)(Path('xxx'))


def test_or_filter():
    true_filter = lambda path: True
    false_filter = lambda path: False

    assert orFilter(true_filter, true_filter)(Path('xxx'))
    assert orFilter(false_filter, true_filter)(Path('xxx'))
    assert orFilter(true_filter, false_filter)(Path('xxx'))
    assert not orFilter(false_filter, false_filter)(Path('xxx'))

