#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.wxthumbmaker import WxThumbmaker
from ..thumbnails import Thumbnails
from outwiker.core.attachment import Attachment


class PageThumbmaker (object):
	def __init__ (self):
		# Имя файла превьюшки: th_width_200_fname
		# Имя файла превьюшки: th_height_100_fname
		self.thumbsTemplate = "th_%s_%d_%s"

		self.thumbmaker = WxThumbmaker()


	def __createThumb (self, page, fname, size, file_prefix, func):
		"""
		Создание превьюшки на все случаи жизни :)
		page - страница, внутри которой создается превьюшка
		fname - имя исходной картинки (без полного пути). Полный путь определяется по пути до страницы
		size - размер превьюшки
		file_prefix - дополнение к имени файла
		func - указатель на функцию, которая будет создавать превьюшку (из self.thumbmaker)
		"""
		thumb = Thumbnails (page)
		path_thumbdir = thumb.getThumbPath (True)

		path_src = os.path.join (Attachment (page).getAttachPath(), fname)

		# Имя файла для превьюшки
		fname_res = self.thumbsTemplate % (file_prefix, size, fname)

		# wx не умеет сохранять в GIF, поэтому преобразуем в PNG
		if fname_res.lower().endswith (".gif"):
			fname_res = fname_res.replace (".gif", ".png")

		path_res = os.path.join (path_thumbdir, fname_res)

		# Путь, относительный к корню страницы
		relative_path = os.path.join (Thumbnails.getRelativeThumbDir(), fname_res)

		if os.path.exists (path_res):
			return relative_path

		# Возможно исключение ThumbException
		func (path_src, size, path_res)

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
