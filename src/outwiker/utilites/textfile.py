# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Union


def readTextFile(fname: Union[str, Path]) -> str:
    """
    Read text content. Content must be in utf-8 encoding.
    The function return unicode object
    """
    with open(fname, "r", encoding="utf-8", errors='surrogatepass') as fp:
        return fp.read()


def writeTextFile(fname, text: str) -> None:
    """
    Write text with utf-8 encoding
    """
    with open(fname, "w", encoding="utf-8", errors='surrogatepass') as fp:
        fp.write(text)
