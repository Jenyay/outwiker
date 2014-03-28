#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path
from abc import abstractmethod, ABCMeta

import wx


class BaseFileIcons (object):
    """
    Базовый класс для получения иконок прикрепленных файлов
    """
    __metaclass__ = ABCMeta

    def __init__ (self):
        self.DEFAULT_FILE_ICON = 0
        self.FOLDER_ICON = 1

        self._imageList = wx.ImageList (16, 16)

        # Ключ - расширение файла, значение - номер иконки в self._imageList
        self._iconsDict = {}


    def initialize (self):
        from outwiker.core.system import getImagesDir
        imagesDir = getImagesDir()
        self._imageList.Add (wx.Bitmap(os.path.join (imagesDir, "file_icon_default.png"),
                    wx.BITMAP_TYPE_ANY))
        self._imageList.Add (wx.Bitmap(os.path.join (imagesDir, "folder.png"),
                    wx.BITMAP_TYPE_ANY))


    def getFileImage (self, filepath):
        if self.imageListCount == 0:
            self.initialize()

        return self._getFileImage (filepath)


    @abstractmethod
    def _getFileImage (self, filepath):
        pass


    @property
    def imageList (self):
        return self._imageList


    def clear (self):
        self._imageList.RemoveAll()
        self._iconsDict = {}


    @property
    def imageListCount (self):
        """
        Используется для тестирования
        """
        return self._imageList.GetImageCount()


    @property
    def dictSize (self):
        """
        Используется для тестирования
        """
        return len (self._iconsDict)


class UnixFileIcons (BaseFileIcons):
    """
    Класс для получения иконок прикрепленных файлов под Unix (все иконки берутся из прилагающихся картинок)
    """
    def _getFileImage (self, filepath):
        """
        Возвращает номер картинки в imageList для файла по его расширению. При необходимости добавляет картинку в список
        """
        if os.path.isdir (filepath):
            return self.FOLDER_ICON

        filename = os.path.basename (filepath)

        elements = filename.rsplit (".", 1)
        if len (elements) < 2:
            return self.DEFAULT_FILE_ICON

        ext = elements[1].lower()

        if ext in self._iconsDict:
            return self._iconsDict[ext]

        bmp = self.__getSystemIcon (ext)

        if bmp == None:
            return self.DEFAULT_FILE_ICON

        index = self.imageList.Add (bmp)
        self._iconsDict[ext] = index

        return index


    def __getSystemIcon (self, ext):
        """
        Получить картинку по расширению или None, если такой картинки нет
        """
        iconfolder = "fileicons"
        from outwiker.core.system import getImagesDir
        iconpath = os.path.join (getImagesDir(), iconfolder)

        filename = u"file_extension_{}.png".format (ext)
        imagePath = os.path.join (iconpath, filename)

        if os.path.exists (imagePath):
            return wx.Bitmap (imagePath, wx.BITMAP_TYPE_ANY)

        return None



class WindowsFileIcons (BaseFileIcons):
    """
    Класс для получения иконок прикрепленных файлов под Windows
    """
    def __getExeIcon (self, filepath):
        """
        Возвращает картинку exe-шника
        """
        icon = wx.Icon(filepath, wx.BITMAP_TYPE_ICO, 16, 16)
        if not icon.Ok():
            return None

        bmp = wx.EmptyBitmap(16,16)
        bmp.CopyFromIcon(icon)
        bmp = bmp.ConvertToImage()
        bmp.Rescale(16,16)
        bmp = wx.BitmapFromImage(bmp)

        return bmp


    def __getSystemIcon (self, ext):
        """
        Возвращает картинку, связанную  расширением ext в системе. Если с расширением не связана картинка, возвращется None
        """
        filetype = wx.TheMimeTypesManager.GetFileTypeFromExtension(ext)
        if filetype == None:
            return None

        nntype = filetype.GetIconInfo()
        if nntype == None:
            return None

        icon = nntype[0]
        if not icon.Ok():
            return None

        bmp = wx.EmptyBitmap(16,16)
        bmp.CopyFromIcon(icon)
        bmp = bmp.ConvertToImage()
        bmp.Rescale(16,16)
        bmp = wx.BitmapFromImage(bmp)
        return bmp


    def _getFileImage (self, filepath):
        """
        Возвращает номер картинки в imageList для файла по его расширению. При необходимости добавляет картинку в список
        """
        if os.path.isdir (filepath):
            return self.FOLDER_ICON

        filename = os.path.basename (filepath)

        elements = filename.rsplit (".", 1)
        if len (elements) < 2:
            return self.DEFAULT_FILE_ICON

        ext = elements[1]

        # Поиск иконки по расширению
        if ext in self._iconsDict:
            return self._iconsDict[ext]

        # Поиск иконки по имени файла (используется для расширения .exe)
        if filepath in self._iconsDict:
            return self._iconsDict[filepath]

        if ext.lower() == "exe":
            bmp = self.__getExeIcon (filepath)
        else:
            bmp = self.__getSystemIcon (ext)

        if bmp == None:
            return self.DEFAULT_FILE_ICON

        index = self.imageList.Add (bmp)

        # Для всех расширений кроме .exe в качестве ключа испльзуется расширение
        # Для .exe используется полный путь до файла
        if ext.lower() != "exe":
            self._iconsDict[ext] = index
        else:
            self._iconsDict[filepath] = index

        return index
