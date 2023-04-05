from pathlib import Path
from typing import Union

import outwiker.core.images as _images
import outwiker.core.iconmaker as _iconmaker


def isImage(fname: Union[Path, str]) -> bool:
    """
    If fname is image then the function return True. Otherwise - False.
    """
    return _images.isImage(fname)


def isSVG(fname: Union[Path, str]) -> bool:
    return _images.isSVG(fname)


def createIcon(fname_in, fname_out) -> None:
    return _iconmaker.IconMaker().create(fname_in, fname_out)
