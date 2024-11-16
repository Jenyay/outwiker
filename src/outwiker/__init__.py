__version__ = (4, 0, 0, 944)
__status__ = 'alpha'
__api_version__ = (4, 944)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__