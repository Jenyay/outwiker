# -*- coding: UTF-8 -*-

"""
Вспомогательные функции для тестов
"""

import logging
import os
import shutil
import time

import wx


def removeDir(path):
    """
    Удалить вики из указанной папки
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError:
            time.sleep(1)
            shutil.rmtree(path)


def getImageSize(fname):
    """
    Получить размер картинки.
    Возвращает кортеж(ширина, высота)
    """
    image = wx.Image(fname)
    width = image.GetWidth()
    height = image.GetHeight()
    return (width, height)


def createFile(fname):
    fp = open(fname, 'w')
    fp.close()


class SkipLogFilter(logging.Filter):
    def filter(self, record):
        return False
