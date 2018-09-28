# -*- coding: utf-8 -*-

import pytest

import outwiker.gui.controls.pagelist as pl


def test_createDefaultColumns_len():
    factory = pl.ColumnsFactory()
    default = factory.createDefaultColumns()
    assert len(default) == 4


def test_createColumn():
    factory = pl.ColumnsFactory()
    assert type(factory.createColumn('title')) == pl.PageTitleColumn
    assert type(factory.createColumn('parent')) == pl.ParentPageColumn
    assert type(factory.createColumn('tags')) == pl.TagsColumn
    assert type(factory.createColumn('moddate')) == pl.ModifyDateColumn


def test_createColumn_invalid_empty():
    factory = pl.ColumnsFactory()
    with pytest.raises(ValueError):
        factory.createColumn('')


def test_createColumn_invalid_name():
    factory = pl.ColumnsFactory()
    with pytest.raises(ValueError):
        factory.createColumn('invalid')


def test_createColumnsFromString_empty():
    text = ''
    factory = pl.ColumnsFactory()
    columns = factory.createColumnsFromString(text)

    assert len(columns) == 0


def test_createColumnsFromString_single_title():
    text = 'title:100:True'
    factory = pl.ColumnsFactory()
    columns = factory.createColumnsFromString(text)

    assert len(columns) == 1
    assert type(columns[0]) == pl.PageTitleColumn
    assert columns[0].width == 100
    assert columns[0].visible


def test_createColumnsFromString_single_parent():
    text = 'parent:200:False'
    factory = pl.ColumnsFactory()
    columns = factory.createColumnsFromString(text)

    assert len(columns) == 1
    assert type(columns[0]) == pl.ParentPageColumn
    assert columns[0].width == 200
    assert not columns[0].visible


def test_createColumnsFromString_single_tags():
    text = 'tags:300:True'
    factory = pl.ColumnsFactory()
    columns = factory.createColumnsFromString(text)

    assert len(columns) == 1
    assert type(columns[0]) == pl.TagsColumn
    assert columns[0].width == 300
    assert columns[0].visible


def test_createColumnsFromString_single_moddate():
    text = 'moddate:400:True'
    factory = pl.ColumnsFactory()
    columns = factory.createColumnsFromString(text)

    assert len(columns) == 1
    assert type(columns[0]) == pl.ModifyDateColumn
    assert columns[0].width == 400
    assert columns[0].visible


def test_createColumnsFromString_several():
    text = 'moddate:400:False,title:200:True'
    factory = pl.ColumnsFactory()
    columns = factory.createColumnsFromString(text)

    assert len(columns) == 2
    assert type(columns[0]) == pl.ModifyDateColumn
    assert type(columns[1]) == pl.PageTitleColumn
    assert columns[0].width == 400
    assert columns[1].width == 200
    assert not columns[0].visible
    assert columns[1].visible
