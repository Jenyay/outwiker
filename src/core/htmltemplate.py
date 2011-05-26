#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from string import Template
import os.path


class HtmlTemplate (object):
	"""
	Класс для генерации HTML-страницы на основе шаблона
	"""
	def __init__ (self, path):
		"""
		path - путь до директории с шаблоном. 

		Основной шаблон должен иметь имя template.html, 
		содержание которого оформлено в стиле, описанном в http://docs.python.org/library/string.html#template-strings
		"""
		self.fontsize = 14
		self.fontfamily = u"Verdana"

		tpl_fname = u"template.html"
		tpl_path = os.path.join (path, tpl_fname)

		with open (tpl_path) as fp:
			self.template = Template (unicode (fp.read().strip(), "utf8") )


	def substitute (self, content):
		return self.template.substitute (content=content, 
				fontsize=self.fontsize,
				fontfamily = self.fontfamily)
