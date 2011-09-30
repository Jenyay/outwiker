#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.version import Version, Status, StatusSet


class StatusTest (unittest.TestCase):
	def setUp (self):
		pass


	def testEqual (self):
		self.assertTrue (StatusSet.DEV == StatusSet.DEV)
		self.assertTrue (StatusSet.BETA == StatusSet.BETA)
	

	def testNotEqual (self):
		self.assertTrue (StatusSet.DEV != StatusSet.BETA)
		self.assertTrue (StatusSet.STABLE != StatusSet.BETA)
	

	def testCustomCompare (self):
		self.assertTrue (StatusSet.DEV > Status ("custom", -1))
		self.assertTrue (StatusSet.BETA < Status ("custom", 10000))

		self.assertTrue (StatusSet.DEV >= Status ("custom", -1))
		self.assertTrue (StatusSet.BETA <= Status ("custom", 10000))
	

	def testLess (self):
		self.assertTrue (StatusSet.BETA < StatusSet.STABLE)
		self.assertTrue (StatusSet.DEV < StatusSet.ALPHA)
		self.assertTrue (StatusSet.ALPHA < StatusSet.ALPHA2)
		self.assertTrue (StatusSet.ALPHA2 < StatusSet.BETA)
		self.assertTrue (StatusSet.BETA < StatusSet.BETA2)
		self.assertTrue (StatusSet.BETA2 < StatusSet.RC)
		self.assertTrue (StatusSet.RC < StatusSet.RC2)
		self.assertTrue (StatusSet.RC2 < StatusSet.STABLE)


	def testLessEqual (self):
		self.assertTrue (StatusSet.BETA <= StatusSet.STABLE)
		self.assertTrue (StatusSet.DEV <= StatusSet.ALPHA)
		self.assertTrue (StatusSet.ALPHA <= StatusSet.ALPHA2)
		self.assertTrue (StatusSet.ALPHA2 <= StatusSet.BETA)
		self.assertTrue (StatusSet.BETA <= StatusSet.BETA2)
		self.assertTrue (StatusSet.BETA2 <= StatusSet.RC)
		self.assertTrue (StatusSet.RC <= StatusSet.RC2)
		self.assertTrue (StatusSet.RC2 <= StatusSet.STABLE)


	def testGreatEqual (self):
		self.assertTrue (StatusSet.BETA >= StatusSet.ALPHA)
		self.assertTrue (StatusSet.ALPHA >= StatusSet.DEV)


class VersionTest(unittest.TestCase):
	def setUp(self):
		pass

	
	def testToString1 (self):
		ver = Version (1)
		self.assertEqual (str(ver), "1")


	def testToString2 (self):
		ver = Version (1, 0, 3)
		self.assertEqual (str(ver), "1.0.3")
	

	def testToString3 (self):
		ver = Version (1, 0, 6, status=StatusSet.BETA)
		self.assertEqual (str(ver), "1.0.6 beta")
	

	def testToString4 (self):
		ver = Version (1, 0, 6)
		self.assertEqual (str(ver), "1.0.6")


	def testCompareEqual (self):
		self.assertTrue (Version (1) == Version (1))
		self.assertTrue (Version (1, 2, 3) == Version (1, 2, 3))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.BETA) == Version (1, 2, 3, status=StatusSet.BETA))
	

	def testCompareNotEqual (self):
		self.assertTrue (Version (1) != Version (2))
		self.assertTrue (Version (1, 2, 3) != Version (1, 2, 4))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.BETA) != Version (1, 2, 3, status=StatusSet.ALPHA))
	

	def testCompareGreat (self):
		self.assertTrue (Version (2) > Version (1))
		self.assertTrue (Version (1, 2, 4) > Version (1, 2, 3))
		self.assertTrue (Version (2, 2, 4) > Version (1, 2, 3))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.STABLE) > Version (1, 2, 3, status=StatusSet.BETA))
		self.assertTrue (Version (2, 2, 3, status=StatusSet.ALPHA) > Version (1, 2, 3, status=StatusSet.BETA) )

	
	def testCompareGreatEqual (self):
		self.assertTrue (Version (2) >= Version (1))
		self.assertTrue (Version (1, 2, 4) >= Version (1, 2, 3))
		self.assertTrue (Version (2, 2, 4) >= Version (1, 2, 3))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.STABLE) >= Version (1, 2, 3, status=StatusSet.BETA))
		self.assertTrue (Version (2, 2, 3, status=StatusSet.ALPHA) >= Version (1, 2, 3, status=StatusSet.BETA) )

	
	def testCompareLess (self):
		self.assertTrue (Version (1) < Version (2))
		self.assertTrue (Version (1, 2, 2) < Version (1, 2, 3))
		self.assertTrue (Version (2, 2, 4) < Version (2, 6, 3))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.ALPHA) < Version (1, 2, 3, status=StatusSet.BETA))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.BETA) < Version (2, 2, 3, status=StatusSet.ALPHA))
	

	def testCompareLessEqual (self):
		self.assertTrue (Version (1) <= Version (2))
		self.assertTrue (Version (1, 2, 2) <= Version (1, 2, 3))
		self.assertTrue (Version (2, 2, 4) <= Version (2, 6, 3))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.ALPHA) <= Version (1, 2, 3, status=StatusSet.BETA))
		self.assertTrue (Version (1, 2, 3, status=StatusSet.BETA) <= Version (2, 2, 3, status=StatusSet.ALPHA))
	

	def testParse1 (self):
		self.assertTrue (Version.parse ("1") == Version (1))


	def testParse2 (self):
		self.assertTrue (Version.parse ("1.2.3") == Version (1, 2, 3), str (Version.parse ("1.2.3")))

	
	def testParse3 (self):
		self.assertTrue (Version.parse ("1.2.3 beta") == Version (1, 2, 3, status=StatusSet.BETA))
		self.assertTrue (Version.parse (" 1.2.3 dev") == Version (1, 2, 3, status=StatusSet.DEV))
		self.assertTrue (Version.parse ("1.2.3  stable ") == Version (1, 2, 3, status=StatusSet.STABLE))
	

	def testParse4 (self):
		self.assertRaises (ValueError, Version.parse, "abyrvalg")
		self.assertRaises (ValueError, Version.parse, ".10.2.0")
