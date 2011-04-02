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


	@property
	def attachmentBasename (self):
		"""
		Возвращает список прикрепленных файлов (только имена файлов без путей).
		"""
		path = self.getAttachPath()

		if not os.path.exists (path):
			return []

		return os.listdir (path)


	def attach (self, files):
		"""
		Прикрепить файл к странице
		files -- список файлов (или папок), которые надо прикрепить
		"""
		if self.page.readonly:
			raise exceptions.ReadonlyException

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
			raise exceptions.ReadonlyException

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


	@staticmethod
	def sortByName (fname1, fname2):
		"""
		Метод для сортировки файлов по имени
		"""
		fname1_lower = fname1.lower()
		fname2_lower = fname2.lower()

		if fname1_lower > fname2_lower:
			return 1
		elif fname1_lower < fname2_lower:
			return -1
		return 0


	@staticmethod
	def sortByExt (fname1, fname2):
		"""
		Метод для сортировки файлов по расширению
		"""
		(root1, ext1) = os.path.splitext (os.path.basename (fname1).lower())
		(root2, ext2) = os.path.splitext (os.path.basename (fname2).lower())

		if ext1 > ext2:
			return 1
		elif ext1 < ext2:
			return -1
		
		if root1 > root2:
			return 1
		elif root1 < root2:
			return -1

		return 0


	@staticmethod
	def sortByDate (fname1, fname2):
		"""
		Метод для сортировки файлов по дате. 
		Пути до файлов должны быть полные
		"""
		stat1 = os.stat (fname1)
		stat2 = os.stat (fname2)

		if stat1.st_mtime > stat2.st_mtime:
			return 1
		elif stat1.st_mtime < stat2.st_mtime:
			return -1
		return 0


	def getFullPath (self, fname, create=False):
		"""
		Возвращает полный путь до прикрепленного файла с именем fname.
		Файл fname не обязательно должен существовать.
		create - нужно ли создавать папку __attach, если ее еще не существует?
		"""
		return os.path.join (self.getAttachPath(create), fname)
