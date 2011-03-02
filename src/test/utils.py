#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Вспомогательные функции для тестов
"""

import os
import shutil

import wx

def removeWiki (path):
	"""
	Удалить вики из указанной папки
	"""
	if os.path.exists (path):
		try:
			shutil.rmtree (path)
		except OSError:
			shutil.rmtree (path)


def getImageSize (fname):
	"""
	Получить размер картинки. 
	Возвращает кортеж (ширина, высота)
	"""
	image = wx.Image (fname)
	width = image.GetWidth()
	height = image.GetHeight()

	return (width, height)

