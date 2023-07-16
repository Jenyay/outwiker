# -*- coding=utf-8 -*-

from outwiker.core.attachment import Attachment
from outwiker.tests.fixtures import wikipage
from outwiker.tests.utils import attach_files


def test_no_attaches_empty_query(wikipage):
    query = ''
    attach = Attachment(wikipage)
    result = attach.query(query)

    assert len(result) == 0


def test_empty_query(wikipage):
    files = ['image.png', 'add.png']
    query = ''
    attach_files(wikipage, files)

    attach = Attachment(wikipage)
    result = attach.query(query)

    assert len(result) == 0


def test_invalid_query_space(wikipage):
    files = ['image.png', 'add.png']
    query = '\n\t '
    attach_files(wikipage, files)

    attach = Attachment(wikipage)
    result = attach.query(query)

    assert len(result) == 0


def test_invalid_query_double_dots(wikipage):
    files = ['image.png', 'add.png']
    query = '../*.*'
    attach_files(wikipage, files)

    attach = Attachment(wikipage)
    result = attach.query(query)

    assert len(result) == 0


def test_invalid_query_root_slash(wikipage):
    files = ['image.png', 'add.png']
    query = '/*.*'
    attach_files(wikipage, files)

    attach = Attachment(wikipage)
    result = attach.query(query)

    assert len(result) == 0


def test_attach_not_exists(wikipage):
    query = '*.*'

    attach = Attachment(wikipage)
    result = attach.query(query)

    assert len(result) == 0


def test_select_all_root(wikipage):
    files = ['image.png', 'add.png']
    query = '*.*'
    attach_files(wikipage, files)
    expected = ['add.png', 'image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_all_root_single_star(wikipage):
    files = ['image.png', 'add.png']
    query = '*'
    attach_files(wikipage, files)
    expected = ['add.png', 'image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_by_extension(wikipage):
    files = ['image.png', 'add.png', 'image.jpg']
    query = '*.png'
    attach_files(wikipage, files)
    expected = ['add.png', 'image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_by_name(wikipage):
    files = ['image.png', 'add.png', 'image.jpg']
    query = 'image.*'
    attach_files(wikipage, files)
    expected = ['image.jpg', 'image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_by_name_with_question_marks(wikipage):
    files = ['image.png', 'add.png', 'image.jpg']
    query = 'ima??.*'
    attach_files(wikipage, files)
    expected = ['image.jpg', 'image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_by_name_with_star(wikipage):
    files = ['image.png', 'add.png', 'image.jpg']
    query = 'ima*.png'
    attach_files(wikipage, files)
    expected = ['image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_query_in_subdir(wikipage):
    subdir = 'subdir'
    files = ['image.png', 'add.png', 'image.jpg']
    query = 'subdir/*.png'
    attach_files(wikipage, files, subdir)
    expected = ['subdir/add.png', 'subdir/image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_all_in_subdir_single_star(wikipage):
    subdir = 'subdir'
    files = ['image.png', 'add.png', 'image.jpg']
    query = 'subdir/*'
    attach_files(wikipage, files, subdir)
    expected = ['subdir/add.png', 'subdir/image.jpg', 'subdir/image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_all_in_subdir_double_star(wikipage):
    subdir = 'subdir'
    files = ['image.png', 'add.png', 'image.jpg']
    query = 'subdir/*.*'
    attach_files(wikipage, files, subdir)
    expected = ['subdir/add.png', 'subdir/image.jpg', 'subdir/image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_all_with_subdir(wikipage):
    subdir = 'subdir/subdir2'
    files = ['image.png', 'add.png', 'image.jpg']
    query = '**/*.*'
    attach_files(wikipage, files, subdir)
    expected = ['subdir/subdir2/add.png',
                'subdir/subdir2/image.jpg',
                'subdir/subdir2/image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected


def test_select_mask_with_subdir(wikipage):
    subdir = 'subdir/subdir2'
    files = ['image.png', 'add.png', 'image.jpg']
    query = '**/*.png'
    attach_files(wikipage, files, subdir)
    expected = ['subdir/subdir2/add.png',
                'subdir/subdir2/image.png']

    attach = Attachment(wikipage)
    result = sorted(attach.query(query))

    assert result == expected
