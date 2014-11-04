# -*- coding: UTF-8 -*-

import os
import os.path


class IconsCollection (object):
    """
    Class for the working with groups of the icons
    """
    def __init__ (self, iconsDirList):
        """
        iconsDirList - list of the root directories with icons
        """
        self._iconsDirList = iconsDirList

        # Folder names for localization
        _(u"awards")
        _(u"battery")
        _(u"books")
        _(u"computer")
        _(u"emotions")
        _(u"flags")
        _(u"folders")
        _(u"food")
        _(u"internet")
        _(u"money")
        _(u"people")
        _(u"signs")
        _(u"software")
        _(u"tags")
        _(u"weather")

        # Key - group name, value - list of the files (full paths)
        self._groups = {}

        # Key - group name, value - full path to icon for group
        self._groupsCover = {}

        # List of the files for root folders with icons
        self._root = []

        # Full path to cover for root group
        self._rootCover = None

        self._scanIconsDirs (iconsDirList)


    def getRootCover (self):
        return self._rootCover


    def getGroupCover (self, groupname):
        if groupname not in self._groups:
            raise KeyError

        return self._groupsCover.get (groupname, None)


    def _scanIconsDirs (self, iconsDirList):
        """
        Fill _groups and _root
        """
        self._root = []
        self._groups = {}

        for folder in iconsDirList:
            rootIcons, cover = self._findIcons (folder)
            self._root += rootIcons

            if cover is not None:
                newBaseCover = os.path.basename (cover)

                if self._rootCover is None or newBaseCover.startswith ("__"):
                    self._rootCover = cover

            self._findGroups (folder, self._groups)

        self._root.sort()


    def _findGroups (self, folder, groups):
        files = os.listdir (folder)

        for fname in files:
            fullpath = os.path.join (folder, fname)

            if os.path.isdir (fullpath):
                icons, cover = self._findIcons (os.path.join (fullpath))

                if fname in groups:
                    groups[fname] += icons
                else:
                    groups[fname] = icons

                if cover is not None and fname not in self._groupsCover:
                    self._groupsCover[fname] = cover


    def _findIcons (self, folder):
        """
        Return files list (full paths) for icons in "folder" and cover icon
        """
        cover = None
        result = []
        files = sorted (os.listdir (folder))

        for fname in files:
            fullpath = os.path.join (folder, fname)

            if os.path.isfile (fullpath) and self._isIcon (fullpath):
                if fname.startswith (u"__") and cover is None:
                    cover = fullpath

                if not fname.startswith (u"__"):
                    result.append (fullpath)
                    if cover is None:
                        cover = fullpath

        return (result, cover)


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
