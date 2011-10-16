#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx

class ButtonsDialog (wx.Dialog):
	"""
	Диалог с пользовательскими кнопками.
	Метод ShowModal возвращает номер (начиная от 0) нажатой кнопки
	"""
	def __init__ (self, parent, message, caption, buttons, default=0, cancel=-1):
		"""
		parent - родитель диалога
		message - сообщение, отображаемое в диалоге
		caption - заголовок диалога
		buttons - список строк. Каждая строка соответствует кнопке с соответствующей надписью
		default - номер кнопки, выбранной по умолчанию
		cancel - номер кнопки, срабатывающей при нажатии Esc
		"""
		assert len (buttons) > 0
		assert default < len (buttons)
		assert cancel < len (buttons)

		wx.Dialog.__init__ (self, parent)

		self.__default = default
		self.__cancel = cancel

		self.SetTitle (caption)
		self.__textLabel = wx.StaticText(self, -1, message, style=wx.ALIGN_CENTRE)

		self.__createButtons (buttons, default, cancel)
		self.__do_layout()


	def __createButtons (self, buttons, default, cancel):
		"""Создание кнопок"""
		self.__buttons = [wx.Button (self, index, text) for text, index in zip (buttons, range (len (buttons)) )]

		if default >= 0:
			self.SetAffirmativeId (self.__buttons[default].GetId())
			self.__buttons[default].SetFocus()

		if cancel >= 0:
			self.SetEscapeId (self.__buttons[cancel].GetId())

		self.Bind(wx.EVT_BUTTON, self.__onButton)


	def __onButton (self, event):
		self.EndModal(event.GetId())


	def __do_layout(self):
		sizer_1 = wx.BoxSizer(wx.VERTICAL)
		sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

		sizer_1.Add(self.__textLabel, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_CENTER_HORIZONTAL, 4)
		
		for button in self.__buttons:
			sizer_2.Add(button, 0, wx.ALL, 2)

		sizer_1.Add(sizer_2, 1, wx.EXPAND|wx.ALIGN_CENTER_HORIZONTAL, 0)
		self.SetSizer(sizer_1)
		sizer_1.Fit(self)
		self.Layout()

