from pathlib import Path
from typing import Union

import outwiker.core.images as _images

from outwiker.pages.wiki.parser.pagethumbmaker import PageThumbmaker


def isImage(fname: Union[Path, str]) -> bool:
    """
    If fname is image then the function return True. Otherwise - False.
    """
    return _images.isImage(fname)


def isSVG(fname: Union[Path, str]) -> bool:
    return _images.isSVG(fname)
