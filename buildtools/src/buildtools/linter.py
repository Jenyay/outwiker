'''
Tools to check errors in OutWiker information
'''
from enum import IntEnum
from typing import Tuple

from outwiker.core.xmlchangelogparser import XmlChangelogParser

from colorama import Fore


class LinterResult(IntEnum):
    OK = 0
    WARNING = 1
    ERROR = 2

    def __and__(self, other: 'LinterResult') -> 'LinterResult':
        return max(self, other)


class Linter:
    def __init__(self):
        self._fores = [Fore.GREEN, Fore.YELLOW, Fore.RED]


class LinterForOutWiker(Linter):
    '''
    Errors checker for OutWiker information
    '''

    def check_all(self, versions_xml: str) -> LinterResult:
        print(self._fores[LinterResult.OK] + 'Checking started...')
        checkers = [
            self.check_versions_list,
            self.check_release_date,
            self.check_even_versions,
        ]

        result = LinterResult.OK
        for checker in checkers:
            current_result, message = checker(versions_xml)
            result = result & current_result
            if message:
                print(self._fores[current_result] + '    ' + message)

        print(self._fores[result] + 'Checking finished')
        return result

    def check_release_date(self, versions_xml: str) -> Tuple[LinterResult, str]:
        '''
        Check that the date is set
        '''
        changelog = XmlChangelogParser.parse(versions_xml)
        for version in changelog.versions:
            if version.date is None:
                return (LinterResult.ERROR, 'No release date for OutWiker')

        return (LinterResult.OK, '')

    def check_versions_list(self, versions_xml: str) -> Tuple[LinterResult, str]:
        '''
        Check that the versions is not empty
        '''
        changelog = XmlChangelogParser.parse(versions_xml)
        if not changelog.versions:
            return (LinterResult.ERROR, 'No versions list for OutWiker')

        return (LinterResult.OK, '')

    def check_even_versions(self, versions_xml: str) -> Tuple[LinterResult, str]:
        '''
        Check that the date is set
        '''
        changelog = XmlChangelogParser.parse(versions_xml)
        for version in changelog.versions:
            try:
                build = int(version.number.split('.')[3])
            except (ValueError, IndexError):
                return (LinterResult.ERROR, 'Invalid version format: {}'.format(version.number))

            if build % 2 != 0:
                return (LinterResult.ERROR, 'Build number for version {} is odd (dev version)'.format(version.number))

        return (LinterResult.OK, '')
