from pathlib import Path
from typing import Any, Dict, Union

import outwiker.core.text as _text
import outwiker.utilites.textfile as _textfile


def dictToStr(paramsDict: Dict[str, Any]) -> str:
    return _text.dictToStr(paramsDict)


def readTextFile(fname: Union[str, Path]) -> str:
    """
    Read text content. Content must be in utf-8 encoding.
    The function return unicode object
    """
    return _textfile.readTextFile(fname)


def writeTextFile(fname, text: str) -> None:
    """
    Write text with utf-8 encoding
    """
    return _textfile.writeTextFile(fname, text)
