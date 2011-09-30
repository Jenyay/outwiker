#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path

from outwiker.core.attachment import Attachment


class Thumbnails (object):
	"""
	Класс для работы с директорией с вложенными файлами
	"""
	thumbDir = u"__thumb"

	def __init__ (self, page):
		self.page = page

	
	@staticmethod
	def getRelativeThumbDir ():
		return os.path.join (Attachment.attachDir, Thumbnails.thumbDir)


	def getThumbPath (self, create):
		"""
		Получить полный путь до папки с превьюшками
		create - нужно ли создавать директорию, если ее еще нет
		"""
		path = os.path.join (Attachment (self.page).getAttachPath(create=create), Thumbnails.thumbDir)

		if create and not os.path.exists (path):
			os.mkdir (path)

		return path


	def clearDir (self):
		"""
		Удалить все содержимое папки __thumb (вложенные директории пока не трогаем)
		"""
		path = self.getThumbPath (create=False)

		if not os.path.exists (path):
			return

		for fname in os.listdir (path):
			fullpath = os.path.join (path, fname)

			if os.path.isfile (fullpath):
				os.remove (fullpath)
