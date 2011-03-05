#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from utils import concatenate
from libs.pyparsing import Regex


class HeadingFactory (object):
	@staticmethod
	def make (parser):
		return HeadingToken().getToken()


class HeadingToken (object):
	def __init__ (self):
		self.heading1_Regex = "^!!\s+(?P<title>.*)$"
		self.heading2_Regex = "^!!!\s+(?P<title>.*)$"
		self.heading3_Regex = "^!!!!\s+(?P<title>.*)$"
		self.heading4_Regex = "^!!!!!\s+(?P<title>.*)$"
		self.heading5_Regex = "^!!!!!!\s+(?P<title>.*)$"
		self.heading6_Regex = "^!!!!!!!\s+(?P<title>.*)$"


	def getToken (self):
		"""
		Токены для заголовков H1 - H6
		"""
		tokens = []
		tokens.append (Regex (self.heading1_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H1>","</H1>") ) )
		tokens.append (Regex (self.heading2_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H2>","</H2>") ) )
		tokens.append (Regex (self.heading3_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H3>","</H3>") ) )
		tokens.append (Regex (self.heading4_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H4>","</H4>") ) )
		tokens.append (Regex (self.heading5_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H5>","</H5>") ) )
		tokens.append (Regex (self.heading6_Regex, re.MULTILINE).setParseAction(self.__convertToHeading("<H6>","</H6>") ) )

		return concatenate (tokens)


	def __convertToHeading (self, opening, closing):
		def conversionParseAction(s,l,t):
			return opening + t["title"] + closing
		return conversionParseAction
