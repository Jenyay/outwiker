#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ConfigParser

class Config (object):
	"""
	Оболочка над ConfigParser
	"""
	def __init__ (self, fname):
		"""
		fname -- имя файла конфига
		"""
		self.fname = fname
		self.__config = ConfigParser.ConfigParser()
		self.__config.read (self.fname)
	

	def set (self, section, param, value):
		section_encoded = section.encode ("utf-8")
		if not self.__config.has_section (section_encoded):
			self.__config.add_section (section_encoded)

		self.__config.set (section_encoded, param.encode ("utf-8"), unicode (value).encode ("utf-8"))
		self.save()


	def save (self):
		with open (self.fname, "wb") as fp:
			self.__config.write (fp)
	
	
	def get (self, section, param):
		return unicode (self.__config.get (section.encode ("utf-8"), param.encode ("utf-8")), "utf-8")

	
	def getint (self, section, param):
		return int (self.__config.get (section.encode ("utf-8"), param.encode ("utf-8")))

	def getbool (self, section, param):
		val = self.__config.get (section.encode ("utf-8"), param.encode ("utf-8"))

		return True if val.strip().lower() == "true" else False


	def remove_section (self, section):
		section_encoded = section.encode ("utf-8")
		result = self.__config.remove_section (section_encoded)
		self.save()
		return result


	def has_section (self, section):
		section_encoded = section.encode ("utf-8")
		return self.__config.has_section (section_encoded)
