# -*- coding: utf-8 -*-

"""
Tests for IconsCollection
"""

import os

import pytest

from outwiker.gui.iconscollection import IconsCollection, DuplicateGroupError
from outwiker.tests.utils import getImageSize

IMAGES_DIR = "testdata/images"


def _get_max_image_size(fname):
    (width, height) = getImageSize(fname)
    return max(width, height)


def test_empty_01(wxapp):
    collection = IconsCollection("testdata/icons/Без иконок")

    assert collection.getIcons("") == []
    assert collection.getGroups() == []
    with pytest.raises(KeyError):
        collection.getIcons("Группа")
    with pytest.raises(KeyError):
        collection.getCover("Группа")
    assert collection.getCover(None) is None


def test_empty_02(wxapp):
    collection = IconsCollection("testdata/icons/Без иконок")

    assert collection.getIcons(None) == []
    assert collection.getGroups() == []
    with pytest.raises(KeyError):
        collection.getIcons("Группа")
    with pytest.raises(KeyError):
        collection.getCover("Группа")
    assert collection.getCover("") is None


def test_single_root(wxapp):
    collection = IconsCollection("testdata/icons/Без групп")

    assert len(collection.getIcons(None)) == 4
    assert collection.getGroups() == []
    assert collection.getCover(None).endswith("__cover.png")


def test_groups_01(wxapp):
    collection = IconsCollection("testdata/icons/Иконки и группы")

    assert len(collection.getIcons(None)) == 4
    assert collection.getGroups() == ["Группа 1", "Группа 2"]
    assert len(collection.getIcons("Группа 1")) == 3
    assert len(collection.getIcons("Группа 2")) == 4
    assert collection.getCover(None) is None
    assert collection.getCover("Группа 1").endswith("__cover.png")
    assert collection.getCover("Группа 2") is None


def test_groups_02(wxapp):
    collection = IconsCollection("testdata/icons/Только группы")

    assert len(collection.getIcons(None)) == 0
    assert collection.getGroups() == ["Группа 3", "Группа 4"]
    assert len(collection.getIcons("Группа 3")) == 3
    assert len(collection.getIcons("Группа 4")) == 4
    assert collection.getCover(None) is None


def test_add_group_01(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    assert collection.getGroups() == []

    collection.addGroup("Новая группа")
    assert collection.getGroups() == ["Новая группа"]

    newcollection1 = IconsCollection(str(tmp_path))
    assert newcollection1.getGroups() == ["Новая группа"]


def test_add_group_02_invalid(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))

    with pytest.raises(ValueError):
        collection.addGroup("Абырвалг\\Абырвалг")
    with pytest.raises(ValueError):
        collection.addGroup("Абырвалг/Абырвалг")
    with pytest.raises(ValueError):
        collection.addGroup("")


def test_add_group_03(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    assert collection.getGroups() == []

    collection.addGroup("Новая группа")
    collection.addGroup("Вторая группа")
    assert collection.getGroups() == ["Вторая группа", "Новая группа"]

    newcollection = IconsCollection(str(tmp_path))
    assert newcollection.getGroups() == ["Вторая группа", "Новая группа"]


def test_rename_group_01(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")
    assert collection.getGroups() == ["Новая группа"]

    collection.renameGroup("Новая группа", "Переименованная группа")
    assert collection.getGroups() == ["Переименованная группа"]

    newcollection1 = IconsCollection(str(tmp_path))
    assert newcollection1.getGroups() == ["Переименованная группа"]


def test_rename_group_02_invalid(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")

    with pytest.raises(ValueError):
        collection.renameGroup("Новая группа", "")
    with pytest.raises(ValueError):
        collection.renameGroup("Новая группа", "Абырвалг/Абырвалг")
    with pytest.raises(ValueError):
        collection.renameGroup("Новая группа", "Абырвалг\\Абырвалг")


def test_rename_group_03_self(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")

    collection.renameGroup("Новая группа", "Новая группа")
    assert collection.getGroups() == ["Новая группа"]

    newcollection = IconsCollection(str(tmp_path))
    assert newcollection.getGroups() == ["Новая группа"]


def test_rename_group_04_self(wxapp, tmp_path):
    files = ["new.png", "image_01.JPG"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")
    collection.addIcons("Новая группа", fullPaths)

    collection.renameGroup("Новая группа", "Новая группа")
    assert collection.getGroups() == ["Новая группа"]
    assert len(collection.getIcons("Новая группа")) == 2

    newcollection = IconsCollection(str(tmp_path))
    assert newcollection.getGroups() == ["Новая группа"]
    assert len(newcollection.getIcons("Новая группа")) == 2


def test_rename_group_04_invalid(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")
    collection.addGroup("Абырвалг")

    with pytest.raises(DuplicateGroupError):
        collection.renameGroup("Новая группа", "Абырвалг")


def test_remove_group_01(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")
    collection.addGroup("Другая группа")

    collection.removeGroup("Новая группа")
    assert collection.getGroups() == ["Другая группа"]

    newcollection1 = IconsCollection(str(tmp_path))
    assert newcollection1.getGroups() == ["Другая группа"]


def test_remove_group_02(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")

    collection.removeGroup("Новая группа")
    assert collection.getGroups() == []


def test_remove_group_03_invalid(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")

    with pytest.raises(KeyError):
        collection.removeGroup("Абырвалг")
    with pytest.raises(KeyError):
        collection.removeGroup("")


def test_remove_group_04(wxapp, tmp_path):
    files = ["new.png", "image_01.JPG"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")
    collection.addIcons("Новая группа", fullPaths)

    collection.removeGroup("Новая группа")
    assert collection.getGroups() == []


def test_add_icons_01_empty(wxapp, tmp_path):
    files = []
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")

    collection.addIcons("Новая группа", fullPaths)
    assert collection.getIcons("Новая группа") == []


def test_add_icons_02_empty(wxapp, tmp_path):
    files = []
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))
    collection.addGroup("Новая группа")

    collection.addIcons("Новая группа", fullPaths)
    assert collection.getIcons("Новая группа") == []


def test_add_icons_03_empty(wxapp, tmp_path):
    files = []
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    collection.addIcons("", fullPaths)
    assert collection.getIcons(None) == []


def test_add_icons_04_invalid(wxapp, tmp_path):
    files = ["new.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    with pytest.raises(KeyError):
        collection.addIcons("Другая группа", fullPaths)


def test_add_icons_png(wxapp, tmp_path):
    files = ["new.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    collection.addIcons("", fullPaths)

    icons = collection.getIcons(None)
    assert len(icons) == 1
    assert "new.png" in icons[0]
    assert collection.getCover(None) is None


def test_add_icons_svg(wxapp, tmp_path):
    files = ["new.svg"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    collection.addIcons("", fullPaths)

    icons = collection.getIcons(None)
    assert len(icons) == 1
    assert "new.svg" in icons[0]
    assert collection.getCover(None) is None


def test_add_icons_png_and_svg(wxapp, tmp_path):
    files = ["new.png", "new.svg"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    collection.addIcons("", fullPaths)

    icons = collection.getIcons(None)
    assert len(icons) == 1
    assert "new.svg" in icons[0]
    assert collection.getCover(None) is None


def test_add_icons_06(wxapp, tmp_path):
    files = ["new.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    collection.addIcons(None, fullPaths)

    icons = collection.getIcons(None)
    assert "new.png" in icons[0]


def test_add_icons_07(wxapp, tmp_path):
    files = ["new.png", "image_01.JPG"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))

    collection.addIcons(None, fullPaths)

    icons = sorted(collection.getIcons(None))
    assert "image_01.png" in icons[0]
    assert "new.png" in icons[1]


def test_add_icons_08(wxapp, tmp_path):
    files = ["new.png", "image_01.JPG"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 2
    assert "image_01.png" in icons[0]
    assert "new.png" in icons[1]
    assert collection.getCover("Новая группа") is None


def test_add_icons_09(wxapp, tmp_path):
    files = ["new.png", "image_01.JPG", "__init__.py"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 2
    assert "image_01.png" in icons[0]
    assert "new.png" in icons[1]


def test_add_icons_10_not_exists(wxapp, tmp_path):
    files = ["new.png", "image_01.JPG", "notexists.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 2
    assert "image_01.png" in icons[0]
    assert "new.png" in icons[1]


def test_add_icons_11(wxapp, tmp_path):
    files = ["new.png", "new.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 2
    assert "new.png" in icons[0]
    assert "new_(1).png" in icons[1]


def test_add_icons_12(wxapp, tmp_path):
    files = ["new.png", "new.png", "new.png", "new.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 4
    assert "new.png" in icons[0]
    assert "new_(1).png" in icons[1]
    assert "new_(2).png" in icons[2]
    assert "new_(3).png" in icons[3]


def test_add_icons_13(wxapp, tmp_path):
    files = ["__sample.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 1
    assert "__sample.png" not in icons[0]
    assert "sample.png" in icons[0]


def test_add_icons_14(wxapp, tmp_path):
    files = ["______sample.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 1
    assert "______sample.png" not in icons[0]
    assert "__sample.png" not in icons[0]
    assert "sample.png" in icons[0]


def test_add_icons_15(wxapp, tmp_path):
    files = ["______sample.png", "__sample.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 2
    assert "__sample.png" not in icons[0]
    assert "sample.png" in icons[0]
    assert "sample_(1).png" in icons[1]


def test_add_icons_16_invalid(wxapp, tmp_path):
    files = ["invalid.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 0


def test_add_icons_17_invalid(wxapp, tmp_path):
    files = ["invalid.png", "new.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 1
    assert "new.png" in icons[0]


def test_add_icons_18_invalid(wxapp, tmp_path):
    files = ["new.png", "invalid.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)

    collection.addIcons(groupname, fullPaths)

    icons = sorted(collection.getIcons(groupname))
    assert len(icons) == 1
    assert "new.png" in icons[0]


def test_add_icons_19_resize(wxapp, tmp_path):
    files = [
        "16x16.png",
        "16x15.png",
        "16x17.png",
        "15x16.png",
        "17x16.png",
        "17x17.png",
        "15x15.png",
        "8x8.png",
        "8x16.png",
        "16x8.png",
        "first.png",
        "first_vertical.png",
    ]

    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    collection = IconsCollection(str(tmp_path))
    collection.addIcons(None, fullPaths)

    icons = sorted(collection.getIcons(None))
    assert len(icons) == 12

    icons = {fname: os.path.join(str(tmp_path), fname) for fname in files}

    for fname in files:
        assert getImageSize(icons[fname]) == (16, 16)


def test_add_cover_01_group(wxapp, tmp_path):
    files = []
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)
    collection.addIcons(groupname, fullPaths)

    coverpath = os.path.join(IMAGES_DIR, "icon.png")

    newCoverPath = os.path.join(
        str(tmp_path), groupname, IconsCollection.COVER_FILE_NAME
    )

    collection.setCover(groupname, coverpath)
    assert os.path.exists(newCoverPath)
    assert os.path.abspath(newCoverPath) == os.path.abspath(
        collection.getCover(groupname)
    )

    collection.setCover(groupname, coverpath)
    assert os.path.exists(
        os.path.join(str(tmp_path), groupname, IconsCollection.COVER_FILE_NAME)
    )


def test_add_cover_02_root(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))

    coverpath = os.path.join(IMAGES_DIR, "icon.png")

    newCoverPath = os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME)

    collection.setCover(None, coverpath)
    assert os.path.exists(newCoverPath)
    assert os.path.abspath(newCoverPath) == os.path.abspath(
        collection.getCover(None)
    )

    collection.setCover(None, coverpath)
    assert os.path.exists(os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME))


def test_add_cover_03_root(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))

    coverpath = os.path.join(IMAGES_DIR, "icon.png")

    newCoverPath = os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME)

    collection.setCover("", coverpath)
    assert os.path.exists(newCoverPath)
    assert os.path.abspath(newCoverPath) == os.path.abspath(
        collection.getCover(None)
    )

    collection.setCover("", coverpath)
    assert os.path.exists(os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME))


def test_add_cover_04_root_invalid(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))

    coverpath = os.path.join(IMAGES_DIR, "invalid.png")

    collection.setCover("", coverpath)
    assert not os.path.exists(os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME))


def test_add_cover_05_root(wxapp, tmp_path):
    collection = IconsCollection(str(tmp_path))

    coverpath = os.path.join(IMAGES_DIR, "first.jpg")

    collection.setCover(None, coverpath)
    assert os.path.exists(os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME))

    assert _get_max_image_size(
        os.path.join(str(tmp_path), IconsCollection.COVER_FILE_NAME)
    ) == 16


def test_add_cover_06_group(wxapp, tmp_path):
    files = ["new.png", "8x8.png"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)
    collection.addIcons(groupname, fullPaths)

    coverpath = os.path.join(IMAGES_DIR, "icon.png")

    newCoverPath = os.path.join(
        str(tmp_path), groupname, IconsCollection.COVER_FILE_NAME
    )

    collection.setCover(groupname, coverpath)
    assert os.path.exists(newCoverPath)
    assert os.path.abspath(newCoverPath) == os.path.abspath(
        collection.getCover(groupname)
    )


def test_add_cover_06_group_svg(wxapp, tmp_path):
    files = ["new.png", "8x8.png", "image1.svg"]
    fullPaths = [os.path.join(IMAGES_DIR, fname) for fname in files]

    groupname = "Новая группа"

    collection = IconsCollection(str(tmp_path))
    collection.addGroup(groupname)
    collection.addIcons(groupname, fullPaths)

    coverpath = os.path.join(IMAGES_DIR, "image1.svg")

    newCoverPath = os.path.join(
        str(tmp_path), groupname, IconsCollection.COVER_FILE_NAME_SVG
    )

    collection.setCover(groupname, coverpath)
    assert os.path.exists(newCoverPath)
    assert os.path.abspath(newCoverPath) == os.path.abspath(
        collection.getCover(groupname)
    )
