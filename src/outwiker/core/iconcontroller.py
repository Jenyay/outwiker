# -*- coding: utf-8 -*-


import os
import os.path
import shutil
from typing import Dict, Union

from outwiker.core.defines import ICONS_EXTENSIONS, ICONS_STD_PREFIX, PAGE_ICON_NAME
from outwiker.core.events import PAGE_UPDATE_ICON
from outwiker.core.exceptions import ReadonlyException
from outwiker.core.images import convert_name_to_svg


class IconController:
    def __init__(self, builtin_icons_path):
        """
        builtin_icons_path -- path to built-in icons folder.
        """
        self._builtin_icons_path = builtin_icons_path
        self._redirect: Dict[str, str] = {}

        # Used to move builtin icons to other file name
        self._redirect["__std_attach.png"] = os.path.join("office", "__std_clip.svg")
        self._redirect["__std_calculator.png"] = os.path.join("office", "__std_calculator.png")
        self._redirect["__std_cut.png"] = os.path.join("office", "__std_cut.png")
        self._redirect["__std_cuter.png"] = os.path.join("office", "__std_cutter.png")
        self._redirect["folders/__std_folder.svg"] = os.path.join("folders", "__std_folder_yellow.svg")
        self._redirect["folders/__std_folder-black.svg"] = os.path.join("folders", "__std_folder_black.svg")
        self._redirect["folders/__std_folder-blue.svg"] = os.path.join("folders", "__std_folder_blue.svg")
        self._redirect["folders/__std_folder-green.svg"] = os.path.join("folders", "__std_folder_green.svg")
        self._redirect["folders/__std_folder-red.svg"] = os.path.join("folders", "__std_folder_red.svg")
        self._redirect["folders/__std_folder_open.svg"] = os.path.join("folders", "__std_folder-search.svg")
        self._redirect["folders/__std_folders.svg"] = os.path.join("folders", "__std_folders_yellow.svg")
        self._redirect["folders/__std_folder-vertical-document.png"] = os.path.join("folders", "__std_folder-vertical-document_yellow.svg")
        self._redirect["folders/__std_folder-vertical-open.png"] = os.path.join("folders", "__std_folder-vertical-open_yellow.svg")
        self._redirect["folders/__std_folder_clipboard.svg"] = os.path.join("folders", "__std_folder-clipboard.svg")

    # Used in tests
    def add_redirect(self, src_icon_path, dst_icon_path):
        self._redirect[src_icon_path] = dst_icon_path

    def _is_subdir(self, fname, directory):
        fname = os.path.realpath(fname)
        directory = os.path.realpath(directory)

        try:
            relative = os.path.relpath(fname, directory)
        except ValueError:
            return False

        return not relative.startswith(os.pardir + os.sep)

    def is_builtin_icon(self, fname):
        """
        Return True if fname is standard (built-in) icon file name,
        return False if fname is user's icon file name.
        """
        if not fname:
            raise ValueError

        basename = os.path.basename(fname)

        main_path = self._builtin_icons_path

        return self._is_subdir(fname, main_path) and basename.startswith(
            ICONS_STD_PREFIX
        )

    def _check_icon_extension(self, fname):
        for extension in ICONS_EXTENSIONS:
            if fname.endswith("." + extension):
                return True

        return False

    def remove_icon(self, page):
        self._remove_icon(page)
        page.updateDateTime()
        page.root.onPageUpdate(page, change=PAGE_UPDATE_ICON)

    def _remove_icon(self, page):
        if page.readonly:
            raise ReadonlyException

        for extension in ICONS_EXTENSIONS:
            icon_fname = os.path.join(page.path, PAGE_ICON_NAME + "." + extension)
            if os.path.exists(icon_fname):
                os.remove(icon_fname)

        page.params.iconOption.value = ""

    def set_icon(self, page, icon_fname: Union[str, None]) -> Union[str, None]:
        """
        Set icon (icon_fname - icon file name) for a page.
        If icon_fname is built-in icon then link to icon will be added to page
        params, else file will be copied to page folder.

        Raises exceptions: ValueError, IOError
        """
        if page.readonly:
            raise ReadonlyException

        if icon_fname is None and self.get_icon(page) is None:
            return None
        elif icon_fname is None:
            self._remove_icon(page)
            page.params.iconOption.remove_option()
        elif self.is_builtin_icon(icon_fname):
            self._set_builtin_icon(page, icon_fname)
        else:
            self._set_custom_icon(page, icon_fname)

        page.updateDateTime()
        page.root.onPageUpdate(page, change=PAGE_UPDATE_ICON)
        return icon_fname

    def _set_custom_icon(self, page, icon_fname):
        assert icon_fname is not None

        icon_fname = os.path.abspath(icon_fname)
        if not self._check_icon_extension(icon_fname):
            raise ValueError

        dot = icon_fname.rfind(".")
        extension = icon_fname[dot:]

        newname = PAGE_ICON_NAME + extension
        newpath = os.path.abspath(os.path.join(page.path, newname))

        if icon_fname != newpath:
            self._remove_icon(page)
            shutil.copyfile(icon_fname, newpath)

    def _set_builtin_icon(self, page, icon_fname):
        assert icon_fname is not None

        icon_fname = os.path.abspath(icon_fname)
        if not self._check_icon_extension(icon_fname):
            raise ValueError

        self._remove_icon(page)
        rel_icon_path = os.path.relpath(icon_fname, self._builtin_icons_path)
        page.params.iconOption.value = rel_icon_path

    def get_icon(self, page) -> Union[str, None]:
        """
        Return path to a page icon or None if icon is not installed.
        """
        assert page is not None

        # Find __icon.* file
        for extension in ICONS_EXTENSIONS:
            fname = os.path.join(page.path, PAGE_ICON_NAME + "." + extension)
            if os.path.exists(fname):
                return fname

        # If an icon file name wrote in the page params.
        icon_from_config = page.params.iconOption.value.strip()
        icon_file = None
        if icon_from_config:
            icon_from_config = self.take_redirect(icon_from_config)
            icon_path_src = os.path.join(self._builtin_icons_path, icon_from_config)

            # Return vector icon instead of bitmap icon if exists
            icon_path_svg = convert_name_to_svg(icon_path_src)
            if icon_path_src != icon_path_svg and os.path.exists(icon_path_svg):
                icon_file = icon_path_svg
            else:
                icon_file = icon_path_src

        if icon_file is not None and not os.path.exists(icon_file):
            icon_file = None

        return icon_file

    def take_redirect(self, icon_from_config: str) -> str:
        icon_from_config = self._fix_slashes(icon_from_config)
        return self._redirect.get(icon_from_config, icon_from_config)

    def _fix_slashes(self, path: str) -> str:
        path = path.replace("\\", os.sep)
        path = path.replace("/", os.sep)
        return path

    @staticmethod
    def display_name(file_name):
        """
        Return string to show icon name for user.
        Raise ValueError if file_name is None or empty string.
        """
        if not file_name:
            raise ValueError

        text = os.path.basename(file_name)

        dotPos = text.rfind(".")
        if dotPos != -1:
            text = text[:dotPos]

        if text.startswith(ICONS_STD_PREFIX):
            text = text[len(ICONS_STD_PREFIX) :]

        return text
