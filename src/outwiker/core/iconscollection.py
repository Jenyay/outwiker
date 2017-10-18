# -*- coding: utf-8 -*-

import os
import os.path
import shutil

from outwiker.core.commands import isImage
from outwiker.core.iconmaker import IconMaker


class DuplicateGroupError(BaseException):
    pass


class IconsCollection(object):
    '''
    Class for the working with groups of the icons
    '''

    # File name for cover of the group
    COVER_FILE_NAME = u'__cover.png'

    def __init__(self, iconsDir):
        '''
        iconsDir - Root directory (absolute path) with the icons
        '''
        self._iconsDir = iconsDir

        # Key - group name, value - files list (full paths)
        self._groups = {}

        # Key - group name, value - full path to group icon
        self._groupsCover = {}

        self._rootGroupName = u''
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
        '''
        Fill _groups and _groupsCover
        '''
        self._groups = {}
        self._groupsCover = {}

        rootFiles = [self._rootGroupName] + os.listdir(rootFolder)

        for itemname in rootFiles:
            fullpath = os.path.join(rootFolder, itemname)

            if os.path.isdir(fullpath):
                self._groups[itemname] = self._findIcons(fullpath)
                self._groupsCover[itemname] = self._findCover(fullpath)

    def _findCover(self, folder):
        '''
        Return path to group cover or None if it is not exists
        '''
        cover = None
        fullpath = os.path.join(folder, self.COVER_FILE_NAME)
        if os.path.exists(fullpath):
            cover = fullpath

        return cover

    def _findIcons(self, folder):
        '''
        Return files list (full paths) for icons in 'folder'
        '''
        result = []
        files = sorted(os.listdir(folder))

        for fname in files:
            fullpath = os.path.join(folder, fname)

            if (os.path.isfile(fullpath) and
                    self._isIcon(fullpath) and
                    fname != self.COVER_FILE_NAME):
                result.append(fullpath)

        return result

    def _isIcon(self, fname):
        fname_lower = fname.lower()

        return (fname_lower.endswith(u'.png') or
                fname_lower.endswith(u'.jpg') or
                fname_lower.endswith(u'.gif') or
                fname_lower.endswith(u'.bmp'))

    def getGroups(self):
        '''
        Return all group names
        '''
        return [groupname
                for groupname
                in sorted(self._groups.keys())
                if groupname != self._rootGroupName]

    def getIcons(self, groupname):
        '''
        Return all icons (full paths) for groups with name group
        Raise KeyError if group not exists
        '''
        if groupname is None:
            groupname = self._rootGroupName

        return self._groups[groupname]

    def addGroup(self, groupname):
        '''
        Add new group (and directory) of the icons.
        If directory exists the method does nothing.
        The method can raise ValueError, IOError and SystemError exceptions.
        '''
        if not self._checkGroupName(groupname):
            raise ValueError

        newdir = os.path.join(self._iconsDir, groupname)

        if os.path.exists(newdir):
            return

        os.mkdir(newdir)
        self._groups[groupname] = []

    def renameGroup(self, groupname, newgroupname):
        '''
        The method can raise DuplicateGroupError, KeyError, ValueError,
            IOError and SystemError exceptions.
        '''
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
        '''
        Remove icon group and all icons inside it.
        '''
        oldGroupPath = os.path.join(self._iconsDir, groupname)
        if (len(groupname) == 0 or
                not os.path.exists(oldGroupPath) or
                groupname not in self._groups):
            raise KeyError

        shutil.rmtree(oldGroupPath)
        self._scanIconsDir(self._iconsDir)

    def addIcons(self, groupname, files):
        '''
        Add icons into group.
        files - list of full paths to icon files
        '''
        if groupname is None:
            groupname = self._rootGroupName

        grouppath = os.path.join(self._iconsDir, groupname)

        if not os.path.exists(grouppath):
            raise KeyError

        for iconpath in files:
            self._addIconToDir(grouppath, iconpath)

        self._scanIconsDir(self._iconsDir)

    def _addIconToDir(self, grouppath, iconpath):
        '''
        Add single icon with full path iconpath into folder groupPath.
        Not images will be skipped.
        '''
        if (not isImage(iconpath) or not os.path.exists(iconpath)):
            return

        iconname = os.path.basename(iconpath)
        newIconName = self._getNewIconName(grouppath, iconname)
        newIconPath = os.path.join(grouppath, newIconName)

        try:
            IconMaker().create(iconpath, newIconPath)
        except(IOError, ValueError):
            pass

    def _getNewIconName(self, grouppath, fname):
        '''
        Return unique name for icon on basis of fname.
        fname is basename of the full path to icon
        '''
        prefix = u'__'
        clearname = fname
        while clearname.startswith(prefix):
            clearname = clearname[len(prefix):]

        dotPos = clearname.rfind(u'.')

        # Here we get only for picture 'fname'.
        assert dotPos != -1

        index = 1

        newname = clearname
        while os.path.exists(os.path.join(grouppath, newname)):
            newname = (clearname[:dotPos] +
                       u'_({})'.format(index) +
                       clearname[dotPos:])
            index += 1

        # Return png always
        return newname[:newname.rfind(u'.')] + '.png'

    def _checkGroupName(self, groupname):
        return (len(groupname) != 0 and
                '\\' not in groupname and
                '/' not in groupname)

    def setCover(self, groupname, fname):
        if groupname is None:
            groupname = self._rootGroupName

        grouppath = os.path.join(self._iconsDir, groupname)

        if not os.path.exists(grouppath):
            raise KeyError

        if (not isImage(fname) or not os.path.exists(fname)):
            return

        newIconPath = os.path.join(grouppath, self.COVER_FILE_NAME)

        try:
            IconMaker().create(fname, newIconPath)
        except(IOError, ValueError):
            pass

        self._scanIconsDir(self._iconsDir)
