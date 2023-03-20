# -*- coding=utf-8 -*-

from pathlib import Path
from typing import Callable

from outwiker.core.images import isImage
from outwiker.core.attachment import Attachment


def getImagesOnlyFilter() -> Callable[[Path], bool]:
    return lambda path: not path.is_dir() and isImage(path)


def getDirOnlyFilter() -> Callable[[Path], bool]:
    return lambda path: path.is_dir()


def getHiddenFilter(page) -> Callable[[Path], bool]:
    '''
    Returns filter for skipping hidden directories (starts with "__")
    '''
    attach = Attachment(page)
    root_dir = attach.getAttachPath(create=False)
    return lambda path: path.is_dir() and str(path.relative_to(root_dir)).startswith('__')


def andFilter(*filter_list: Callable[[Path], bool]) -> Callable[[Path], bool]:
    def filter_func(path: Path) -> bool:
        result = True
        for func in filter_list:
            result = result and func(path)
            if not result:
                break

        return result

    return filter_func


def orFilter(*filter_list: Callable[[Path], bool]) -> Callable[[Path], bool]:
    def filter_func(path: Path) -> bool:
        result = False
        for func in filter_list:
            result = result or func(path)
            if result:
                break

        return result

    return filter_func


def notFilter(filter_func: Callable[[Path], bool]) -> Callable[[Path], bool]:
    return lambda path: not filter_func(path)


def getImageRecursiveFilter() -> Callable[[Path], bool]:
    return orFilter(getImagesOnlyFilter(), getDirOnlyFilter())


def getNotHiddenImageRecursiveFilter(page):
    return andFilter(getImageRecursiveFilter(),
                     notFilter(getHiddenFilter(page)))


def getNotHiddenDirOnlyFilter(page):
    return andFilter(getDirOnlyFilter(),
                     notFilter(getHiddenFilter(page)))
