#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from libs.pyparsing import Regex


class CenterAlignFactory (object):
	@staticmethod
	def make (parser):
		return CenterAlignToken(parser).getToken()


class RightAlignFactory (object):
	@staticmethod
	def make (parser):
		return RightAlignToken(parser).getToken()


class AlignToken (object):
	"""
	Базовый класс для "выравнивающих" токенов
	"""
	def __init__ (self, parser):
		self.parser = parser
	

	def _align (self, align):
		def __divTransform (s, l, t):
			return u'<DIV ALIGN="' + align + '">' + self.parser.parseWikiMarkup (t["text"]) + '</DIV>' + t["end"]

		return __divTransform



class CenterAlignToken (AlignToken):
	"""
	Токен для выравнивания по центру
	"""
	def __init__ (self, parser):
		AlignToken.__init__ (self, parser)


	def getToken (self):
		centerRegex = "%\\s*center\\s*%(?P<text>.*?)(?P<end>(\n\n)|\Z)"

		return Regex (centerRegex, 
				re.MULTILINE | re.DOTALL | re.IGNORECASE).setParseAction(self._align ("CENTER") )


class RightAlignToken (AlignToken):
	"""
	Токен для выравнивания по правому краю
	"""
	def __init__ (self, parser):
		AlignToken.__init__ (self, parser)


	def getToken (self):
		rightRegex = "%\\s*right\\s*%(?P<text>.*?)(?P<end>(\n\n)|\Z)"

		return Regex (rightRegex, 
				re.MULTILINE | re.DOTALL | re.IGNORECASE).setParseAction(self._align ("RIGHT") )
