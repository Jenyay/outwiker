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
		# Здесь накапливаем список интересующих строк (по которым определяем изменилась страница или нет)
		content = []
		content.append (self.page.content.encode ("unicode_escape"))
		self.__getDirContent (self.page, content)

		# Настройки, касающиеся вида вики-страницы
		content.append (str (self.config.showAttachInsteadBlankOptions.value))
		content.append (str (self.config.thumbSizeOptions.value))

		return u"".join (content)


	def __getDirContent (self, page, filescontent, dirname="."):
		"""
		Сформировать строку для расчета хеша по данным вложенной поддиректории dirname (путь относительно __attach)
		page - страница, для которой собираем список вложений
		filescontent - список, содержащий строки, описывающие вложенные файлы
		"""
		attach = Attachment (page)
		attachroot = attach.getAttachPath()

		attachlist = attach.getAttachRelative (dirname)
		attachlist.sort (Attachment.sortByName)

		for fname in attachlist:
			fullpath = os.path.join (attachroot, dirname, fname)

			# Пропустим директории, которые начинаются с __
			if not os.path.isdir (fname) or not fname.startswith ("__"):
				filescontent.append (fname.encode ("unicode_escape"))
				filescontent.append (unicode (os.stat (fullpath).st_mtime))

				if os.path.isdir (fullpath):
					self.__getDirContent (page, filescontent, os.path.join (dirname, fname))

	
	def __generateAttachList (self):
		"""
		Сгенерировать список прикрепленных файлов.
		Используется в случае, если текст страницы пустой
		"""
		files = [os.path.basename (path) for path in Attachment (self.page).attachmentFull]
		files.sort()

		result = reduce (lambda res, path: res + "[[%s -> Attach:%s]]\n" % (path, path), files, u"")

		return result
