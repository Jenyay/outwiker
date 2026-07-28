# -*- coding: utf-8 -*-

"""
Helper functions that can be used across different classes
"""

import os.path

from outwiker.api.pages.wiki.wikiparser import AttachToken

from .params import STYLE_DEFAULT


def getFileName(fileParam) -> str:
    """
    Get the attached file name from file parameter.
    fileParam - value of the file parameter
    """
    fname = fileParam.strip()
    attach_string = AttachToken.attachString

    if fname.startswith(attach_string):
        fname = fname[len(attach_string) :]

    return fname


def getImagePath(imageName) -> str:
    """
    Get full path to an image
    """
    imagedir = os.path.join(os.path.dirname(__file__), "images")
    fname = os.path.join(imagedir, imageName)
    return fname


def getDefaultStyle(config) -> str:
    """
    Get the default style
    """
    from pygments.styles import STYLE_MAP

    style = config.defaultStyle.value

    if style not in STYLE_MAP:
        style = STYLE_DEFAULT

    return style


def fillStyleComboBox(config, comboBox, selectedStyle):
    """
    Fill ComboBox with available styles
    config - config to read settings from
        (SourceConfig instance)
    comboBox - ComboBox to fill
    selectedStyle - style that should be selected by default
    """
    from pygments.styles import STYLE_MAP

    styles = sorted(STYLE_MAP.keys())

    assert len(styles) > 0

    comboBox.Clear()
    comboBox.AppendItems(styles)

    if selectedStyle not in styles:
        selectedStyle = getDefaultStyle(config)

    if selectedStyle in STYLE_MAP:
        index = styles.index(selectedStyle)
        assert index >= 0

        comboBox.SetSelection(index)
