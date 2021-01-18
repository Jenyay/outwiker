# -*- coding: utf-8 -*-

from typing import List

VERSION_OK = 0
OUTWIKER_MUST_BE_UPGRADED = 1
PLUGIN_MUST_BE_UPGRADED = 2


def checkSingleVersion(current_api_version: List[int],
                       required_version: List[int]) -> int:
    if current_api_version[0] > required_version[0]:
        return PLUGIN_MUST_BE_UPGRADED

    if current_api_version[0] < required_version[0]:
        return OUTWIKER_MUST_BE_UPGRADED

    if current_api_version[1] < required_version[1]:
        return OUTWIKER_MUST_BE_UPGRADED

    return VERSION_OK


def checkVersion(current_api_version: List[int],
                 requiredlist: List[List[int]]) -> int:
    """
    current_api_version - current package version.
    requiredlist - list of the supported versions.
    """
    if requiredlist is None or len(requiredlist) == 0:
        return VERSION_OK

    for required in requiredlist:
        result = checkSingleVersion(current_api_version, required)
        if result == VERSION_OK:
            return result

    return result
