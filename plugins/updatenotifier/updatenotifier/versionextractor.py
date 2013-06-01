#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re


class VersionExtractor (object):
    """
    Класс для получения версий по содержимому страницы сайта
    """
    def __init__ (self):
        self._versionRegEx = re.compile (
                r"<!--\s*#version\s+(?P<key>\w+)\s+(?P<version>\d+(.\d+){0,3})\s*-->",
                re.IGNORECASE | re.MULTILINE | re.UNICODE)


    def getVersions (self, text):
        versionsDict = {}

        matches = self._versionRegEx.finditer (text)
        for match in matches:
            versionsDict[match.group ("key")] = match.group ("version")

        return versionsDict

