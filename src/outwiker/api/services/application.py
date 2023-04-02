from pathlib import Path
from typing import List, Union
import outwiker.app.services.application as _app
import outwiker.core.system as _system


def exit(application):
    return _app.exit(application)


def printCurrentPage(application):
    return _app.printCurrentPage(application)


def openInNewWindow(path, args=[]):
    """ Open wiki tree in the new OutWiker window
    """
    return _system.openInNewWindow(path, args)


def startFile(path: Union[str, Path]) -> None:
    return _system.getOS().startFile(path)


def getCurrentDir() -> str:
    return _system.getCurrentDir()


def getImagesDir() -> str:
    return _system.getImagesDir()


def getBuiltinImagePath(*relative_image_name: str) -> str:
    '''
    Return absolute path to image file from "images" directory
    '''
    return _system.getBuiltinImagePath(*relative_image_name)


def getTemplatesDir() -> str:
    return _system.getTemplatesDir()


def getExeFile() -> str:
    """
    Возвращает имя запускаемого файла
    """
    return _system.getExeFile()


def getPluginsDirList() -> List[str]:
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return _system.getPluginsDirList()


def getIconsDirList() -> List[str]:
    """
    Возвращает список директорий, где могут располагаться иконки для страниц
    """
    return _system.getIconsDirList()


def getStylesDirList() -> List[str]:
    """
    Возвращает список директорий, откуда должны грузиться плагины
    """
    return _system.getStylesDirList()


def getSpellDirList() -> List[str]:
    """
    Возвращает список директорий со словарями для проверки орфографии
    """
    return _system.getSpellDirList()


def getSpecialDirList(dirname) -> List[str]:
    return _system.getSpecialDirList(dirname)
