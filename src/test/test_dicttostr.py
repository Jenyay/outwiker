# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.commands import dictToStr


class DictToStrTest(unittest.TestCase):
    def testDictToStr_01_empty(self):
        params = {}
        result = dictToStr(params)

        validResult = u''

        self.assertEqual(result, validResult)


    def testDictToStr_02(self):
        params = {
            u'param1': 10
        }
        result = dictToStr(params)

        validResult = u'param1="10"'

        self.assertEqual(result, validResult)


    def testDictToStr_03(self):
        params = {
            u'param1': 10,
            u'Параметр2': u'абырвалг',
        }
        result = dictToStr(params)

        validResult = u'param1="10", Параметр2="абырвалг"'

        self.assertEqual(result, validResult)


    def testDictToStr_04(self):
        params = {
            u'param1': 10,
            u'Параметр2': u"абыр'валг",
        }
        result = dictToStr(params)

        validResult = u'param1="10", Параметр2="абыр\'валг"'

        self.assertEqual(result, validResult)


    def testDictToStr_05(self):
        params = {
            u'param1': 10,
            u'Параметр2': u'абыр"валг',
        }
        result = dictToStr(params)

        validResult = u'param1="10", Параметр2=\'абыр"валг\''

        self.assertEqual(result, validResult)


    def testDictToStr_06(self):
        params = {
            u'param1': 10,
            u'Параметр2': u'аб\'ыр"валг',
        }
        result = dictToStr(params)

        validResult = u'param1="10", Параметр2="аб\'ыр\\"валг"'

        self.assertEqual(result, validResult, result)


    def testDictToStr_07(self):
        params = {
            u'param1': 10,
            u'Параметр2': u'',
        }
        result = dictToStr(params)

        validResult = u'param1="10", Параметр2=""'

        self.assertEqual(result, validResult, result)
