# -*- coding: UTF-8 -*-

import unittest
from datetime import datetime

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class DateParserTest (unittest.TestCase):
    def setUp (self):
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        self.loader.clear()


    def testGetStruct_empty_01 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u''

        self.assertRaises (ValueError, createDateTimeStruct, text)


    def testGetStruct_empty_02 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'    '

        self.assertRaises (ValueError, createDateTimeStruct, text)


    def testGetStruct_01 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1y'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 1)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 0)


    def testGetStruct_02 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1mon'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 0)
        self.assertEqual (result.months, 1)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 0)


    def testGetStruct_03 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1d'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 0)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 1)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 0)


    def testGetStruct_04 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1h'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 0)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 1)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 0)


    def testGetStruct_05 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1min'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 0)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 1)
        self.assertEqual (result.seconds, 0)


    def testGetStruct_06 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1s'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 0)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 1)


    def testGetStruct_07 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1sasdf'

        self.assertRaises (ValueError, createDateTimeStruct, text)


    def testGetStruct_08 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1s 1ysdfasdf'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 0)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 1)


    def testGetStruct_09 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'1s 1y'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 1)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 1)


    def testGetStruct_10 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'  1s   1y  '

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 1)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 1)


    def testGetStruct_11 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'asdfasdf  1s   1y  adfadsf 10'

        result = createDateTimeStruct (text)

        self.assertEqual (result.years, 1)
        self.assertEqual (result.months, 0)
        self.assertEqual (result.days, 0)
        self.assertEqual (result.hours, 0)
        self.assertEqual (result.minutes, 0)
        self.assertEqual (result.seconds, 1)


    def testGetStruct_12 (self):
        from datagraph.dateparser import createDateTimeStruct
        text = u'10'

        self.assertRaises (ValueError, createDateTimeStruct, text)


    def testGetDateTime_01 (self):
        from datagraph.dateparser import createDateTime
        text = u'2014y 1mon 2d'

        result = createDateTime (text)
        self.assertEqual (result, datetime (2014, 1, 2))


    def testGetDateTime_02 (self):
        from datagraph.dateparser import createDateTime
        text = u'2014y 0mon'

        self.assertRaises (ValueError, createDateTime, text)


    def testGetDateTime_03 (self):
        from datagraph.dateparser import createDateTime
        text = u'2014y 13mon'

        self.assertRaises (ValueError, createDateTime, text)


    def testGetDateTime_04 (self):
        from datagraph.dateparser import createDateTime
        text = u'2014y'

        self.assertRaises (ValueError, createDateTime, text)
