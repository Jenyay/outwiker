# -*- coding: utf-8 -*-


import os.path

from defines import ICONS_STD_PREFIX


class IconController(object):
    def __init__(self, icons_path_list):
        '''
        icons_path_list -- list of the paths to icons collections.
            The first item is built-in icons.
        '''
        self.icons_path_list = icons_path_list[:]

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
