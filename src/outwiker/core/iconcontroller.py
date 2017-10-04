# -*- coding: utf-8 -*-


import os
import os.path

from defines import ICONS_STD_PREFIX


class IconController(object):
    def __init__(self, icons_path_list):
        '''
        icons_path_list -- list of the paths to icons collections.
            The first item is built-in icons.
        '''
        if not icons_path_list:
            raise ValueError

        self._icons_path_list = icons_path_list[:]

    def _is_subdir(self, fname, directory):
        fname = os.path.realpath(fname)
        directory = os.path.realpath(directory)
        relative = os.path.relpath(fname, directory)
        return not relative.startswith(os.pardir + os.sep)

    def is_builtin_icon(self, fname):
        '''
        Return True if fname is standard (built-in) icon file name,
        return False if fname is user's icon file name.
        '''
        if not fname:
            raise ValueError

        basename = os.path.basename(fname)

        main_path = self._icons_path_list[0]

        return (self._is_subdir(fname, main_path) and
                basename.startswith(ICONS_STD_PREFIX))

    @staticmethod
    def display_name(file_name):
        '''
        Return string to show icon name for user.
        Raise ValueError if file_name is None or empty string.
        '''
        if not file_name:
            raise ValueError

        text = os.path.basename(file_name)

        dotPos = text.rfind(".")
        if dotPos != -1:
            text = text[: dotPos]

        if text.startswith(ICONS_STD_PREFIX):
            text = text[len(ICONS_STD_PREFIX):]

        return text
