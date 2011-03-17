#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import subprocess
import hashlib

from core.system import getOS, getCurrentDir


def getTexRender (thumb_path):
	"""
	Возвращает класс для рендеринга формул в зависимости от операционки
	"""
	if os.name == "nt":
		return MimeTexWindows(thumb_path)
	else:
		return MimeTexLinux(thumb_path)


class MimeTex (object):
	"""
	Базовый класс для рендеринга формул
	В производных классах нужно опеределить свойства mimeTexPath, useShellPipe
	"""
	def __init__ (self, thumb_path):
		"""
		thumb_path - путь до папки, где можно делать временные файлы, и где создается файл с картинкой
		"""
		self.thumb_path = thumb_path

		# Имя временного файла
		self.tempFname = "__temp.tmp"

	
	def makeImage (self, eqn):
		"""
		eqn - выражение, которое нужно отрендерить
		"""
		currentOS = getOS()

		temp_path = os.path.join (self.thumb_path, self.tempFname)

		imageName = self.getImageName (eqn)
		image_path = os.path.join (self.thumb_path, imageName)

		with open (temp_path, "w") as fp:
			fp.write (eqn)

		# mimeTexPath нужно определить в производных классах
		mimeTexPath = self.mimeTexPath

		p = subprocess.Popen([mimeTexPath.encode (currentOS.filesEncoding), 
			"-f", temp_path.encode (currentOS.filesEncoding), 
			"-e", image_path.encode (currentOS.filesEncoding)], shell=self.useShellPipe)

		p.communicate()
		return imageName


	def getImageName (self, eqn):
		md5 = hashlib.md5 (eqn).hexdigest()
		fname = u"eqn_{0}.gif".format (md5)
		return fname



class MimeTexWindows (MimeTex):
	"""
	Класс для работы с mimeTex под Windows
	"""
	@property
	def mimeTexPath (self):
		os.path.join (getCurrentDir(), "tools\\mimetex\\mimetex.exe")

	
	@property
	def useShellPipe (self):
		"""
		Значение параметра shell при создании класса Popen
		"""
		return False



class MimeTexLinux (MimeTex):
	"""
	Класс для работы с mimeTex под Linux
	"""
	@property
	def mimeTexPath (self):
		return "mimetex"


	@property
	def useShellPipe (self):
		"""
		Значение параметра shell при создании класса Popen
		"""
		return False
