#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re

from libs.pyparsing import Regex


class CommandFactory (object):
	@staticmethod
	def make (parser):
		return CommandToken(parser).getToken()


class CommandToken (object):
	def __init__ (self, parser):
		self.parser = parser

	def getToken (self):
		reg = r"""\(:\s*(?P<name>\w+)\s*(?P<params>.*?)\s*:\)((?P<content>.*?)\(:\s*(?P=name)end\s*:\))?"""
		#reg = r"""\(:\s*(?P<name>\w+)\s*(?P<params>.*?)\s*:\)(?P<content>.*?)\(:\s*(?P=name)end\s*:\)"""
		return Regex (reg, flags=re.MULTILINE | re.DOTALL | re.IGNORECASE).setParseAction (self.execute)


	def execute (self, s, l, t):
		"""
		Найти нужную команду и выполнить ее
		"""
		name = t["name"]
		params = t["params"]
		content = t["content"]

		try:
			command = self.parser.commands[name]
		except KeyError:
			return t[0]

		return command.execute (params, content)
