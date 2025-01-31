from typing import Optional

from outwiker.gui.mainpanes.mainpane import MainPane

import outwiker.app.gui.mainwindowtools as _tools


def getMainWindowTitle(application) -> str:
    return _tools.getMainWindowTitle(application)


def addStatusBarItem(mainWindow, name: str, width: int = -1, position: Optional[int] = None) -> None:
    return _tools.addStatusBarItem(mainWindow, name, width, position)


def setStatusText(mainWindow, item_name: str, text: str) -> None:
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    return _tools.setStatusText(mainWindow, item_name, text)


def showHideAttachPanel(mainWindow, visible: bool) -> None:
    return _tools.showHideAttachPanel(mainWindow, visible)


def showHideTagsPanel(mainWindow, visible: bool) -> None:
    return _tools.showHideTagsPanel(mainWindow, visible)


def showHideNotesTreePanel(mainWindow, visible: bool) -> None:
    return _tools.showHideNotesTreePanel(mainWindow, visible)
