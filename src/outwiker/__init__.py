__version__ = (3, 2, 0, 919)
__status__ = 'dev'
__api_version__ = (3, 918)


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__