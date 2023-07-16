# -*- coding: utf-8 -*-

import os.path
from typing import Optional

from outwiker.core.application import Application


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


def addStatusBarItem(name: str, width: int = -1, position: Optional[int] = None) -> None:
    if Application.mainWindow:
        Application.mainWindow.statusbar.addItem(name, width, position)


def setStatusText(item_name: str, text: str) -> None:
    """
    Установить текст статусбара.
    text - текст
    index - номер ячейки статусбара
    """
    if Application.mainWindow:
        Application.mainWindow.statusbar.setStatusText(item_name, text)


def _showHideMainPanel(application, panel, visible):
    if visible:
        panel.pane.Show()
    else:
        panel.pane.Hide()

    application.mainWindow.auiManager.Update()


def showHideAttachPanel(application, visible):
    _showHideMainPanel(application, application.mainWindow.attachPanel, visible)


def showHideTagsPanel(application, visible):
    _showHideMainPanel(application, application.mainWindow.tagsCloudPanel, visible)


def showHideNotesTreePanel(application, visible):
    _showHideMainPanel(application, application.mainWindow.treePanel, visible)
