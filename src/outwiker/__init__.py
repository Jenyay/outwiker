__version__ = (3, 2, 0, 926)
__status__ = ''
__api_version__ = (3, 924)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__