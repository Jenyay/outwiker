'''
Tools to check errors in OutWiker information
'''
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from typing import Tuple, List

from outwiker.core.xmlchangelogparser import XmlChangelogParser


class LinterStatus(IntEnum):
    OK = 0
    WARNING = 1
    ERROR = 2

    def __and__(self, other: 'LinterStatus') -> 'LinterStatus':
        return max(self, other)


class LinterReport:
    '''
    Status + Message
    '''

    def __init__(self, status: LinterStatus, message: str):
        self.status = status
        self.message = message


class Linter(metaclass=ABCMeta):
    @abstractmethod
    def get_checkers(self):
        pass

    def get_sum_status(self, reports: List[LinterReport]) -> LinterStatus:
        sum_status = LinterStatus.OK
        for report in reports:
            sum_status = sum_status & report.status

        return sum_status

    def check_all(self, versions_xml: str) -> Tuple[LinterStatus, List[LinterReport]]:
        checkers = self.get_checkers()

        sum_report = []

        # Run all checkers
        for checker in checkers:
            current_report = checker(versions_xml)
            sum_report += current_report

        # Calculate overall status
        sum_status = self.get_sum_status(sum_report)

        return (sum_status, sum_report)


class LinterForOutWiker(Linter):
    '''
    Errors checker for OutWiker information
    '''

    def get_checkers(self):
        return [
            check_versions_list,
            check_release_date,
            check_even_versions,
            check_changelog_list,
        ]


class LinterForPlugin(Linter):
    '''
    Errors checker for Plug-in information
    '''

    def get_checkers(self):
        return [
            check_versions_list,
            check_release_date,
            check_download_plugin_url,
            check_changelog_list,
        ]


def check_release_date(versions_xml: str) -> List[LinterReport]:
    '''
    Check that the date is set
    '''
    reports = []

    changelog = XmlChangelogParser.parse(versions_xml)
    for version in changelog.versions:
        if version.date is None:
            reports.append(LinterReport(LinterStatus.ERROR,
                                        'No release date for OutWiker'))

    return reports


def check_versions_list(versions_xml: str) -> List[LinterReport]:
    '''
    Check that the versions is not empty
    '''
    reports = []

    changelog = XmlChangelogParser.parse(versions_xml)
    if not changelog.versions:
        reports.append(LinterReport(LinterStatus.ERROR,
                                    'No versions list for OutWiker'))

    return reports


def check_even_versions(versions_xml: str) -> List[LinterReport]:
    '''
    Check that the date is set
    '''
    reports = []

    changelog = XmlChangelogParser.parse(versions_xml)
    for version in changelog.versions:
        try:
            build = int(version.number.split('.')[3])
        except (ValueError, IndexError):
            reports.append(
                LinterReport(LinterStatus.ERROR,
                             'Invalid version format: {}'.format(version.number)))
            continue

        if build % 2 != 0:
            reports.append(
                LinterReport(LinterStatus.ERROR,
                             'Build number for version {} is odd (dev version)'.format(version.number)))

    return reports


def check_download_plugin_url(versions_xml: str) -> List[LinterReport]:
    '''
    Check version number in URL for download
    '''
    reports = []

    archive_extension = '.zip'

    changelog = XmlChangelogParser.parse(versions_xml)
    for version in changelog.versions:
        if not version.downloads:
            reports.append(
                LinterReport(LinterStatus.ERROR,
                             'Empty download list for version {}'.format(version.number)))
            continue

        for download in version.downloads:
            if not download.href.endswith(archive_extension):
                reports.append(
                    LinterReport(LinterStatus.ERROR,
                                 'Invalid archive format for version {}: {}'.format(version.number, download.href)))
                continue

            if not download.href[:-len(archive_extension)].endswith(version.number):
                reports.append(
                    LinterReport(LinterStatus.ERROR,
                                 'Invalid file name for version {}: {}'.format(version.number, download.href)))
                continue

    return reports


def check_changelog_list(versions_xml: str) -> List[LinterReport]:
    '''
    Compare chages for Russian and English languages
    '''
    reports = []

    changelog = XmlChangelogParser.parse(versions_xml)
    for version in changelog.versions:
        changes_ru = version.changes.get('ru')
        changes_en = version.changes.get('')

        if not changes_ru:
            reports.append(
                LinterReport(LinterStatus.ERROR,
                             'Empty Russian changelog for version {}'.format(version.number)))
            continue

        if not changes_en:
            reports.append(
                LinterReport(LinterStatus.ERROR,
                             'Empty English changelog for version {}'.format(version.number)))
            continue

        if len(changes_ru) != len(changes_en):
            reports.append(
                LinterReport(LinterStatus.ERROR,
                             'Changelog for English and Russian versions are not equal for version {}'.format(version.number)))

    return reports
