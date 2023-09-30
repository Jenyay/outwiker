__version__ = (3, 3, 0, 929)
__status__ = 'dev'
__api_version__ = (3, 928)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__