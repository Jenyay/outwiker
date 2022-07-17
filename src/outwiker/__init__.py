__version__ = (3, 2, 0, 908)
__status__ = 'beta'
__api_version__ = (3, 906)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__