# -*- coding: utf-8 -*-

import os.path
from typing import Optional


def getMainWindowTitle(application):
    template = application.mainWindow.mainWindowConfig.titleFormat.value

    if application.wikiroot is None:
        result = "OutWiker"
    else:
        page = application.wikiroot.selectedPage

        pageTitle = "" if page is None else page.display_title
        subpath = "" if page is None else page.display_subpath
        filename = os.path.basename(application.wikiroot.path)

        result = (template
                  .replace("{file}", filename)
                  .replace("{page}", pageTitle)
                  .replace("{subpath}", subpath)
                  )

    return result


def addStatusBarItem(mainWindow, name: str, width: int = -1, position: Optional[int] = None) -> None:
    if mainWindow:
        mainWindow.statusbar.addItem(name, width, position)


def setStatusText(mainWindow, item_name: str, text: str) -> None:
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    if mainWindow:
        mainWindow.statusbar.setStatusText(item_name, text)


def _showHideMainPanel(mainWindow, panel, visible):
    if visible:
        panel.pane.Show()
    else:
        panel.pane.Hide()

    mainWindow.auiManager.Update()


def showHideAttachPanel(mainWindow, visible):
    _showHideMainPanel(mainWindow, mainWindow.attachPanel, visible)


def showHideTagsPanel(mainWindow, visible):
    _showHideMainPanel(mainWindow, mainWindow.tagsCloudPanel, visible)


def showHideNotesTreePanel(mainWindow, visible):
    _showHideMainPanel(mainWindow, mainWindow.treePanel, visible)
