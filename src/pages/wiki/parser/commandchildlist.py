#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from command import Command


class SimpleView (object):
	"""
	Класс для простого представления списка дочерних страниц - каждая страница на отдельной строке
	"""
	@staticmethod
	def make (children, parser, params):
		"""
		children - список упорядоченных дочерних страниц
		"""
		template = u'<A HREF="{link}">{title}</A>\n'
		result = u"".join ([template.format (link=page.title, title=page.title) for page in children ] )

		# Выкинем последний перевод строки
		return result[: -1]


class ChildListCommand (Command):
	def __init__ (self, parser):
		Command.__init__ (self, parser)

	@property
	def name (self):
		return u"childlist"


	def execute (self, params, content):
		return SimpleView.make (self.parser.page.children, self.parser, params)
