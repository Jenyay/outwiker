#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core.config import BooleanOption, IntegerOption

class WikiConfig (object):
	"""
	Класс, хранящий указатели на настройки, связанные с викиы
	"""
	def __init__ (self, config):
		self.config = config

		# Показывать вкладку с HTML-кодом?
		self.showHtmlCodeOptions = BooleanOption (self.config, "Wiki", "ShowHtmlCode", True)

		# Размер превьюшек по умолчанию
		self.thumbSizeOptions = IntegerOption (self.config, "Wiki", "ThumbSize", 250)
		
		# Показывать список прикрепленных файлов вместо пустой страницы?
		self.showAttachInsteadBlankOptions = BooleanOption (self.config, "Wiki", "ShowAttachInsteadBlank", True)
