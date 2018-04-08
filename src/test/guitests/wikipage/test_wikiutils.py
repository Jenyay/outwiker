# -*- coding: UTF-8 -*-

import unittest

from outwiker.pages.wiki.utils import getCommandsByPos
from outwiker.pages.wiki.tableactions import getTableByPos


class WikiUtilsTest (unittest.TestCase):
    def testGetCommandsByPos_empty(self):
        text = ''
        pos = 0

        result = getCommandsByPos(text, pos)
        self.assertEqual(result, [])

    def testGetCommandsByPos_out_01(self):
        text = '(:command:)(:commandend:)'
        pos = 0

        result = getCommandsByPos(text, pos)
        self.assertEqual(result, [])

    def testGetCommandsByPos_out_02(self):
        text = '(:command:)(:commandend:)'
        pos = 25

        result = getCommandsByPos(text, pos)
        self.assertEqual(result, [])

    def testGetCommandsByPos_in_01(self):
        text = '(:command:)(:commandend:)'
        pos = 1

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].groupdict()['name'], 'command')

    def testGetCommandsByPos_in_02(self):
        text = '(:command:)(:commandend:)'
        pos = 24

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].groupdict()['name'], 'command')

    def testGetCommandsByPos_in_03(self):
        text = '(:command:)'
        pos = 1

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].groupdict()['name'], 'command')

    def testGetCommandsByPos_in_04(self):
        text = '(:command2:)(:command:)(:commandend:)'
        pos = 12

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 0)

    def testGetCommandsByPos_in_05(self):
        text = '(:command2:)(:command:)(:commandend:)'
        pos = 13

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].groupdict()['name'], 'command')

    def testGetCommandsByPos_nested_01(self):
        text = '(:command:)(:comamnd2:)(:command2end:)(:commandend:)'
        pos = 1

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].groupdict()['name'], 'command')

    def testGetCommandsByPos_nested_02(self):
        text = '(:command:)(:command2:)(:command2end:)(:commandend:)'
        pos = 13

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].groupdict()['name'], 'command')
        self.assertEqual(result[1].groupdict()['name'], 'command2')

    def testGetCommandsByPos_nested_03(self):
        text = '(:command:)(:command2:)(:command2end:)(:commandend:)'
        pos = 25

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].groupdict()['name'], 'command')
        self.assertEqual(result[1].groupdict()['name'], 'command2')

    def testGetCommandsByPos_nested_04(self):
        text = '(:command:)(:command2:)(:command2end:)(:commandend:)'
        pos = 40

        result = getCommandsByPos(text, pos)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].groupdict()['name'], 'command')

    def testTableByPos_01(self):
        text = '(:table:)(:tableend:)'
        pos = 0

        result = getTableByPos(text, pos)
        self.assertEqual(result, None)

    def testTableByPos_02(self):
        text = '(:table:)(:tableend:)'
        pos = 1

        result = getTableByPos(text, pos)
        self.assertEqual(result, '')

    def testTableByPos_03(self):
        text = '(:table:)(:tableend:)'
        pos = 21

        result = getTableByPos(text, pos)
        self.assertEqual(result, None)

    def testTableByPos_04(self):
        text = '(:table:)(:row:)(:rowend:)(:tableend:)'
        pos = 16

        result = getTableByPos(text, pos)
        self.assertEqual(result, '')

    def testTableByPos_05(self):
        text = '(:table20:)(:row:)(:rowend:)(:table20end:)'
        pos = 16

        result = getTableByPos(text, pos)
        self.assertEqual(result, '20')

    def testTableByPos_06(self):
        text = '(:table20:)(:row:)(:table3:)(:table3end:)(:rowend:)(:table20end:)'
        pos = 28

        result = getTableByPos(text, pos)
        self.assertEqual(result, '3')

    def testTableByPos_07(self):
        text = '(:table1:)(:table1end:)(:table20:)(:row:)(:table3:)(:table3end:)(:rowend:)(:table20end:)(:table4:)(:table4end:)'
        pos = 51

        result = getTableByPos(text, pos)
        self.assertEqual(result, '3')

    def testTableByPos_08_invalid(self):
        text = '(:tableqqq:)(:tableqqqend:)'
        pos = 2

        result = getTableByPos(text, pos)
        self.assertEqual(result, None)
