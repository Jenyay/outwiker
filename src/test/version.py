#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

from core.version import Version, Status

class StatusTest (unittest.TestCase):
	def setUp (self):
		pass


	def test1 (self):
		self.assertEqual (Status ("dev") == Status ("dev"))
		self.assertEqual (Status ("beta") == Status ("beta"))
		self.assertEqual (Status ("beta") > Status ("alpha"))
		self.assertEqual (Status ("beta") < Status ("stable"))

		self.assertEqual (Status ("dev") < Status ("alpha"))
		self.assertEqual (Status ("alpha") < Status ("alpha2"))
		self.assertEqual (Status ("alpha2") < Status ("beta"))
		self.assertEqual (Status ("beta") < Status ("beta2"))
		self.assertEqual (Status ("beta2") < Status ("RC"))
		self.assertEqual (Status ("RC") < Status ("RC2"))
		self.assertEqual (Status ("RC2") < Status ("stable"))



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
		ver = Version (1, 0, 6, status="beta")
		self.assertEqual (str(ver), "1.0.6 beta")
	

	def testToString4 (self):
		ver = Version (1)
		self.assertEqual (str(ver), "1")
	

	def testCompare1 (self):
		self.assertTrue (Version (1) == Version (1))
		self.assertTrue (Version (2) > Version (1))
		self.assertTrue (Version (2) >= Version (1))
		self.assertTrue (Version (1, 1) > Version (1))
		self.assertTrue (Version (1, 1) >= Version (1))

		self.assertTrue (Version (2, 1) < Version (2, 2))
		self.assertTrue (Version (2, 1) <= Version (2, 2))

		self.assertTrue (Version (1, 0, 10) > Version (1, 0))
		self.assertTrue (Version (1, 0, 2) > Version (1, 0, 1))
		
		self.assertTrue (Version (1, 0) < Version (1, 0, 10))
		self.assertTrue (Version (1, 0, 1) < Version (1, 0, 2))


	def testCompare3 (self):
		self.assertTrue (Version (1, 0) == Version (1))
	

	def testCompareStatus (self):
		self.assertTrue (Version (1, status="beta") == Version (1, status="beta"))
		self.assertTrue (Version (1, 2, 3, status="beta") == Version (1, 2, 3, status="beta"))

		self.assertTrue (Version (1, status="alpha") < Version (1, status="beta"))
		self.assertTrue (Version (1, status="alpha") <= Version (1, status="beta"))
		self.assertTrue (Version (1, status="RC") > Version (1, status="beta"))
		self.assertTrue (Version (1, status="RC") >= Version (1, status="beta"))

		self.assertTrue (Version (1, 1, status="alpha") > Version (1, status="stable"))
		self.assertTrue (Version (1, 1, status="alpha") >= Version (1, status="stable"))
		self.assertTrue (Version (1, 1, status="alpha") > Version (1, 0, status="stable"))
		self.assertTrue (Version (1, 1, status="alpha") >= Version (1, 0, status="stable"))

		self.assertTrue (Version (1, status="stable") < Version (1, 1, status="alpha"))
		self.assertTrue (Version (1, status="stable") <= Version (1, 1, status="alpha"))
		self.assertTrue (Version (1, 0, status="stable") < Version (1, 1, status="alpha"))
		self.assertTrue (Version (1, 0, status="stable") < Version (1, 1, status="alpha"))



