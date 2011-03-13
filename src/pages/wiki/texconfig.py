#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core.config import StringOption

class TexConfig (object):
	"""
	Класс, хранящий указатели на настройки, связанные с mimeTex
	"""
	def __init__ (self, config):
		self.config = config

		# Путь до mimeTex
		self.mimeTexPath = StringOption (self.config, "Wiki", "mimetexpath", "")
