# -*- coding: UTF-8 -*-

VERSION_OK = 0
OUTWIKER_MUST_BE_UPGRADED = 1
PLUGIN_MUST_BE_UPGRADED = 2


def checkVersion(packageversion, required):
    if packageversion[0] > required[0]:
        return PLUGIN_MUST_BE_UPGRADED

    if packageversion[0] < required[0]:
        return OUTWIKER_MUST_BE_UPGRADED

    if packageversion[1] < required[1]:
        return OUTWIKER_MUST_BE_UPGRADED

    return VERSION_OK


def checkVersionAny(packageversion, requiredlist):
    '''
    packageversion - current package version.
    requiredlist - list of the supported versions.
    '''
    if requiredlist is None or len(requiredlist) == 0:
        return VERSION_OK

    for required in requiredlist:
        result = checkVersion(packageversion, required)
        if result == VERSION_OK:
            return result

    return result


def checkAllPackagesVersions(packageversion_list, required_list_list):
    '''
    packageversion_list - list of the current packages versions.
    required_list_list - list of the list supported versions.
    length of the packageversion_list must be equal length of
    the required_list_list.
    '''
    for packageversion, requiredlist in zip(packageversion_list,
                                            required_list_list):
        result = checkVersionAny(packageversion, requiredlist)
        if result != VERSION_OK:
            return result

    return VERSION_OK
