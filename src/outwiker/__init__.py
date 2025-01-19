__version__ = (4, 0, 0, 950)
__status__ = 'alpha'
__api_version__ = (4, 950)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__