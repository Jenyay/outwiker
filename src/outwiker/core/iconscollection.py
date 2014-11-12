# -*- coding: UTF-8 -*-

import os
import os.path
import shutil

from outwiker.core.commands import isImage
from outwiker.core.thumbmakerpil import ThumbmakerPil


class DuplicateGroupError (BaseException):
    pass


class IconsCollection (object):
    '''
    Class for the working with groups of the icons
    '''

    # File name for cover of the group
    COVER_FILE_NAME = u'__cover.png'


    def __init__ (self, iconsDirList):
        '''
        iconsDirList - list of the root directories with icons
        '''
        self._iconsDirList = iconsDirList

        # Key - group name, value - list of the files (full paths)
        self._groups = {}

        # Key - group name, value - full path to icon for group
        self._groupsCover = {}

        # List of the files for root folders with icons
        self._root = []

        # Full path to cover for root group
        self._rootCover = None

        self._thumbmaker = ThumbmakerPil ()
        self._maxIconSize = 16

        self._scanIconsDirs (iconsDirList)


    def getRootCover (self):
        return self._rootCover


    def getGroupCover (self, groupname):
        if groupname not in self._groups:
            raise KeyError

        return self._groupsCover.get (groupname, None)


    def _scanIconsDirs (self, iconsDirList):
        '''
        Fill _groups and _root
        '''
        self._root = []
        self._groups = {}
        self._rootCover = None
        self._groupsCover = {}

        for folder in iconsDirList:
            rootIcons, cover = self._findIcons (folder)
            self._root += rootIcons

            if cover is not None:
                newBaseCover = os.path.basename (cover)

                if self._rootCover is None or newBaseCover == self.COVER_FILE_NAME:
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
        '''
        Return files list (full paths) for icons in 'folder' and cover icon
        '''
        cover = None
        result = []
        files = sorted (os.listdir (folder))

        for fname in files:
            fullpath = os.path.join (folder, fname)

            if os.path.isfile (fullpath) and self._isIcon (fullpath):
                if fname == self.COVER_FILE_NAME:
                    cover = fullpath
                else:
                    result.append (fullpath)
                    if cover is None:
                        cover = fullpath

        return (result, cover)


    def _isIcon (self, fname):
        fname_lower = fname.lower()

        return (fname_lower.endswith (u'.png') or
                fname_lower.endswith (u'.jpg') or
                fname_lower.endswith (u'.gif') or
                fname_lower.endswith (u'.bmp'))


    def getAll (self):
        '''
        Return icons from all groups (root included)
        '''
        result = reduce (lambda x, y: x + y, self._groups.values(), []) + self._root
        result.sort()

        return result


    def getGroups (self):
        '''
        Return all group names
        '''
        return sorted (self._groups.keys())


    def getIcons (self, group):
        '''
        Return all icons (full paths) for groups with name group
        Raise KeyError if group not exists
        '''
        if group is None or len (group) == 0:
            return self._root
        else:
            return self._groups[group]


    def addGroup (self, groupname, dirindex=-1):
        '''
        Add new group (and directory) of the icons. dirindex - item index in _iconsDirList.
        If directory exists the method does nothing.
        The method can raise ValueError, IOError and SystemError exceptions.
        '''
        if not self._checkGroupName (groupname):
            raise ValueError

        parent = self._iconsDirList[dirindex]
        newdir = os.path.join (parent, groupname)

        if os.path.exists (newdir):
            return

        os.mkdir (newdir)
        self._groups[groupname] = []


    def renameGroup (self, groupname, newgroupname, dirindex=-1):
        '''
        dirindex - item index in _iconsDirList.
        The method can raise DuplicateGroupError, KeyError, ValueError, IOError and SystemError exceptions.
        '''
        if groupname == newgroupname:
            return

        if not self._checkGroupName (newgroupname):
            raise ValueError

        oldGroupPath = os.path.join (self._iconsDirList[dirindex], groupname)
        newGroupPath = os.path.join (self._iconsDirList[dirindex], newgroupname)

        if not os.path.exists (oldGroupPath):
            raise KeyError

        if os.path.exists (newGroupPath):
            raise DuplicateGroupError

        os.rename (oldGroupPath, newGroupPath)
        self._scanIconsDirs (self._iconsDirList)


    def removeGroup (self, groupname, dirindex=-1):
        '''
        Remove icon group and all icons inside it.
        '''
        oldGroupPath = os.path.join (self._iconsDirList[dirindex], groupname)
        if (len (groupname) == 0 or
                not os.path.exists (oldGroupPath) or
                groupname not in self._groups):
            raise KeyError

        shutil.rmtree (oldGroupPath)
        self._scanIconsDirs (self._iconsDirList)


    def addIcons (self, groupname, files, dirindex=-1):
        '''
        Add icons into group.
        files - list of full paths to icon files
        '''
        if groupname is None:
            groupname = u''

        grouppath = os.path.join (self._iconsDirList[dirindex], groupname)

        if not os.path.exists (grouppath):
            raise KeyError

        for iconpath in files:
            self._addIconToDir (grouppath, iconpath)

        self._scanIconsDirs (self._iconsDirList)


    def _addIconToDir (self, grouppath, iconpath):
        '''
        Add single icon with full path iconpath into folder groupPath.
        Not images is skipped.
        '''
        if (not isImage (iconpath) or not os.path.exists (iconpath)):
            return

        iconname = os.path.basename (iconpath)
        newIconName = self._getNewIconName (grouppath, iconname)
        newIconPath = os.path.join (grouppath, newIconName)

        try:
            self._thumbmaker.thumbByMaxSize (
                iconpath,
                self._maxIconSize,
                newIconPath,
                larger = False)
        except (IOError, ValueError):
            pass


    def _getNewIconName (self, grouppath, fname):
        '''
        Return unique name for icon on basis of fname.
        fname is basename of the full path to icon
        '''
        # Remove '__'
        prefix = u'__'
        clearname = fname
        while clearname.startswith (prefix):
            clearname = clearname[len (prefix):]

        dotPos = clearname.rfind (u'.')

        # Here we get only for picture 'fname'.
        assert dotPos != -1

        index = 1

        newname = clearname
        while os.path.exists (os.path.join (grouppath, newname)):
            newname = clearname[:dotPos] + u'_({})'.format (index) + clearname[dotPos:]
            index += 1

        # Return png always
        return newname[:newname.rfind (u'.')] + '.png'


    def _checkGroupName (self, groupname):
        return (len (groupname) != 0 and
                '\\' not in groupname and
                '/' not in groupname)


    def setCover (self, groupname, fname, dirindex=-1):
        if groupname is None:
            groupname = u''

        grouppath = os.path.join (self._iconsDirList[dirindex], groupname)

        if not os.path.exists (grouppath):
            raise KeyError

        if (not isImage (fname) or not os.path.exists (fname)):
            return

        newIconPath = os.path.join (grouppath, self.COVER_FILE_NAME)

        try:
            self._thumbmaker.thumbByMaxSize (
                fname,
                self._maxIconSize,
                newIconPath,
                larger = False)
        except (IOError, ValueError):
            pass

        self._scanIconsDirs (self._iconsDirList)
