from pathlib import Path
from typing import Any, Dict, Union

import outwiker.core.text as _text
import outwiker.utilites.textfile as _textfile
import outwiker.utilites.text as _textutils


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


def find_all(text: str, sub: str, start=0, end=None):
    return _textutils.find_all(text, sub, start, end)


def positionInside(text: str,
                   position: int,
                   open_str: str,
                   close_str: str) -> bool:
    '''
    Return true if position located between open_str and close_str strings
    '''
    return _textutils.positionInside(text, position, open_str, close_str)
