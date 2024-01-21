from pathlib import Path
from typing import Union

from outwiker.core.defines import IMAGES_EXTENSIONS


def isImage(fname: Union[Path, str]) -> bool:
    """
    If fname is image then the function return True. Otherwise - False.
    """
    fnameLower = str(fname).lower()
    for extension in IMAGES_EXTENSIONS:
        if fnameLower.endswith('.' + extension):
            return True

    return False


def isSVG(fname: Union[Path, str]) -> bool:
    fnameLower = str(fname).lower()
    return fnameLower.endswith('.svg')


def convert_name_to_svg(fname: str) -> str:
    suffix_old = ".png"
    suffix_new = ".svg"

    if fname.endswith(suffix_old):
        return fname[: -len(suffix_old)] + suffix_new

    return fname
