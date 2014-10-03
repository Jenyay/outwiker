# -*- coding: UTF-8 -*-

import re


def extractVersion (text):
    versionRegEx = re.compile (
        r"<!--\s*#version\s+(?P<key>\w+)\s+(?P<version>\d+(.\d+){0,3})\s*-->",
        re.IGNORECASE | re.MULTILINE | re.UNICODE)
    versionsDict = {}

    matches = versionRegEx.finditer (text)
    for match in matches:
        versionsDict[match.group ("key")] = match.group ("version")

    return versionsDict
