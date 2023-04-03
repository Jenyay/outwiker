from typing import Optional

import outwiker.app.services.bookmarks as _bookmarks


def toggleBookmarkForCurrentPage(application) -> Optional[bool]:
    return _bookmarks.toggleBookmarkForCurrentPage(application)
