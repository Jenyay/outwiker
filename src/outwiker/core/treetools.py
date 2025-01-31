# coding: utf-8

import logging
import os.path
import re
from typing import List

from pathlib import Path
from typing import Union

import wx

from outwiker.app.services.messages import showError
from outwiker.core.defines import PAGE_RESULT_HTML
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

            showError(wx.GetApp().getMainWindow(),
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


def getAlternativeTitle(title: str,
                        siblings: List[str],
                        substitution: str = '_',
                        template: str = '{title} ({number})') -> str:
    '''
    The function proposes the page title based on the user title.
    The function replace forbidden characters on the substitution symbol.

    title - original title for the page (with forbidden characters).
    siblings - list of the page titles on the same level.
    substitution - forbidden characters will be replaced to this string.
    template - format string for unique title.

    Return title for the new page.
    '''
    newtitle = title.strip()
    siblings_lower = [sibling.lower().strip() for sibling in siblings]

    # 1. Replace forbidden characters
    regexp = re.compile(r'[><|?*:"\\/#%]')
    newtitle = regexp.sub(substitution, newtitle)

    # 2. Check for special names
    if re.match(r'^\.+$', newtitle):
        newtitle = ''

    # 3. Replace dots at the end of the title
    dots_regexp = re.compile(r'(?P<dots>\.+)$')
    dots_match = dots_regexp.search(newtitle)
    if dots_match is not None:
        dots_count = len(dots_match.group('dots'))
        newtitle = newtitle[:-dots_count] + '_' * dots_count

    # 4. Replace double underline in the begin title
    if newtitle.startswith('__'):
        newtitle = '--' + newtitle[2:]

    # 5. Make unique title
    result = newtitle
    n = 1
    while (len(result.strip()) == 0 or
           result.lower() in siblings_lower):
        result = template.format(title=newtitle, number=n).strip()
        n += 1

    result = result.strip()
    return result
