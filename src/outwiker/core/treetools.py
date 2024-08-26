# coding: utf-8

import logging
import os.path

from pathlib import Path
from typing import Union


from outwiker.api.core.defines import PAGE_RESULT_HTML
from outwiker.app.services.messages import showError
from outwiker.core.application import Application
from outwiker.core.tree import WikiDocument
from outwiker.core.notestreeloader import NotesTreeLoader
from outwiker.core.exceptions import ReadonlyException


logger = logging.getLogger("treetools")


def loadNotesTree(path: Union[str, Path], readonly: bool = False) -> WikiDocument:
    return NotesTreeLoader().loadNotesTree(str(path), readonly)


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
        except ReadonlyException as ex:
            if ex.page is not None:
                logger.debug("ReadonlyException for page: %s (%s)", ex.page.display_title, ex.page.title)
            else:
                logger.debug("ReadonlyException for unknown page: %s (%s)")

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


def findPage(application, page_id):
    """
    page_id - subpath of page or page UID.
    """
    if application.wikiroot is None or page_id is None:
        return None

    prefix = 'page://'

    if page_id.startswith(prefix):
        page_id = page_id[len(prefix):]
        return application.pageUidDepot[page_id]
    elif application.wikiroot[page_id] is not None:
        return application.wikiroot[page_id]
    else:
        return application.pageUidDepot[page_id]


def getPageHtmlPath(page):
    return os.path.join(page.path, PAGE_RESULT_HTML)
