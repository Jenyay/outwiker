# -*- coding: utf-8 -*-


import os
import os.path
import shutil
from typing import Union

from outwiker.core.defines import ICONS_EXTENSIONS, ICONS_STD_PREFIX, PAGE_ICON_NAME
from outwiker.core.events import PAGE_UPDATE_ICON
from outwiker.core.exceptions import ReadonlyException


class IconController:
    def __init__(self, builtin_icons_path):
        """
        builtin_icons_path -- path to built-in icons folder.
        """
        self._builtin_icons_path = builtin_icons_path

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
        The existence of a built-in icons is not checked.

        Added in outwiker.core 1.5
        """
        assert page is not None

        # Find __icon.* file
        for extension in ICONS_EXTENSIONS:
            fname = os.path.join(page.path, PAGE_ICON_NAME + "." + extension)
            if os.path.exists(fname):
                return fname

        # If an icon file name wrote in the page params.
        icon_from_config = page.params.iconOption.value.strip()
        if icon_from_config:
            icon_from_config = icon_from_config.replace("\\", os.sep)
            icon_from_config = icon_from_config.replace("/", os.sep)
            return os.path.join(self._builtin_icons_path, icon_from_config)

        return None

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
