#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import shutil

import exceptions
from application import Application


class Attachment (object):
	"""
	Класс для работы с прикрепленными файлами
	"""
	# Название директории с прикрепленными файлами
	attachDir = u"__attach"

	def __init__ (self, page):
		"""
		page - страница, для которой интересуют прикрепленные файлы
		"""
		self.page = page

	
	def getAttachPath (self, create=False):
		"""
		Возвращает путь до страницы с прикрепленными файлами
		create - создать папку для прикрепленных файлов, если она еще не создана?
		"""
		path = os.path.join (self.page.path, Attachment.attachDir)

		if create and not os.path.exists(path):
			os.mkdir (path)

		return path


	@property
	def attachmentFull (self):
		"""
		Возвращает список прикрепленных файлов.
		Пути до файлов полные
		"""
		path = self.getAttachPath()

		if not os.path.exists (path):
			return []

		result = [os.path.join (path, fname) for fname in os.listdir (path)]

		return result


	def attach (self, files):
		"""
		Прикрепить файл к странице
		files -- список файлов (или папок), которые надо прикрепить
		"""
		if self.page.readonly:
			raise core.exceptions.ReadonlyException

		attachPath = self.getAttachPath(True)

		for name in files:
			if os.path.isdir (name):
				basename = os.path.basename (name)
				shutil.copytree (name, os.path.join (attachPath, basename) )
			else:
				shutil.copy (name, attachPath)

		Application.onPageUpdate (self.page)


	def removeAttach (self, files):
		"""
		Удалить прикрепленные файлы
		"""
		if self.page.readonly:
			raise core.exceptions.ReadonlyException

		attachPath = self.getAttachPath(True)

		for fname in files:
			path = os.path.join (attachPath, fname)
			try:
				if os.path.isdir (path):
					shutil.rmtree (path)
				else:
					os.remove (path)
			except OSError:
				Application.onPageUpdate (self.page)
				raise IOError (u"Can't remove %s" % fname)

		Application.onPageUpdate (self.page)
