#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os


class HtmlReport (object):
	"""
	Класс для генерации HTML-а, для вывода найденных страниц
	"""

	@staticmethod
	def generate (pages):
		"""
		Сгенерить отчет
		"""
		shell = u"""<html>
				<head>
				<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>
				</head>
				<body>
				<ol type='1'>
				%s
				</ol>
				</body>
				</html>"""

		items = u""

		for page in pages:
			items += HtmlReport.generataPageView (page)

		result = shell % items
		return result
	

	@staticmethod
	def generataPageView (page):
		"""
		Вернуть представление для одной страницы
		"""
		item = "<b><a href='/%s'>%s</a></b>" % (page.subpath, page.title)
		if page.parent.parent != None:
			item += u" (%s)" % page.parent.subpath

		item += "<br>" + HtmlReport.generatePageTags (page) + "<p>"

		result = u"<li>%s</li>\n" % item

		return result


	@staticmethod
	def generatePageTags (page):
		"""
		Создать список тегов для страницы
		"""
		result = u""
		for tag in page.tags:
			result += HtmlReport.generageTagView (tag) + u", "

		return result [: -2]


	@staticmethod
	def generageTagView (tag):
		"""
		Оформление для одного тега
		"""
		result = "<img src='__tag.png'/>%s" % (tag)
		return result
