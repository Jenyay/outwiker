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

from outwiker.api.core.tree import createNotesTree
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiPage


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
    Create empty note tree in the temp directory
    '''
    path = mkdtemp(prefix='Абырвалг абыр')
    wikiroot = createNotesTree(path)
    return wikiroot


def remove_notes_tree(wikiroot):
    removeDir(wikiroot.path)


def attach_files(page: WikiPage, files: List[str], subdir: str = '.'):
    attach = Attachment(page)
    if subdir != '.':
        attach.createSubdir(subdir)

    src_dir = Path('testdata', 'samplefiles')
    attaches = [src_dir / fname for fname in files]
    attach.attach(attaches, subdir)


def copy_test_files_to_attachments(wikipage: WikiPage, files: List[str]) -> List[str]:
    """Copy files but not change edit datetime"""
    src_dir = os.path.join('testdata', 'samplefiles')

    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    src_full_paths = [os.path.join(src_dir, fname) for fname in files]
    atach_full_paths = [os.path.join(attach_dir, fname) for fname in files]
    for fname in src_full_paths:
        shutil.copy(fname, attach_dir)

    return atach_full_paths
