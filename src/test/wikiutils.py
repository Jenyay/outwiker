# -*- coding: UTF-8 -*-

import unittest

from outwiker.pages.wiki.utils import getCommandsByPos


class WikiUtilsTest (unittest.TestCase):
    def testGetCommandsByPos_empty (self):
        text = u''
        pos = 0

        result = getCommandsByPos (text, pos)
        self.assertEqual (result, [])


    def testGetCommandsByPos_out_01 (self):
        text = u'(:command:)(:commandend:)'
        pos = 0

        result = getCommandsByPos (text, pos)
        self.assertEqual (result, [])


    def testGetCommandsByPos_out_02 (self):
        text = u'(:command:)(:commandend:)'
        pos = 25

        result = getCommandsByPos (text, pos)
        self.assertEqual (result, [])


    def testGetCommandsByPos_in_01 (self):
        text = u'(:command:)(:commandend:)'
        pos = 1

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].groupdict()['name'], u'command')


    def testGetCommandsByPos_in_02 (self):
        text = u'(:command:)(:commandend:)'
        pos = 24

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].groupdict()['name'], u'command')


    def testGetCommandsByPos_in_03 (self):
        text = u'(:command:)'
        pos = 1

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].groupdict()['name'], u'command')


    def testGetCommandsByPos_in_04 (self):
        text = u'(:command2:)(:command:)(:commandend:)'
        pos = 12

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 0)


    def testGetCommandsByPos_in_05 (self):
        text = u'(:command2:)(:command:)(:commandend:)'
        pos = 13

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].groupdict()['name'], u'command')


    def testGetCommandsByPos_nested_01 (self):
        text = u'(:command:)(:comamnd2:)(:command2end:)(:commandend:)'
        pos = 1

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].groupdict()['name'], u'command')


    def testGetCommandsByPos_nested_02 (self):
        text = u'(:command:)(:command2:)(:command2end:)(:commandend:)'
        pos = 13

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 2)
        self.assertEqual (result[0].groupdict()['name'], u'command')
        self.assertEqual (result[1].groupdict()['name'], u'command2')


    def testGetCommandsByPos_nested_03 (self):
        text = u'(:command:)(:command2:)(:command2end:)(:commandend:)'
        pos = 25

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 2)
        self.assertEqual (result[0].groupdict()['name'], u'command')
        self.assertEqual (result[1].groupdict()['name'], u'command2')


    def testGetCommandsByPos_nested_04 (self):
        text = u'(:command:)(:command2:)(:command2end:)(:commandend:)'
        pos = 40

        result = getCommandsByPos (text, pos)
        self.assertEqual (len (result), 1)
        self.assertEqual (result[0].groupdict()['name'], u'command')
