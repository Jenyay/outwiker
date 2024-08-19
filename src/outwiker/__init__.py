__version__ = (3, 3, 0, 940)
__status__ = ''
__api_version__ = (3, 934)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__