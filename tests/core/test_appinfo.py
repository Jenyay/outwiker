# -*- coding: utf-8 -*-

from outwiker.core.version import Version
from outwiker.core.appinfo import AppInfo, VersionInfo


def test_currentVersion_empty():
    appinfo = AppInfo()
    assert appinfo.currentVersion is None


def test_currentVersion_single():
    versions = [VersionInfo(Version(1, 0), None, [], [])]
    appinfo = AppInfo(versions=versions)

    assert appinfo.currentVersion == Version(1, 0)


def test_currentVersion_min_max():
    versions = [
        VersionInfo(Version(1, 0), None, [], []),
        VersionInfo(Version(2, 0), None, [], []),
    ]
    appinfo = AppInfo(versions=versions)

    assert appinfo.currentVersion == Version(2, 0)


def test_currentVersion_max_min():
    versions = [
        VersionInfo(Version(2, 0), None, [], []),
        VersionInfo(Version(1, 0), None, [], []),
    ]
    appinfo = AppInfo(versions=versions)

    assert appinfo.currentVersion == Version(2, 0)
