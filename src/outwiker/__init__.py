__version__ = (4, 1, 0, 978)
__status__ = 'beta'
__api_version__ = (4, 972)

__version_str__ = ".".join([str(n) for n in __version__])


def getVersionStr() -> str:
    return '.'.join([str(item) for item in __version__]) + ' ' + __status__