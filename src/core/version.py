#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Классы для работы с версией программы
"""

class Status (object):
	"""
	Статус программы: альфа, бета и т.д.
	"""
	def __init__ (self, status):
		self.__createStatuses()
		self.status = status


	def __createStatuses (self):
		self.statset = dict()

		self.statset["dev"] = 0
		self.statset["nightly"] = 1

		self.statset["prealpha"] = 10
		self.statset["alpha"] = 20
		self.statset["alpha2"] = 21
		self.statset["alpha3"] = 22
		self.statset["alpha4"] = 23
		self.statset["alpha5"] = 24

		self.statset["prebeta"] = 29
		self.statset["beta"] = 30
		self.statset["beta2"] = 31
		self.statset["beta3"] = 32
		self.statset["beta4"] = 33
		self.statset["beta5"] = 34

		self.statset["preRC"] = 39
		self.statset["RC"] = 40
		self.statset["RC2"] = 41
		self.statset["RC3"] = 42
		self.statset["RC4"] = 43
		self.statset["RC5"] = 44

		self.statset["release"] = 100
		self.statset["stable"] = 1000



class Version (object):
	def __init__ (self, major, *args, **kwargs):
		self._vertion = [major]
		self.status = u""
