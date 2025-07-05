__version__ = (4, 0, 0, 952)
__status__ = 'alpha'
__api_version__ = (4, 951)

__version_str__ = ".".join([str(n) for n in __version__])


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__