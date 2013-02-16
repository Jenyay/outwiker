#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Небольшие функции, которые могут быть использованы в разных классах
"""
import os.path

from outwiker.pages.wiki.parser.tokenattach import AttachToken
from outwiker.core.system import getOS

from .params import STYLE_DEFAULT


def getFileName (fileParam):
    """
    Получить имя прикрепленного файла по параметру file
    fileParam - значение параметра file
    """
    fname = fileParam.strip()

    if fname.startswith (AttachToken.attachString):
        fname = fname[len (AttachToken.attachString): ]

    return fname


def getImagePath (imageName):
    """
    Получить полный путь до картинки
    """
    imagedir = unicode (os.path.join (os.path.dirname (__file__), "images"), getOS().filesEncoding)
    fname = os.path.join (imagedir, imageName)
    return fname


def getDefaultStyle (config):
    """
    Получить стиль, который используется по уомлчанию
    """
    from pygments.styles import STYLE_MAP
    style = config.defaultStyle.value

    if style not in STYLE_MAP:
        style = STYLE_DEFAULT

    return style


def fillStyleComboBox (config, comboBox, selectedStyle):
    """
    Заполнить ComboBox имеющимися стилями
    config - конфиг, откда будут читаться настройки (экземпляр класса SourceConfig)
    comboBox - ComboBox, который будет заполняться
    selectedStyle - стиль, который должен быть выбран по умолчанию
    """
    from pygments.styles import STYLE_MAP

    styles = STYLE_MAP.keys()
    styles.sort()

    assert len (styles) > 0

    comboBox.Clear()
    comboBox.AppendItems (styles)

    if selectedStyle not in styles:
        selectedStyle = getDefaultStyle (config)

    if selectedStyle in STYLE_MAP:
        index = styles.index (selectedStyle)
        assert index >= 0

        comboBox.SetSelection (index)
