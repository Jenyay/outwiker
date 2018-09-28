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
