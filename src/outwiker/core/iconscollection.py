# -*- coding: UTF-8 -*-

import os
import os.path


class IconsCollection (object):
    """
    Class for the wortking with groups of the icons
    """
    def __init__ (self, iconsDirList):
        """
        iconsDirList - list of the root directories with icons
        """
        # Folder names for localization
        _(u"awards")
        _(u"battery")
        _(u"books")
        _(u"computer")
        _(u"emotions")
        _(u"flags")
        _(u"folders")
        _(u"money")
        _(u"people")
        _(u"signs")
        _(u"software")
        _(u"tags")
        _(u"weather")

        # Key - group name, value - list of the files (full paths)
        self._groups = {}

        # List of the files for root folders with icons
        self._root = []

        self._scanIconsDirs (iconsDirList)


    def _scanIconsDirs (self, iconsDirList):
        """
        Fill _groups and _root
        """
        self._root = []
        self._groups = {}

        for folder in iconsDirList:
            self._root += self._findIcons (folder)
            self._findGroups (folder, self._groups)

        self._root.sort()


    def _findGroups (self, folder, groups):
        files = [fname for fname in os.listdir (folder)]

        for fname in files:
            fullpath = os.path.join (folder, fname)

            if os.path.isdir (fullpath):
                icons = self._findIcons (os.path.join (fullpath))

                if fname in groups:
                    groups[fname] += icons
                else:
                    groups[fname] = icons


    def _findIcons (self, folder):
        """
        Return files list (full paths) for icons in "folder"
        """
        result = []
        files = [fname for fname in os.listdir (folder)]
        for fname in files:
            fullpath = os.path.join (folder, fname)

            if os.path.isfile (fullpath) and self._isIcon (fullpath):
                result.append (fullpath)

        return result


    def _isIcon (self, fname):
        fname_lower = fname.lower()

        return (fname_lower.endswith (u".png") or
                fname_lower.endswith (u".jpg") or
                fname_lower.endswith (u".gif") or
                fname_lower.endswith (u".bmp"))


    def getAll (self):
        """
        Return icons from all groups (root included)
        """
        result = reduce (lambda x, y: x + y, self._groups.values(), []) + self._root
        result.sort()

        return result


    def getRoot (self):
        """
        Return icons from all roots
        """
        return self._root


    def getGroups (self):
        """
        Return all group names
        """
        return sorted (self._groups.keys())


    def getIcons (self, group):
        """
        Return all icons (full paths) for groups with name group
        Raise KeyError if group not exists
        """
        return self._groups[group]
