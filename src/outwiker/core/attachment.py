# -*- coding: utf-8 -*-

import os
import os.path
import shutil
from pathlib import Path
from typing import Union, List

from .defines import PAGE_ATTACH_DIR
from .exceptions import ReadonlyException
from .events import AttachListChangedParams


class Attachment:
    """
    Класс для работы с прикрепленными файлами
    """

    def __init__(self, page):
        """
        page - страница, для которой интересуют прикрепленные файлы
        """
        self.page = page

    def getAttachPath(self, create: bool = False) -> str:
        """
        Возвращает путь до папки с прикрепленными файлами
        create - создать папку для прикрепленных файлов,
        если она еще не создана?
        """
        path = os.path.join(self.page.path, PAGE_ATTACH_DIR)

        if create and not os.path.exists(path):
            os.mkdir(path)

        return path

    @property
    def attachmentFull(self) -> List[str]:
        """
        Возвращает список прикрепленных файлов.
        Пути до файлов полные
        """
        return self.getAttachFull()

    def getAttachFull(self, subdir: str = ".") -> List[str]:
        """
        Возвращает список прикрепленных файлов.
        Пути до файлов полные
        """
        path = self.getAttachPath()
        return [os.path.normpath(os.path.join(path, subdir, fname))
                for fname in self.getAttachRelative(subdir)]

    def createSubdir(self, subdir: Union[str, Path]) -> Path:
        if self.page.readonly:
            raise ReadonlyException

        root = Path(self.getAttachPath(create=True)).resolve()
        subdir_path = (root / subdir).resolve()
        if root == subdir_path:
            return root

        if root not in subdir_path.parents:
            raise OSError

        subdir_path.mkdir(parents=True, exist_ok=True)
        return subdir_path

    def getAttachRelative(self, subdir="."):
        """
        Возвращает список прикрепленных файлов
        (только имена файлов без путей относительно директории subdir).
        subdir - поддиректория в PAGE_ATTACH_DIR,
        где хотим получить список файлов
        """
        path = self.getAttachPath()

        if not os.path.exists(path):
            return []

        fullpath = os.path.join(path, subdir)

        return os.listdir(fullpath)

    def attach(self, files: List[Union[Path, str]], subdir: Union[Path, str] = '.') -> None:
        """
        Прикрепить файлы к странице
        files -- список файлов (или папок), которые надо прикрепить
        subdir -- вложенная директория в папку __attach
        """
        if self.page.readonly:
            raise ReadonlyException

        subdir_path = self.createSubdir(subdir)

        if not subdir_path.exists() or not subdir_path.is_dir():
            raise OSError

        for name in files:
            name_path = Path(name)
            if name_path.is_dir():
                basename = name_path.name
                shutil.copytree(name, subdir_path / basename)
            else:
                shutil.copy(name, subdir_path)

        self.page.updateDateTime()
        self.page.root.onAttachListChanged(self.page,
                                           AttachListChangedParams())

    def removeAttach(self, files):
        """
        Удалить прикрепленные файлы
        files - список имен файлов (путей относительно папки PAGE_ATTACH_DIR)
        """
        if self.page.readonly:
            raise ReadonlyException

        attachPath = self.getAttachPath(True)

        for fname in files:
            path = os.path.join(attachPath, fname)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
            except OSError:
                self.page.root.onAttachListChanged(self.page,
                                                   AttachListChangedParams())
                raise IOError(u"Can't remove %s" % fname)

        self.page.updateDateTime()
        self.page.root.onAttachListChanged(self.page,
                                           AttachListChangedParams())

    def fixCurrentSubdir(self):
        """
        Fix invalid attachment current subdir for the page.
        Returns absolute path to attachment fixed directory
        or None if __attach is not created.
        """
        root = os.path.abspath(self.getAttachPath(create=False))

        # Check if root attach directory exists
        if not self._dirExists(root):
            if self.page.currentAttachSubdir != '.':
                self.page.currentAttachSubdir = None
            return None

        current_subdir = self.page.currentAttachSubdir
        current_path = os.path.join(root, current_subdir)

        # Check if current attach subdir exists
        if self._dirExists(current_path):
            return current_path

        # Find first existed parent directory
        while current_subdir != '':
            if self._dirExists(os.path.join(root, current_subdir)):
                break
            current_subdir = os.path.dirname(current_subdir)

        # Walk to parent?
        if current_subdir == '':
            current_subdir = None

        # Current page must be fixed
        self.page.currentAttachSubdir = current_subdir
        return os.path.join(root, self.page.currentAttachSubdir)

    def _dirExists(self, path):
        return os.path.exists(path) and os.path.isdir(path)

    @staticmethod
    def sortByName(fname):
        """
        Deprecated. Please use kye=str.lower instead.

        Метод для сортировки файлов по имени
        Key stile method to sort files by name.

        Args:
            fname: path to the file.
        Returns:
            fname.lower()
        """
        return fname.lower()

    @staticmethod
    def sortByType(fname):
        NOT_EXISTS = 0
        IS_FILE = 1
        IS_DIR = 2

        if not os.path.exists(fname):
            return NOT_EXISTS
        if os.path.isdir(fname):
            return IS_DIR

        return IS_FILE

    @staticmethod
    def sortByExt(fname):
        """
        Метод для сортировки файлов по расширению
        Key stile method to sort files by extension.
        If the extension is equivalent for 2 files they will be sorted by name.

        Args:
            fname: path to the file.
        Returns:
            (file_ext, file_name)
        """
        name, ext = os.path.splitext(os.path.basename(fname).lower())

        return ext, name

    @staticmethod
    def sortByDate(full_file_path):
        """
        Метод для сортировки файлов по дате последней модификации.
        Key stile method to sort files by last modified date.
        If the date is equivalent for 2 files they will be sorted by name.

        Args:
            full_file_path: full path to the existing file.
        Returns:
            (os.stat().st_mtimem, full_file_path.lower())
        """
        stat = os.stat(full_file_path)

        return stat.st_mtime, full_file_path.lower()

    @staticmethod
    def sortBySize(full_file_path):
        """
        Метод для сортировки файлов по размеру файла.
        Key stile method to sort files by file size.
        If the size is equivalent for 2 files they will be sorted by name.

        Args:
            full_file_path: full path to the existing file.
        Returns:
            (os.stat().st_mtimem, full_file_path.lower())
        """
        stat = os.stat(full_file_path)

        return stat.st_size, full_file_path.lower()

    def sortBySizeRelative(self, relative_file_path):
        """
        Метод для сортировки файлов по размеру файла.
        Key stile method to sort files by file size.
        If the size is equivalent for 2 files they will be sorted by name.

        Args:
            relative_file_path: relative path to the file.
        Returns:
            (os.stat().st_mtimem, relative_file_path.lower())
        """
        stat = os.stat(self.getFullPath(relative_file_path))

        return stat.st_size, relative_file_path.lower()

    def sortByDateRelative(self, relative_file_path):
        """
        Метод для сортировки файлов по дате.
        Key stile method to sort files by last modified date.
        If the date is equivalent for 2 files they will be sorted by name.

        Args:
            relative_file_path: relative path to the file.
        Returns:
            (os.stat().st_mtimem, relative_file_path.lower())
        """
        stat = os.stat(self.getFullPath(relative_file_path))

        return stat.st_mtime, relative_file_path.lower()

    def getFullPath(self, fname, create=False):
        """
        Возвращает полный путь до прикрепленного файла с именем fname.
        Файл fname не обязательно должен существовать.
        create - нужно ли создавать папку PAGE_ATTACH_DIR,
        если ее еще не существует?
        """
        return os.path.join(self.getAttachPath(create), fname)

    def query(self, mask: str) -> List[str]:
        mask = mask.replace('\\', '/').strip()
        if len(mask) == 0:
            return []

        if mask.find('..') != -1:
            return []

        if mask.startswith('/'):
            return []


        root_dir = Path(self.getAttachPath(create=False))
        if not root_dir.exists():
            return []

        glob_result = root_dir.glob(mask)

        return [str(fname.relative_to(root_dir)).replace('\\', '/')
                for fname in glob_result]

    def exists(self, fname: Union[Path, str], subdir: Union[Path, str] = '.') -> bool:
        return Path(self.getAttachPath(), subdir, fname).exists()
