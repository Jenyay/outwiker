__version__ = (3, 1, 0, 893)
__status__ = 'dev'
__api_version__ = (3, 890)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__