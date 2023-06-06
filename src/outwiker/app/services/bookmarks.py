# -*- coding: utf-8 -*-

from typing import Optional


def toggleBookmarkForCurrentPage(application) -> Optional[bool]:
    selected_page = application.selectedPage

    if selected_page is None:
        return None

    wikiroot = application.wikiroot

    if wikiroot.bookmarks.pageMarked(selected_page):
        wikiroot.bookmarks.remove(selected_page)
        return False
    else:
        wikiroot.bookmarks.add(selected_page)
        return True

