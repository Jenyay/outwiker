#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Классы для глобального поиска по вики
"""
import os.path
import core.system

#from searchpage import SearchWikiPage, SearchPageFactory
#import searchpage

class AllTagsSearchStrategy (object):
	"""
	Стратегия проверки тегов, когда все теги должны быть найдены
	"""
	@staticmethod
	def testTags (tags, page):
		result = True

		page_tags = [tag.lower() for tag in page.tags]

		for tag in tags:
			if tag not in page_tags:
				result = False
				break

		return result


class AnyTagSearchStrategy (object):
	"""
	Стратегия проверки тегов, когда достаточно найти один гет
	"""
	@staticmethod
	def testTags (tags, page):
		if len (tags) == 0:
			return True

		result = False

		page_tags = [tag.lower() for tag in page.tags]

		for tag in tags:
			if tag in page_tags:
				result = True
				break

		return result


class Searcher (object):
	def __init__ (self, phrase, tags, tagsStrategy):
		"""
		phrase -- строка поиска (неразобранная)
		tags -- список тегов, по которым ищем страницы
		tagsStrategy -- стратегия поиска по тегам
		"""
		self.phrase = phrase
		self.tags = [tag.lower() for tag in tags]
		self.tagsStrategy = tagsStrategy
	

	def find (self, root):
		"""
		Найти подходящие по условию поиска страницы
		"""
		result = []

		for page in root.children:
			if (self.tagsStrategy.testTags (self.tags, page) and 
					(self.testTitle (page) or self.testContent (page) ) ):
				result.append (page)

			result += self.find (page)

		return result


	#def testTags (self, page):
	#	"""
	#	Вернуть True, если все искомые теги установлены и для page.
	#	Также возвращает True, если список искомых тегов пуст
	#	"""
	#	result = True

	#	page_tags = [tag.lower() for tag in page.tags]

	#	for tag in self.tags:
	#		if tag not in page_tags:
	#			result = False
	#			break

	#	return result


	def testTitle (self, page):
		title = page.title.lower()

		if len (self.phrase) == 0 or self.phrase.lower() in title:
			return True

		return False


	def testContent (self, page):
		"""
		Проверить, что искомая фраза встречается в контексте страницы.
		Также возвращает True, если контент пуст
		"""
		content = page.textContent.lower()
		if len (self.phrase) == 0 or self.phrase.lower() in content:
			return True

		return False


class HtmlReport (object):
	"""
	Класс для генерации HTML-а, для вывода найденных страниц
	"""

	@staticmethod
	def generate (pages):
		"""
		Сгенерить отчет
		"""
		shell = u"<html>\
				<head>\
				<meta http-equiv='Content-Type' content='text/html; charset=UTF-8'/>\
				</head>\
				<body>\
				<ol type='1'>\
				%s\
				</ol>\
				</body>\
				</html>"

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
		path = os.path.join (core.system.getImagesDir(), "tag.png")
		result = "<img src='%s'/>%s" % (path, tag)
		return result


class TagsList (object):
	"""
	Класс для хранения списка всех тегов в вики
	"""
	def __init__ (self, root):
		self._root = root

		# Словарь тегов. Ключ - тег, значение - список страниц с этим тегом
		self._tags = {}

		self._findTags (root)

	
	def _findTags (self, page):
		if page.parent != None:
			for tag in page.tags:
				tag_lower = tag.lower()

				if tag_lower in self._tags.keys():
					self._tags[tag_lower].append (page)
				else:
					self._tags[tag_lower] = [page]

		for child in page.children:
			self._findTags (child)
	

	def __len__ (self):
		return len (self._tags.keys())


	def __getitem__ (self, tag):
		return self._tags[tag.lower()]


	def __iter__ (self):
		tags = self._tags.keys()
		tags.sort()

		return iter (tags)


	@staticmethod
	def parseTagsList (tagsString):
		"""
		Преобразовать строку тегов, разделенных запятой, в список
		"""
		tags = [tag.strip() for tag in tagsString.split (",") 
				if len (tag.strip()) > 0]

		return tags


	@staticmethod
	def getTagsString (tags):
		"""
		Получить строку тегов
		"""
		result = u""
		count = len (tags)

		for n in range (count):
			result += tags[n]
			if n != count - 1:
				result += ", "

		return result

