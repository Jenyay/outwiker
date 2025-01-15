# -*- coding: utf-8 -*-

import logging
import os
import os.path
import shutil
from pathlib import Path
from typing import Iterable, List, Union

import wx

from outwiker.core.treetools import testreadonly
from outwiker.core.attachment import Attachment
from outwiker.core.events import BeginAttachRenamingParams
from outwiker.core.exceptions import ReadonlyException
from outwiker.gui.dialogs.overwritedialog import OverwriteDialog
from outwiker.app.services.messages import showError


logger = logging.getLogger('outwiker.app.services.attachment')


@testreadonly
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
    if page.readonly:
        raise ReadonlyException

    attachRoot = Attachment(page).getAttachPath()
    fname_src_full = os.path.join(attachRoot, fname_src)
    fname_dest_full = os.path.join(attachRoot, fname_dest)

    if fname_src_full == fname_dest_full:
        return False

    if os.path.exists(fname_dest_full):
        with OverwriteDialog(parent) as overwriteDialog:
            overwriteDialog.setVisibleOverwriteAllButton(False)
            overwriteDialog.setVisibleSkipButton(False)
            overwriteDialog.setVisibleSkipAllButton(False)

            text = os.path.basename(fname_dest)
            try:
                src_file_stat = os.stat(fname_src_full)
                dest_file_stat = os.stat(fname_dest_full)
            except FileNotFoundError:
                return False
            result = overwriteDialog.ShowDialog(text,
                                                src_file_stat,
                                                dest_file_stat)

            if result == overwriteDialog.ID_SKIP or result == wx.ID_CANCEL:
                return False

    try:
        os.replace(fname_src_full, fname_dest_full)
    except (IOError, shutil.Error) as e:
        text = _('Error renaming file\n{} -> {}\n{}').format(fname_src, fname_dest, str(e))
        logger.error(text)
        showError(parent, text)
        return False

    page.updateDateTime()
    return True


@testreadonly
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
    if page.readonly:
        raise ReadonlyException

    if not files:
        return

    def _expandFiles(files: Iterable[Union[str, Path]]) -> Iterable[Path]:
        """
        Returns list of all files (not directories) in subdirectories including
        """
        result = []
        for fname in files:
            item = Path(fname)
            if not item.exists():
                text = _('File not exists\n{0}').format(item)
                logger.error(text)
                showError(parent, text)
                return []

            if item.is_file():
                result.append(item)
            elif item.is_dir():
                files_inside = item.iterdir()
                result += _expandFiles(files_inside)

        return result

    def _getRelativeSubdirs(root: Path, expanded_files: Iterable[Union[str, Path]]) -> List[Path]:
        result = []
        for fname in expanded_files:
            path = Path(fname)
            parent = path.relative_to(root).parent
            if str(parent) != '.' and str(parent) != '/':
                result.append(parent)

        # Remove duplicates and sort directories alphabetically
        return sorted({item for item in result})

    attach = Attachment(page)
    attach_root = attach.getAttachPath(create=True)

    source_root_dir = Path(files[0]).parent
    expanded_files = _expandFiles(files)
    relative_source_files = [fname.relative_to(source_root_dir)
                             for fname in expanded_files]

    new_relative_attaches = []
    with OverwriteDialog(parent) as overwriteDialog:
        for fname_new in relative_source_files:
            old_path = Path(attach_root, subdir, fname_new)
            source_path = Path(source_root_dir, fname_new)

            if old_path == source_path:
                continue

            if old_path.exists():
                text = str(fname_new)
                old_file_stat = old_path.stat()
                new_file_stat = source_path.stat()

                result = overwriteDialog.ShowDialog(text,
                                                    old_file_stat,
                                                    new_file_stat)

                if result == overwriteDialog.ID_SKIP:
                    continue
                elif result == wx.ID_CANCEL:
                    return

            new_relative_attaches.append(fname_new)

    new_relative_subdirs = _getRelativeSubdirs(source_root_dir, expanded_files)

    for current_subdir in new_relative_subdirs:
        try:
            Path(attach_root, subdir, current_subdir).mkdir(parents=True, exist_ok=True)
        except IOError:
            text = _("Can't create directory: {}").format(current_subdir)
            logger.error(text)
            showError(parent, text)
            return

    for fname_relative in new_relative_attaches:
        source_full = Path(source_root_dir, fname_relative)
        attach_subdir = Path(attach_root, subdir, fname_relative.parent)
        try:
            Attachment(page).attach([source_full], attach_subdir)
        except (IOError, shutil.Error) as e:
            text = _('Error copying files\n{0}').format(str(e))
            logger.error(text)
            showError(parent, text)
            return


def getDefaultSubdirName() -> str:
    return _('New folder')


@testreadonly
def createSubdir(page, application):
    default_subdir_name = getDefaultSubdirName()

    if page is not None:
        attach = Attachment(page)
        root = Path(attach.getAttachPath(create=True), page.currentAttachSubdir)

        dirname = default_subdir_name
        index = 1

        while (root / dirname).exists():
            dirname = '{name} ({index})'.format(name=default_subdir_name, index=index)
            index += 1

        try:
            attach.createSubdir(Path(page.currentAttachSubdir, dirname))
            application.onBeginAttachRenaming(page, BeginAttachRenamingParams(str(dirname)))
        except IOError as e:
            message = _("Can't create folder {} for attachments").format(dirname)
            showError(application.mainWindow, message)
            logger.error("Can't create attachments subdir %s for the page '%s'. Error: %s", dirname, page.subpath, str(e))
