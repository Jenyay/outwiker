# -*- coding: utf-8 -*-

"""
Вспомогательные функции для тестов
"""

import logging
import os
import shutil
import time
import gc
from pathlib import Path
from tempfile import mkdtemp
from typing import List

import wx

from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument


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
    Возвращает кортеж (ширина, высота)
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


def print_memory(count=30):
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
    summary.print_(sum1, limit=count)


def create_temp_notes_tree():
    '''
    Create empty notes tree in the temp directory
    '''
    path = mkdtemp(prefix='Абырвалг абыр')
    wikiroot = WikiDocument.create(path)
    return wikiroot


def remove_notes_tree(wikiroot):
    removeDir(wikiroot.path)


def attach_files(page, files: List[str], subdir: str = '.'):
    attach = Attachment(page)
    if subdir != '.':
        attach.createSubdir(subdir)

    attach_dir = Path('testdata', 'samplefiles')
    attaches = [attach_dir / fname for fname in files]
    attach.attach(attaches, subdir)
