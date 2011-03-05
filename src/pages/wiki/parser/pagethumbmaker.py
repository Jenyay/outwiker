#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from core.wxthumbmaker import WxThumbmaker
from core.tree import RootWikiPage


class PageThumbmaker (object):
	def __init__ (self):
		self.thumbsDir = "__thumb"
		
		# Имя файла превьюшки: th_width_200_fname
		# Имя файла превьюшки: th_height_100_fname
		self.thumbsTemplate = "th_%s_%d_%s"

		self.thumbmaker = WxThumbmaker()


	def getThumbPath (self, page):
		"""
		Вернуть путь до папки с превьюшками
		"""
		return os.path.join (page.getAttachPath(), self.thumbsDir)


	def __createThumb (self, page, fname, size, file_prefix, func):
		"""
		Создание превьюшки на все случаи жизни :)
		page - страница, внутри которой создается превьюшка
		fname - имя исходной картинки (без полного пути). Полный путь определяется по пути до страницы
		size - размер превьюшки
		file_prefix - дополнение к имени файла
		func - указатель на функцию, которая будет создавать превьюшку (из self.thumbmaker)
		"""
		attachPath = page.getAttachPath()

		path = os.path.join (attachPath, self.thumbsDir)

		if not os.path.exists (path):
			# Исключения обрабатываем выше
			os.mkdir (path)

		path_src = os.path.join (attachPath, fname)

		# Имя файла для превьюшки

		fname_res = self.thumbsTemplate % (file_prefix, size, fname)

		# wx не умеет сохранять в GIF, поэтому преобразуем в PNG
		if fname_res.lower().endswith (".gif"):
			fname_res = fname_res.replace (".gif", ".png")

		path_res = os.path.join (attachPath, self.thumbsDir, fname_res)

		# Возможно исключение ThumbException
		func (path_src, size, path_res)

		# Путь, относительный к корню страницы
		relative_path = os.path.join (RootWikiPage.attachDir, self.thumbsDir, fname_res)

		return relative_path


	def createThumbByWidth (self, page, fname, width):
		"""
		Создать превьюшку и вернуть относительный путь до нее
		page - страница, внутри которой создается превьюшка
		fname - имя исходной картинки (без полного пути). Полный путь определяется по пути до страницы
		width - ширина превьюшки

		Возвращает путь относительно корня страницы
		"""
		return self.__createThumb (page, fname, width, u"width", self.thumbmaker.thumbByWidth)


	def createThumbByHeight (self, page, fname, height):
		"""
		Создать превьюшку и вернуть относительный путь до нее
		page - страница, внутри которой создается превьюшка
		fname - имя исходной картинки (без полного пути). Полный путь определяется по пути до страницы
		height - высота превьюшки

		Возвращает путь относительно корня страницы
		"""
		return self.__createThumb (page, fname, height, u"height", self.thumbmaker.thumbByHeight)


	def createThumbByMaxSize (self, page, fname, maxsize):
		"""
		Создать превьюшку и вернуть относительный путь до нее
		page - страница, внутри которой создается превьюшка
		fname - имя исходной картинки (без полного пути). Полный путь определяется по пути до страницы
		maxsize - максимальный размер превьюшки

		Возвращает путь относительно корня страницы
		"""
		return self.__createThumb (page, fname, maxsize, u"maxsize", self.thumbmaker.thumbByMaxSize)
