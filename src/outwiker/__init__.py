__version__ = (3, 3, 0, 938)
__status__ = 'beta'
__api_version__ = (3, 934)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__