from typing import Optional

import outwiker.app.gui.mainwindowtools as _tools


def getMainWindowTitle(application) -> str:
    return _tools.getMainWindowTitle(application)


def addStatusBarItem(name: str, width: int = -1, position: Optional[int] = None) -> None:
    return _tools.addStatusBarItem(name, width, position)


def setStatusText(item_name: str, text: str) -> None:
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    return _tools.setStatusText(item_name, text)


def showHideAttachPanel(application, visible: bool) -> None:
    return _tools.showHideAttachPanel(application, visible)


def showHideTagsPanel(application, visible: bool) -> None:
    return _tools.showHideTagsPanel(application, visible)


def showHideNotesTreePanel(application, visible: bool) -> None:
    return _tools.showHideNotesTreePanel(application, visible)
