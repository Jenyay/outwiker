from typing import Optional

import wx

import outwiker.app.services.tree as _tree
from outwiker.api.core import Application
from outwiker.core.tree import WikiDocument, WikiPage


def removePage(page: WikiPage) -> None:
    return _tree.removePage(page)


def openWikiWithDialog(parent: wx.Window, application: Application, readonly=False) -> Optional[WikiDocument]:
    """
    Показать диалог открытия вики и вернуть открытую wiki
    parent -- родительское окно
    """
    return _tree.openWikiWithDialog(parent, application, readonly)


def openWiki(path: str, application: Application, readonly: bool = False) -> Optional[WikiDocument]:
    return _tree.openWiki(path, application, readonly)


def testPageTitle(title) -> bool:
    """
    Возвращает True, если можно создавать страницу с таким заголовком в текущей ОС
    """
    return _tree.testPageTitle(title)


def testPageTitleWindows(title) -> bool:
    """
    Возвращает True, если можно создавать страницу с таким заголовком в Windows
    """
    return _tree.testPageTitleWindows(title)


def testPageTitleLinux(title) -> bool:
    """
    Возвращает True, если можно создавать страницу с таким заголовком в Linux
    """
    return _tree.testPageTitleLinux(title)


def replaceTitleDangerousSymbols(title: str, replacement: str) -> str:
    """Replace dangerous symbols by 'replacement'"""
    return _tree.replaceTitleDangerousSymbols(title, replacement)


def renamePage(page, newtitle) -> None:
    return _tree.renamePage(page, newtitle)


def movePage(page, newParent) -> None:
    """
    Сделать страницу page ребенком newParent
    """
    return _tree.movePage(page, newParent)


def createNewWiki(parentwnd: wx.Window, application: Application):
    """
    Создать новую вики
    parentwnd - окно-владелец диалога выбора файла
    """
    return _tree.createNewWiki(parentwnd, application)
