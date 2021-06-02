__version__ = (3, 0, 1, 889)
__status__ = ''
__api_version__ = (3, 888)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__
