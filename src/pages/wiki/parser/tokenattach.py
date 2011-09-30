#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from libs.pyparsing import replaceWith, Literal

from outwiker.core.attachment import Attachment

from utils import concatenate, isImage


class NotImageAttachFactory (object):
	@staticmethod
	def make (parser):
		return NotImageAttachToken (parser).getToken()


class ImageAttachFactory (object):
	@staticmethod
	def make (parser):
		return ImageAttachToken (parser).getToken()



class AttachToken (object):
	attachString = u"Attach:"

	def __init__ (self, parser):
		self.parser = parser
	

	# TODO: Вынести в отдельный модуль
	def sortByLength (self, fname1, fname2):
		"""
		Функция для сортировки имен по длине имени
		"""
		if len (fname1) > len (fname2):
			return 1
		elif len (fname1) < len (fname2):
			return -1

		return 0



class NotImageAttachToken (AttachToken):
	def __init__ (self, parser):
		AttachToken.__init__ (self, parser)


	def getToken (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesAll = []

		attaches = Attachment (self.parser.page).attachmentFull
		attaches.sort (self.sortByLength, reverse=True)

		for attach in attaches:
			if not isImage (attach):
				fname = os.path.basename (attach)
				attach = Literal (AttachToken.attachString + fname)
				attach.setParseAction (replaceWith (self.__getReplaceForAttach (fname) ) )
				attachesAll.append (attach)

		return concatenate (attachesAll)


	def __getReplaceForAttach (self, fname):
		"""
		Получить строку для замены ссылкой на прикрепленный файл
		"""
		return '<A HREF="%s/%s">%s</A>' % (Attachment.attachDir, fname, fname)



class ImageAttachToken (AttachToken):
	def __init__ (self, parser):
		AttachToken.__init__ (self, parser)


	def getToken (self):
		"""
		Создать элементы из прикрепленных файлов.
		Отдельно картинки, отдельно все файлы
		"""
		attachesImages = []

		attaches = Attachment (self.parser.page).attachmentFull
		attaches.sort (self.sortByLength, reverse=True)

		for attach in attaches:
			if isImage (attach):
				fname = os.path.basename (attach)
				attach_token = Literal (AttachToken.attachString + fname)
				attach_token.setParseAction (replaceWith (self.__getReplaceForImageAttach (fname) ) )
				attachesImages.append (attach_token)

		return concatenate (attachesImages)


	def __getReplaceForImageAttach (self, fname):
		"""
		Получить строку для замены ссылкой на прикрепленный файл
		"""
		return '<IMG SRC="%s/%s"/>' % (Attachment.attachDir, fname)
