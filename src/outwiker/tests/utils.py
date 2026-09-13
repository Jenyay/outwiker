# -*- coding: utf-8 -*-

"""
Helper functions for tests
"""

import logging
import os
import shutil
import time
import gc
import re
from pathlib import Path
from tempfile import mkdtemp
from typing import List

import wx

from outwiker.api.core.tree import createNotesTree
from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiPage


def removeDir(path):
    """
    Remove the wiki from the specified directory
    """
    if os.path.exists(path):
        try:
            shutil.rmtree(path)
        except OSError:
            time.sleep(1)
            shutil.rmtree(path)


def getImageSize(fname):
    """
    Get the image size.
    Returns a tuple (width, height)
    """
    image = wx.Image(fname)
    width = image.GetWidth()
    height = image.GetHeight()
    return (width, height)


def createFile(fname):
    fp = open(fname, "w")
    fp.close()


def check_tag(text: str, tagname: str, **kwargs) -> bool:
    """
    Check whether the text contains the HTML tag tagname with the specified attributes.

    Attributes and their values are passed in kwargs in any order.
    Returns True if the tag is present in the text and contains all the specified
    attributes, or False otherwise.
    """
    tag_re = re.compile(fr"<{tagname}(?:\s+[^>]*)?/?>")
    tag = tag_re.search(text)
    if tag is None:
        return False

    return all(_check_attribute(tag.group(), name, value) for name, value in kwargs.items())


def _check_attribute(tag: str, name: str, value) -> bool:
    pattern = rf'\b{re.escape(name)}\s*=\s*["\']?{re.escape(str(value))}["\']?'
    return re.search(pattern, tag) is not None


class SkipLogFilter(logging.Filter):
    def filter(self, record):
        return False


def print_memory(count=30):
    """
    Print the statistics of the objects in the memory.
    Need pympler to use.
    """
    from pympler import muppy, summary

    gc.collect()
    all_objects = muppy.get_objects()
    my_types = muppy.filter(all_objects, Type=wx.Object)
    sum1 = summary.summarize(my_types)
    # sum1 = summary.summarize(all_objects)
    summary.print_(sum1, limit=count)


def create_temp_notes_tree():
    """
    Create empty note tree in the temp directory
    """
    path = mkdtemp(prefix="Абырвалг абыр")
    wikiroot = createNotesTree(path)
    return wikiroot


def remove_notes_tree(wikiroot):
    removeDir(wikiroot.path)


def attach_files(page: WikiPage, files: List[str], subdir: str = "."):
    attach = Attachment(page)
    if subdir != ".":
        attach.createSubdir(subdir)

    src_dir = Path("testdata", "samplefiles")
    attaches = [src_dir / fname for fname in files]
    attach.attach(attaches, subdir)


def copy_test_files_to_attachments(wikipage: WikiPage, files: List[str]) -> List[str]:
    """Copy files but not change edit datetime"""
    src_dir = os.path.join("testdata", "samplefiles")

    attach = Attachment(wikipage)
    attach_dir = attach.getAttachPath(create=True)

    src_full_paths = [os.path.join(src_dir, fname) for fname in files]
    atach_full_paths = [os.path.join(attach_dir, fname) for fname in files]
    for fname in src_full_paths:
        shutil.copy(fname, attach_dir)

    return atach_full_paths


def test_check_tag():
    assert check_tag("<b>text</b>", "b")
    assert check_tag("before <b>text</b> after", "b")
    assert check_tag(
        'before <a href="http://example.com" title="link">text</a> after',
        "a",
        href="http://example.com",
        title="link",
    )
    assert check_tag('<br/>', "br")
    assert check_tag("text <br/> after", "br")

    assert not check_tag('<a href="http://example.com">text</a>', "a", title="link")
    assert not check_tag('before <a href="http://example.com">text</a> after', "a", title="link")
