#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import unittest

class MainIdTest (unittest.TestCase):
	"""
	Тесты класса, хранящий основные идентификаторы для кнопок и пунктов меню
	"""

	def test1 (self):
		from outwiker.gui.mainid import MainId
		val1 = MainId.ID_ATTACH

		from outwiker.gui.mainid import MainId
		val2 = MainId.ID_ATTACH

		self.assertEqual (val1, val2)

		import outwiker.gui.mainid
		val3 = outwiker.gui.mainid.MainId.ID_ATTACH
		self.assertEqual (val2, val3)

