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


def checkVersionAny(packageversion, requiredList):
    if requiredList is None or len(requiredList) == 0:
        return VERSION_OK

    for required in requiredList:
        result = checkVersion(packageversion, required)
        if result == VERSION_OK:
            return result

    return result
