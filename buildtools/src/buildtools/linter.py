'''
Tools to check errors in OutWiker information
'''
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


class Linter:
    def get_sum_status(self, reports: List[LinterReport]) -> LinterStatus:
        sum_status = LinterStatus.OK
        for report in reports:
            sum_status = sum_status & report.status

        return (sum_status, reports)


class LinterForOutWiker(Linter):
    '''
    Errors checker for OutWiker information
    '''

    def check_all(self, versions_xml: str) -> Tuple[LinterStatus, List[LinterReport]]:
        checkers = [
            self.check_versions_list,
            self.check_release_date,
            self.check_even_versions,
        ]

        sum_report = []

        # Run all checkers
        for checker in checkers:
            current_report = checker(versions_xml)
            sum_report += current_report

        # Calculate overall status
        sum_status = self.get_sum_status(sum_report)

        return (sum_status, sum_report)

    def check_release_date(self, versions_xml: str) -> List[LinterReport]:
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

    def check_versions_list(self, versions_xml: str) -> List[LinterReport]:
        '''
        Check that the versions is not empty
        '''
        reports = []

        changelog = XmlChangelogParser.parse(versions_xml)
        if not changelog.versions:
            reports.append(LinterReport(LinterStatus.ERROR,
                                        'No versions list for OutWiker'))

        return reports

    def check_even_versions(self, versions_xml: str) -> List[LinterReport]:
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
                    LinterReport(LinterStatus.ERROR, 'Invalid version format: {}'.format(version.number)))
                continue

            if build % 2 != 0:
                reports.append(
                    LinterReport(LinterStatus.ERROR, 'Build number for version {} is odd (dev version)'.format(version.number)))

        return reports
