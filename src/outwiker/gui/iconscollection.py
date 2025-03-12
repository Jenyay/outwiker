# -*- coding: utf-8 -*-

import os
import os.path
import shutil
import logging

from outwiker.gui.iconmaker import IconMaker
from outwiker.core.images import convert_name_to_svg, isImage, isSVG

logger = logging.getLogger("outwiker.core.iconscollection")


class DuplicateGroupError(BaseException):
    pass


class IconsCollection:
    """
    Class for the working with groups of the icons
    """

    # File name for cover of the group
    COVER_FILE_NAME = "__cover.png"
    COVER_FILE_NAME_SVG = "__cover.svg"

    def __init__(self, iconsDir):
        """
        iconsDir - Root directory (absolute path) with the icons
        """
        self._iconsDir = iconsDir

        # Key - group name, value - files list (full paths)
        self._groups = {}

        # Key - group name, value - full path to group icon
        self._groupsCover = {}

        self._rootGroupName = ""
        self._scanIconsDir(self._iconsDir)

    def __contains__(self, groupname):
        return groupname in self._groups

    def getCover(self, groupname):
        if groupname is None:
            groupname = self._rootGroupName

        if groupname not in self._groupsCover:
            raise KeyError

        return self._groupsCover.get(groupname, None)

    def _scanIconsDir(self, rootFolder):
        """
        Fill _groups and _groupsCover
        """
        self._groups = {self._rootGroupName: []}
        self._groupsCover = {self._rootGroupName: None}

        rootFiles = [self._rootGroupName]

        if os.path.exists(rootFolder):
            rootFiles += os.listdir(rootFolder)

        for itemname in rootFiles:
            fullpath = os.path.join(rootFolder, itemname)

            if os.path.isdir(fullpath):
                self._groups[itemname] = self._findIcons(fullpath)
                self._groupsCover[itemname] = self._findCover(fullpath)

    def _findCover(self, folder):
        """
        Return path to group cover or None if it is not exists
        """
        cover = None
        fullpath = os.path.join(folder, self.COVER_FILE_NAME)
        fullpath_svg = os.path.join(folder, self.COVER_FILE_NAME_SVG)
        if os.path.exists(fullpath_svg):
            cover = fullpath_svg
        elif os.path.exists(fullpath):
            cover = fullpath

        return cover

    def _findIcons(self, folder):
        """
        Return files list (full paths) for icons in 'folder'
        """
        result = []
        files = sorted(os.listdir(folder))

        for fname in files:
            fullpath = os.path.join(folder, fname)

            if (
                os.path.isfile(fullpath)
                and self._isIcon(fullpath)
                and fname != self.COVER_FILE_NAME
                and fname != self.COVER_FILE_NAME_SVG
            ):
                fullpath_svg = convert_name_to_svg(fullpath)
                # Skip bitmap icon if vector icon with same name exists
                if not os.path.exists(fullpath_svg) or fullpath == fullpath_svg: 
                    result.append(fullpath)

        return result

    def _isIcon(self, fname):
        fname_lower = fname.lower()

        return (
            fname_lower.endswith(".png")
            or fname_lower.endswith(".jpg")
            or fname_lower.endswith(".gif")
            or fname_lower.endswith(".bmp")
            or fname_lower.endswith(".svg")
        )

    def getGroups(self):
        """
        Return all group names
        """
        return [
            groupname
            for groupname in sorted(self._groups.keys())
            if groupname != self._rootGroupName
        ]

    def getIcons(self, groupname):
        """
        Return all icons (full paths) for groups with name group
        Raise KeyError if group not exists
        """
        if groupname is None:
            groupname = self._rootGroupName

        return self._groups[groupname]

    def addGroup(self, groupname):
        """
        Add new group (and directory) of the icons.
        If directory exists the method does nothing.
        The method can raise ValueError, IOError and SystemError exceptions.
        """
        if not self._checkGroupName(groupname):
            raise ValueError

        newdir = os.path.join(self._iconsDir, groupname)

        if os.path.exists(newdir):
            return

        os.mkdir(newdir)
        self._groups[groupname] = []

    def renameGroup(self, groupname, newgroupname):
        """
        The method can raise DuplicateGroupError, KeyError, ValueError,
            IOError and SystemError exceptions.
        """
        if groupname == newgroupname:
            return

        if not self._checkGroupName(newgroupname):
            raise ValueError

        oldGroupPath = os.path.join(self._iconsDir, groupname)
        newGroupPath = os.path.join(self._iconsDir, newgroupname)

        if not os.path.exists(oldGroupPath):
            raise KeyError

        if os.path.exists(newGroupPath):
            raise DuplicateGroupError

        os.rename(oldGroupPath, newGroupPath)
        self._scanIconsDir(self._iconsDir)

    def removeGroup(self, groupname):
        """
        Remove icon group and all icons inside it.
        """
        oldGroupPath = os.path.join(self._iconsDir, groupname)
        if (
            len(groupname) == 0
            or not os.path.exists(oldGroupPath)
            or groupname not in self._groups
        ):
            raise KeyError

        shutil.rmtree(oldGroupPath)
        self._scanIconsDir(self._iconsDir)

    def addIcons(self, groupname, files):
        """
        Add icons into group.
        files - list of full paths to icon files
        """
        if groupname is None:
            groupname = self._rootGroupName

        grouppath = os.path.join(self._iconsDir, groupname)

        if not os.path.exists(grouppath):
            raise KeyError

        for iconpath in files:
            self._addIconToDir(grouppath, iconpath)

        self._scanIconsDir(self._iconsDir)

    def _addIconToDir(self, grouppath, iconpath):
        """
        Add single icon with full path iconpath into folder groupPath.
        Not images will be skipped.
        """
        if (not isImage(iconpath) and not isSVG(iconpath)) or not os.path.exists(iconpath):
            return

        iconname = os.path.basename(iconpath)
        newIconName = self._getNewIconName(grouppath, iconname)
        newIconPath = os.path.join(grouppath, newIconName)

        try:
            if isSVG(iconpath):
                shutil.copyfile(iconpath, newIconPath)
            else:
                IconMaker().create(iconpath, newIconPath)
        except (IOError, ValueError):
            logger.error("Icon creation error. File name: %s", iconpath)

    def _getNewIconName(self, grouppath, fname):
        """
        Return unique name for icon on basis of fname.
        fname is basename of the full path to icon
        """
        prefix = "__"
        clearname = fname
        while clearname.startswith(prefix):
            clearname = clearname[len(prefix) :]

        dotPos = clearname.rfind(".")

        # Here we get only for picture 'fname'.
        assert dotPos != -1

        index = 1

        newname = clearname
        while os.path.exists(os.path.join(grouppath, newname)):
            newname = clearname[:dotPos] + "_({})".format(index) + clearname[dotPos:]
            index += 1

        extension = ".svg" if isSVG(fname) else ".png"

        # Return png always
        return newname[: newname.rfind(".")] + extension

    def _checkGroupName(self, groupname):
        return len(groupname) != 0 and "\\" not in groupname and "/" not in groupname

    def setCover(self, groupname, fname):
        if groupname is None:
            groupname = self._rootGroupName

        grouppath = os.path.join(self._iconsDir, groupname)

        if not os.path.exists(grouppath):
            raise KeyError

        if (not isImage(fname) and not isSVG(fname)) or not os.path.exists(fname):
            return

        try:
            if isSVG(fname):
                newIconPath = os.path.join(grouppath, self.COVER_FILE_NAME_SVG)
                shutil.copy(fname, newIconPath)
            else:
                newIconPath = os.path.join(grouppath, self.COVER_FILE_NAME)
                IconMaker().create(fname, newIconPath)
        except (IOError, ValueError):
            pass

        self._scanIconsDir(self._iconsDir)
