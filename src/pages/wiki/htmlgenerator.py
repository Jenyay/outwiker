#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import hashlib

from core.config import Config, StringOption
from core.htmlimprover import HtmlImprover
from core.application import Application
from core.attachment import Attachment
from core.tree import RootWikiPage
from parserfactory import ParserFactory
from wikiconfig import WikiConfig


class HtmlGenerator (object):
	"""
	Класс, который создает HTML для вики-страницы с учетом кэширования.
	"""
	def __init__ (self, page):
		self.page = page
		self.config = WikiConfig (Application.config)

		self.resultName = u"__content.html"
		self._configSection = u"wiki"
		self._hashKey = u"md5_hash"


	def makeHtml (self):
		path = self.getResultPath()

		if self.canReadFromCache():
			return path

		factory = ParserFactory ()
		parser = factory.make(self.page, Application.config)

		content = self.page.content if (len (self.page.content) > 0 or
			not self.config.showAttachInsteadBlankOptions.value) else self.__generateAttachList ()

		text = HtmlImprover.run (parser.toHtml (content) )

		with open (path, "wb") as fp:
			fp.write (text.encode ("utf-8"))

		hashoption = StringOption (Config (os.path.join (self.page.path, RootWikiPage.pageConfig)),
				self._configSection, self._hashKey, u"")

		hashoption.value = self.getHash()

		return path


	def getHash (self):
		return hashlib.md5(self.__getFullContent () ).hexdigest()


	def getResultPath (self):
		return os.path.join (self.page.path, self.resultName)


	def canReadFromCache (self):
		"""
		Можно ли прочитать готовый HTML из кеша?
		"""
		path = self.getResultPath()
		hash = self.getHash()

		hashoption = StringOption (Config (os.path.join (self.page.path, RootWikiPage.pageConfig)),
				self._configSection, self._hashKey, u"")

		if os.path.exists (path) and (hash == hashoption.value or self.page.readonly):
			return True

		return False



	def __getFullContent (self):
		"""
		Получить контент для расчета контрольной суммы, по которой определяется, нужно ли обновлять страницу
		"""
		# Текст страницы
		result = self.page.content.encode ("unicode_escape")

		# Список прикрепленных файлов
		attachlist = Attachment (self.page).attachmentFull
		attachlist.sort (Attachment.sortByName)

		for fname in attachlist:
			# TODO: Учесть файлы во вложенных директориях
			if not os.path.isdir (fname) or not os.path.basename (fname).startswith ("__"):
				# Пропустим директории, которые начинаются с __
				result += fname.encode ("unicode_escape")
				result += unicode (os.stat (fname).st_mtime)

		# Настройки, касающиеся вида вики-страницы
		result += str (self.config.showAttachInsteadBlankOptions.value)
		result += str (self.config.thumbSizeOptions.value)
		return result

	
	def __generateAttachList (self):
		"""
		Сгенерировать список прикрепленных файлов.
		Используется в случае, если текст страницы пустой
		"""
		files = [os.path.basename (path) for path in Attachment (self.page).attachmentFull]
		files.sort()

		result = reduce (lambda res, path: res + "[[%s -> Attach:%s]]\n" % (path, path), files, u"")

		return result
