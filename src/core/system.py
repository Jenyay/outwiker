#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Действия, которые зависят от ОС, на которой запущена программа
"""

import os
import os.path
import sys
import locale

import wx

class Windows (object):
	def __init__ (self):
		pass


	def startFile (self, path):
		"""
		Запустить программу по умолчанию для path
		"""
		os.startfile (path.replace ("/", "\\"))
	

	@property
	def filesEncoding (self):
		return "1251"


	@property
	def inputEncoding (self):
		"""
		Кодировка, используемая для преобразования нажатой клавиши в строку
		"""
		return "mbcs"


	@property
	def dragFileDataObject (self):
		"""
		Получить класс для перетаскивания файлов из окна OutWiker'а в другие приложения.
		Под Linux'ом wx.FileDataObject не правильно работает с Unicode
		"""
		return wx.FileDataObject



class Unix (object):
	def __init__ (self):
		pass

	def startFile (self, path):
		"""
		Запустить программу по умолчанию для path
		"""
		runcmd = "xdg-open '%s'" % path
		wx.Execute (runcmd)
	

	@property
	def filesEncoding (self):
		return "utf-8"

	
	@property
	def inputEncoding (self):
		encoding = locale.getpreferredencoding()

		if not encoding:
			encoding = "utf8"
	
		return encoding


	@property
	def dragFileDataObject (self):
		"""
		Получить класс для перетаскивания файлов из окна OutWiker'а в другие приложения.
		Под Linux'ом wx.FileDataObject не правильно работает с Unicode
		"""
		class GtkFileDataObject (wx.PyDataObjectSimple):
			"""
			Класс данных для перетаскивания файлов. Использовать вместо wx.FileDataObject, который по сути не работает с Unicode
			"""
			def __init__ (self):
				wx.PyDataObjectSimple.__init__ (self, wx.DataFormat (wx.DF_FILENAME))
				self._fnames = []

			def AddFile (self, fname):
				self._fnames.append (fname)

			def GetDataHere (self):
				result = ""
				for fname in self._fnames:
					result += u"file:%s\r\n" % (fname)
				
				# Преобразуем в строку
				return result.strip().encode("utf8")

			def GetDataSize (self):
				return len (self.GetDataHere())

		return GtkFileDataObject



def getOS ():
	if os.name == "nt":
		return Windows()
	else:
		return Unix()

def getCurrentDir ():
	return unicode (os.path.dirname (sys.argv[0]), getOS().filesEncoding)


def getImagesDir ():
	return os.path.join (getCurrentDir(), "images")
