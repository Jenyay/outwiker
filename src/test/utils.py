# -*- coding: utf-8 -*-

"""
Вспомогательные функции для тестов
"""

import logging
import os
import shutil
import time
import gc

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


def print_memory():
    '''
    Print the statistics of the objects in the memory.
    Need pympler to use.
    '''
    from pympler import muppy, summary

    gc.collect()
    all_objects = muppy.get_objects()
    my_types = muppy.filter(all_objects, Type=wx.Object)
    sum1 = summary.summarize(my_types)
    # sum1 = summary.summarize(all_objects)
    summary.print_(sum1, limit=50)
