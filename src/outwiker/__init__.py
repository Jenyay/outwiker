__version__ = (3, 2, 0, 914)
__status__ = 'beta'
__api_version__ = (3, 910)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__