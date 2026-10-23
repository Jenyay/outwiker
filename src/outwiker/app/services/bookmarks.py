# -*- coding: utf-8 -*-

from typing import Optional

from outwiker.app.gui.dialogs.bookmarksdialog import BookmarksDialog
from outwiker.core.application import Application


def toggleBookmarkForCurrentPage(application: Application) -> Optional[bool]:
    selected_page = application.selectedPage

    if selected_page is None:
        return None

    bookmarks = application.bookmarks

    if bookmarks.pageMarked(selected_page):
        bookmarks.remove(selected_page)
        return False
    else:
        bookmarks.add(selected_page)
        return True


def showBookmarkManagementDialog(application: Application):
    if application.mainWindow is None:
        return

    with BookmarksDialog(application.mainWindow, application.theme) as dlg:
        dlg.ShowModal()
