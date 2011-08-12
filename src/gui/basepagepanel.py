#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os.path

import wx

import core.commands


class BasePagePanel (wx.Panel):
	"""
	Базовый класс для панелей представления страниц
	"""
	__metaclass__ = ABCMeta

	def __init__ (self, parent, *args, **kwds):
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, parent, *args, **kwds)

		self._currentpage = None


	###############################################
	# Методы, которые обязательно надо перегрузить
	###############################################

	@abstractmethod
	def Print (self):
		"""
		Вызов печати страницы
		"""
		pass


	@abstractmethod
	def UpdateView (self, page):
		"""
		Обновление страницы
		"""
		pass


	@abstractmethod
	def Save (self):
		"""
		Сохранить страницу
		"""
		pass


	@abstractmethod
	def Clear (self):
		"""
		Убрать за собой. Удалить добавленные элементы интерфейса и отписаться от событий
		"""
		pass

	##################################################


	###############################################################################################
	# Методы, которые в базовом классе ничего не делают, но которые может понадобиться перегрузить
	###############################################################################################

	def onAttachmentPaste (self, fnames):
		"""
		Пользователь хочет вставить ссылки на приаттаченные файлы
		"""
		pass


	def removeGui (self):
		"""
		Убрать за собой элементы управления
		"""
		pass

	###################################################

	@property
	def page (self):
		return self._currentpage


	@page.setter
	def page (self, page):
		self.Save()
		self._currentpage = page

		if not os.path.exists (page.path):
			core.commands.MessageBox (
					_(u"Page %s not found. It is recommended to update the wiki") % self.page.title,
					_("Error"), wx.OR | wx.ICON_ERROR )
			return

		self.UpdateView (page)


	def Close (self):
		"""
		Закрытие панели. 
		Вызывать вручную!!!
		"""
		self.Save()
		self.CloseWithoutSave()
	

	def CloseWithoutSave (self):
		"""
		Закрытие панели без сохранения. 
		"""
		self.Clear()
		wx.Panel.Close (self)
		self.Destroy()
