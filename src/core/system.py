#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Действия, которые зависят от ОС, на которой запущена программа
"""

import os
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


def getOS ():
	if os.name == "nt":
		return Windows()
	else:
		return Unix()

def getCurrentDir ():
	return unicode (os.path.dirname (sys.argv[0]), getOS().filesEncoding)


def getImagesDir ():
	return os.path.join (getCurrentDir(), "images")
