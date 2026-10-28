# -*- coding: utf-8 -*-

from typing import Optional

from outwiker.app.gui.dialogs.bookmarksdialog import BookmarksDialog, BookmarksDialogController
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

    dlg = BookmarksDialog(application.mainWindow, application.theme)
    dlg_controller = BookmarksDialogController(dlg)
    dlg_controller.set_bookmark_list([page for page in application.bookmarks if page is not None])
    dlg_controller.show()
