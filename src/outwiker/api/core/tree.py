# coding: utf-8

import os.path

from pathlib import Path
from typing import Union


from outwiker.api.services.messages import showError
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.exceptions import ReadonlyException


def loadNotesTree(path: Union[str, Path], readonly: bool = False) -> WikiDocument:
    return WikiDocument.load(str(path), readonly)


def createNotesTree(path: Union[str, Path]) -> WikiDocument:
    return WikiDocument.create(str(path))


def closeWiki(application):
    application.wikiroot = None


def pageExists(page) -> bool:
    """
    Проверка на то, что страница была удалена сторонними средствами
    """
    return page is not None and os.path.exists(page.path)


def testreadonly(func):
    """
    Декоратор для отлавливания исключения
        outwiker.core.exceptions.ReadonlyException
    """
    def readOnlyWrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ReadonlyException:
            showError(Application.mainWindow,
                      _("Page is opened as read-only"))

    return readOnlyWrap


@testreadonly
def generateLink(application, page):
    """
    Создать ссылку на страницу по UID
    """
    uid = application.pageUidDepot.createUid(page)
    return "page://{}".format(uid)
