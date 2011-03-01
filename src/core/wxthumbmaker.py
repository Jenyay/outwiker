#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

import wx

from core.thumbexception import ThumbException


class WxThumbmaker (object):
	def __init__ (self):
		pass


	def thumbByWidth (self, fname_src, width_res, fname_res):
		"""
		Создать превьюшку определенной ширины
		"""
		if not os.path.exists (fname_src):
			raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src) )

		image_src = wx.Image (fname_src)
		width_src = image_src.GetWidth()
		height_src = image_src.GetHeight()

		scale = float (width_res) / float (width_src)
		height_res = int (height_src * scale)

		image_src.Rescale (width_res, height_res, wx.IMAGE_QUALITY_HIGH)
		image_src.SaveFile (fname_res, self.__getImageType (fname_res) )
	

	def thumbByHeight (self, fname_src, height_res, fname_res):
		"""
		Создать превьюшку определенной высоты
		"""
		if not os.path.exists (fname_src):
			raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src) )

		image_src = wx.Image (fname_src)
		width_src = image_src.GetWidth()
		height_src = image_src.GetHeight()

		scale = float (height_res) / float (height_src)
		width_res = int (width_src * scale)

		image_src.Rescale (width_res, height_res, wx.IMAGE_QUALITY_HIGH)
		image_src.SaveFile (fname_res, self.__getImageType (fname_res) )
	

	def thumbByMaxSize (self, fname_src, maxsize_res, fname_res):
		"""
		Создать превьюшку с заданным максимальным размером
		"""
		if not os.path.exists (fname_src):
			raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src) )

		image_src = wx.Image (fname_src)

		width_src = image_src.GetWidth()
		height_src = image_src.GetHeight()

		if width_src > height_src:
			self.thumbByWidth (fname_src, maxsize_res, fname_res)
		else:
			self.thumbByHeight (fname_src, maxsize_res, fname_res)
	

	def __getImageType (self, fname):
		if fname.lower().endswith (".jpg") or fname.lower().endswith (".jpeg"):
			return wx.BITMAP_TYPE_JPEG

		if fname.lower().endswith (".bmp"):
			return wx.BITMAP_TYPE_BMP

		if fname.lower().endswith (".png"):
			return wx.BITMAP_TYPE_PNG

		if fname.lower().endswith (".tif") or fname.lower().endswith (".tiff"):
			return wx.BITMAP_TYPE_TIF
