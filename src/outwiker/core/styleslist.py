# -*- coding: utf-8 -*-

import os
import os.path

from .style import Style


class StylesList:
    """
    Class for storing the list of existing page styles
    """

    def __init__(self, dirlist):
        """
        dirlist - list of directories where styles are searched
        """
        # List stores paths to existing verified styles
        self.__styles = sorted(self.__findStyles(dirlist))

    def __len__(self):
        return len(self.__styles)

    def __getitem__(self, index):
        return self.__styles[index]

    def __findStyles(self, dirlist):
        """
        Search for styles by paths in the dirlist
        """
        styles = []
        for path in dirlist:
            styles += self.__findStylesInDir(path)

        return styles

    def __findStylesInDir(self, path):
        """
        Returns the list of styles found in the path directory
        """
        if not os.path.exists(path):
            return []

        style = Style()
        return [
            os.path.join(path, styledir)
            for styledir in os.listdir(path)
            if (
                not styledir.startswith("__")
                and style.check(os.path.join(path, styledir))
            )
        ]
