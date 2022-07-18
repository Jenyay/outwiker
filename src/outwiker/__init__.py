__version__ = (3, 2, 0, 909)
__status__ = 'dev'
__api_version__ = (3, 906)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__