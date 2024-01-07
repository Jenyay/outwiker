# -*- coding: utf-8 -*-

import os.path
from abc import abstractmethod, ABCMeta

import wx

from outwiker.gui.controls.safeimagelist import SafeImageList


class BaseFileIcons(metaclass=ABCMeta):
    """
    Базовый класс для получения иконок прикрепленных файлов
    """

    def __init__(self, scale: int = 1):
        self.DEFAULT_FILE_ICON = 0
        self.FOLDER_ICON = 1
        self.GO_TO_PARENT_ICON = 2

        self._width = 16 * scale
        self._height = 16 * scale

        self._imageList = SafeImageList(self._width, self._height)

        # Ключ - расширение файла, значение - номер иконки в self._imageList
        self._iconsDict = {}

    def initialize(self):
        from outwiker.core.system import getBuiltinImagePath

        self._imageList.Add(wx.Bitmap(getBuiltinImagePath(
            "file_icon_default.png"), wx.BITMAP_TYPE_ANY))

        self._imageList.Add(
            wx.Bitmap(getBuiltinImagePath("folder.svg"), wx.BITMAP_TYPE_ANY))

        self._imageList.Add(
            wx.Bitmap(getBuiltinImagePath("arrow_go_to_parent.png"), wx.BITMAP_TYPE_ANY))

    def getFileImage(self, filepath):
        if self.imageListCount == 0:
            self.initialize()

        return self._getFileImage(filepath)

    @abstractmethod
    def _getFileImage(self, filepath):
        pass

    @property
    def imageList(self):
        if self.imageListCount == 0:
            self.initialize()

        return self._imageList

    def clear(self):
        self._imageList.RemoveAll()
        self._iconsDict = {}

    @property
    def imageListCount(self):
        """
        Используется для тестирования
        """
        return self._imageList.GetImageCount()

    @property
    def dictSize(self):
        """
        Используется для тестирования
        """
        return len(self._iconsDict)


class UnixFileIcons(BaseFileIcons):
    """
    Класс для получения иконок прикрепленных
    файлов под Unix(все иконки берутся из прилагающихся картинок)
    """

    def _getFileImage(self, filepath):
        """
        Возвращает номер картинки в imageList для файла по его расширению.
        При необходимости добавляет картинку в список
        """
        if os.path.isdir(filepath):
            return self.FOLDER_ICON

        filename = os.path.basename(filepath)

        elements = filename.rsplit(".", 1)
        if len(elements) < 2:
            return self.DEFAULT_FILE_ICON

        ext = elements[1].lower()

        if ext in self._iconsDict:
            return self._iconsDict[ext]

        bmp = self._getSystemIcon(ext)

        if bmp is None:
            return self.DEFAULT_FILE_ICON

        index = self.imageList.Add(bmp)
        self._iconsDict[ext] = index

        return index

    def _getSystemIcon(self, ext):
        """
        Получить картинку по расширению или None, если такой картинки нет
        """
        from outwiker.core.system import getBuiltinImagePath
        iconfolder = "fileicons"
        filename = u"file_extension_{}.png".format(ext)

        imagePath = getBuiltinImagePath(iconfolder, filename)

        if os.path.exists(imagePath):
            return wx.Bitmap(imagePath, wx.BITMAP_TYPE_ANY)

        return None


class WindowsFileIcons(BaseFileIcons):
    """
    Класс для получения иконок прикрепленных файлов под Windows
    """

    def _loadFromResource(self, filepath):
        """
        Возвращает картинку exe-шника
        """
        icon = wx.Icon(filepath, wx.BITMAP_TYPE_ICO, self._width, self._height)
        if not icon.IsOk():
            return None

        bmp = wx.Bitmap(self._width, self._height)
        bmp.CopyFromIcon(icon)
        bmp = bmp.ConvertToImage()
        bmp.Rescale(self._width, self._height)
        bmp = wx.Bitmap(bmp)

        return bmp

    def _getSystemIcon(self, ext):
        """
        Возвращает картинку, связанную  расширением ext в системе.
        Если с расширением не связана картинка, возвращется None
        """
        filetype = wx.TheMimeTypesManager.GetFileTypeFromExtension(ext)
        if filetype is None:
            return None

        nntype = filetype.GetIconInfo()
        if nntype is None:
            return None

        fname = nntype[1]
        index = nntype[2]
        return self._loadFromResource('{};{}'.format(fname, index))

    def _getFileImage(self, filepath):
        """
        Возвращает номер картинки в imageList для файла по его расширению.
        При необходимости добавляет картинку в список
        """
        if os.path.isdir(filepath):
            return self.FOLDER_ICON

        filename = os.path.basename(filepath)

        elements = filename.rsplit(".", 1)
        if len(elements) < 2:
            return self.DEFAULT_FILE_ICON

        ext = elements[1]

        # Поиск иконки по расширению
        if ext in self._iconsDict:
            return self._iconsDict[ext]

        # Поиск иконки по имени файла(используется для расширения .exe)
        if filepath in self._iconsDict:
            return self._iconsDict[filepath]

        if ext.lower() == "exe":
            bmp = self._loadFromResource(filepath)
        else:
            bmp = self._getSystemIcon(ext)

        if bmp is None:
            return self.DEFAULT_FILE_ICON

        index = self.imageList.Add(bmp)

        # Для всех расширений кроме .exe в качестве ключа
        # испльзуется расширение файла
        # Для .exe используется полный путь до файла
        if ext.lower() != "exe":
            self._iconsDict[ext] = index
        else:
            self._iconsDict[filepath] = index

        return index
