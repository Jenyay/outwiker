from pathlib import Path
from typing import Union
import outwiker.app.services.application as _app
import outwiker.core.system as _system


def exit(application):
    return _app.exit(application)


def printCurrentPage(application):
    return _app.printCurrentPage(application)


def openInNewWindow(path, args=[]):
    """ Open wiki tree in the new OutWiker window
    """
    return _system.openInNewWindow(path, args)


def startFile(path: Union[str, Path]) -> None:
    return _system.getOS().startFile(path)
