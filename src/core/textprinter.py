#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cgi

import wx
import wx.html

import core.commands


class TextPrinter (object):
	"""
	Интерфейс для печати текстовых страниц
	"""
	def __init__ (self, parent):
		self.parent = parent

		self.normalFont = u"Arial"
		self.fixedFont = u"Courier New"

		# Поля на странице: верхнее, нижнее, левое, правое, расстояние между шапкой/подвалом и текстом в мм
		self.margins = (20.0, 20.0, 20.0, 20.0, 5.0)

		self.htmltemplate = ur"""<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>
</HEAD>
<BODY>
{content}
</BODY>
</HTML>"""


	def _preparetext (self, text):
		"""
		Подготовить текст с учетом того, что печататься будет HTML
		"""
		# Заменим спецсимволы HTML и установим переводы строк
		newtext = cgi.escape (text, True)
		newtext = newtext.replace ("\n\n", "<P>")
		newtext = newtext.replace ("\n", "<BR>")

		result = self.htmltemplate.format (content=newtext)
		return result


	def _getPrintout (self, htmltext):
		printout = wx.html.HtmlPrintout()
		printout.SetFonts(self.normalFont, self.fixedFont)
		printout.SetMargins (self.margins[0], self.margins[1], self.margins[2], self.margins[3], self.margins[4])
		printout.SetHtmlText(htmltext)
		return printout


	def _getPrintData (self):
		"""
		Получить параметры печати (страницы) по умолчанию
		"""
		pd = wx.PrintData()
		pd.SetPaperId(wx.PAPER_A4)
		pd.SetOrientation (wx.PORTRAIT)
		return pd


	def _getPrintDialogData (self, printdata):
		"""
		Получить настройки диалога печати по умолчанию
		"""
		pdd = wx.PrintDialogData (printdata)
		pdd.SetAllPages(True)
		pdd.EnableSelection (False)
		return pdd


	def printout (self, text):
		htmltext = self._preparetext (text)
		printout = self._getPrintout (htmltext)
		pd = self._getPrintData()
		pdd = self._getPrintDialogData (pd)

		# По-хорошему, надо было бы примерно таким образом (еще учесть предпросмотр), но под Linux'ом падает libgnomeprint
		#dlg = wx.PrintDialog (self.parent, None)
		#if dlg.ShowModal () == wx.ID_OK:
		#	pdd_new = dlg.GetPrintDialogData()
		#	printer = wx.Printer(pdd_new)
		#	printer.Print(self.parent, printout, False)

		printer = wx.Printer(pdd)
		printer.Print(self.parent, printout, True)

		if printer.GetLastError() == wx.PRINTER_ERROR:
			core.commands.MessageBox (_(u"Printing error"), _("Error"), wx.OK | wx.ICON_ERROR, self.parent)
