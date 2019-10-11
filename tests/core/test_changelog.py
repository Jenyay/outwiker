from outwiker.core.version import Version
from outwiker.core.appinfo import ChangeLog, VersionInfo


def test_changelog_latestVersion_empty():
    changelog = ChangeLog([])
    assert changelog.latestVersion is None


def test_changelog_single():
    versions = [
        VersionInfo(Version(1, 0), None, [], []),
    ]
    changelog = ChangeLog(versions)

    assert changelog.latestVersion.version == Version(1, 0)


def test_changelog_two():
    versions = [
        VersionInfo(Version(1, 0), None, [], []),
        VersionInfo(Version(2, 0), None, [], []),
    ]
    changelog = ChangeLog(versions)

    assert changelog.latestVersion.version == Version(2, 0)


def test_changelog_mix_1():
    versions = [
        VersionInfo(Version(2, 1), None, [], []),
        VersionInfo(Version(1, 1), None, [], []),
        VersionInfo(Version(1, 0), None, [], []),
        VersionInfo(Version(2, 0), None, [], []),
    ]
    changelog = ChangeLog(versions)

    assert changelog.latestVersion.version == Version(2, 1)


def test_changelog_mix_2():
    versions = [
        VersionInfo(Version(2, 1), None, [], []),
        VersionInfo(Version(1, 1), None, [], []),
        VersionInfo(Version(1, 0), None, [], []),
        VersionInfo(Version(3, 0), None, [], []),
        VersionInfo(Version(2, 0), None, [], []),
    ]
    changelog = ChangeLog(versions)

    assert changelog.latestVersion.version == Version(3, 0)
