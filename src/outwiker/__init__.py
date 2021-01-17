__version__ = (3, 0, 0, 880)
__status__ = 'dev'
__api_version__ = (3, 876)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__
