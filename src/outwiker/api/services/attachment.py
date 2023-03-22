from typing import List 

import wx

import outwiker.app.services.attachment as _attach


def renameAttach(parent: wx.Window,
                 page: 'outwiker.core.tree.WikiPage',
                 fname_src: str,
                 fname_dest: str) -> bool:
    """
    Rename attached file. Show overwrite dialog if necessary
    parent - parent for dialog window
    page - page to attach
    fname_src - source file name (relative path)
    fname_dest - new file name (relative path)

    Returns True if file renamed
    """
    return _attach.renameAttach(parent, page, fname_src, fname_dest)


def attachFiles(parent: wx.Window,
                page: 'outwiker.core.tree.WikiPage',
                files: List[str],
                subdir: str = '.'):
    """
    Attach files to page. Show overwrite dialog if necessary
    parent - parent for dialog window
    page - page to attach
    files - list of the files to attach
    subdir - subdirectory relative __attach directory
    """
    return _attach.attachFiles(parent, page, files, subdir)


def getDefaultSubdirName() -> str:
    return _attach.getDefaultSubdirName()


def createSubdir(page, application):
    return _attach.createSubdir(page, application)
