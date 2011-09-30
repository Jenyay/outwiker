#!/usr/bin/env python
#-*- coding: utf-8 -*-


import wx

import gui.TextEditor
from outwiker.core.application import Application


class HtmlTextEditor (gui.TextEditor.TextEditor):
	def __init__(self, *args, **kwds):
		gui.TextEditor.TextEditor.__init__(self, *args, **kwds)

		self._htmlStylesSection = "HtmlStyles"
		self.setupHtmlStyles(self.textCtrl)

	
	def setupHtmlStyles (self, textCtrl):
		# Значения по умолчанию для стилей
		stylesdefault = {
				wx.stc.STC_H_TAG: "fore:#000080,bold",
				wx.stc.STC_H_TAGUNKNOWN: "fore:#FF0000",
				wx.stc.STC_H_ATTRIBUTE: "fore:#008080",
				wx.stc.STC_H_ATTRIBUTEUNKNOWN: "fore:#FF0000",
				wx.stc.STC_H_NUMBER: "fore:#000000",
				wx.stc.STC_H_DOUBLESTRING: "fore:#0000FF",
				wx.stc.STC_H_SINGLESTRING: "fore:#0000FF",
				wx.stc.STC_H_COMMENT: "fore:#12B535"
				}

		# Устанавливаемые стили
		styles = {}
		
		try:
			styles = self.loadStyles()
		except:
			styles = stylesdefault
			self.saveStyles(styles)
		
		textCtrl.SetLexer (wx.stc.STC_LEX_HTML)
		textCtrl.StyleClearAll()

		for key in styles.keys():
			textCtrl.StyleSetSpec (key, styles[key])

		tags = u"a abbr acronym address applet area b base basefont \
			bdo big blockquote body br button caption center \
			cite code col colgroup dd del dfn dir div dl dt em \
			fieldset font form frame frameset h1 h2 h3 h4 h5 h6 \
			head hr html i iframe img input ins isindex kbd label \
			legend li link map menu meta noframes noscript \
			object ol optgroup option p param pre q s samp \
			script select small span strike strong style sub sup \
			table tbody td textarea tfoot th thead title tr tt u ul \
			var xml xmlns"


		attributes = u"abbr accept-charset accept accesskey action align alink \
			alt archive axis background bgcolor border \
			cellpadding cellspacing char charoff charset checked cite \
			class classid clear codebase codetype color cols colspan \
			compact content coords \
			data datafld dataformatas datapagesize datasrc datetime \
			declare defer dir disabled enctype event \
			face for frame frameborder \
			headers height href hreflang hspace http-equiv \
			id ismap label lang language leftmargin link longdesc \
			marginwidth marginheight maxlength media method multiple \
			name nohref noresize noshade nowrap \
			object onblur onchange onclick ondblclick onfocus \
			onkeydown onkeypress onkeyup onload onmousedown \
			onmousemove onmouseover onmouseout onmouseup \
			onreset onselect onsubmit onunload \
			profile prompt readonly rel rev rows rowspan rules \
			scheme scope selected shape size span src standby start style \
			summary tabindex target text title topmargin type usemap \
			valign value valuetype version vlink vspace width \
			text password checkbox radio submit reset \
			file hidden image"

		textCtrl.SetKeyWords (0, tags + attributes)
	

	def loadStyles (self):
		"""
		Загрузить стили из конфига
		"""
		config = Application.config

		styles = {}

		styles[wx.stc.STC_H_TAG] = config.get (self._htmlStylesSection, "tag")
		styles[wx.stc.STC_H_TAGUNKNOWN] = config.get (self._htmlStylesSection, "tag_unknoun")
		styles[wx.stc.STC_H_ATTRIBUTE] = config.get (self._htmlStylesSection, "attribute")
		styles[wx.stc.STC_H_ATTRIBUTEUNKNOWN] = config.get (self._htmlStylesSection, "attribute_unknown")
		styles[wx.stc.STC_H_NUMBER] = config.get (self._htmlStylesSection, "number")
		styles[wx.stc.STC_H_DOUBLESTRING] = config.get (self._htmlStylesSection, "doublestring")
		styles[wx.stc.STC_H_SINGLESTRING] = config.get (self._htmlStylesSection, "singlestring")
		styles[wx.stc.STC_H_COMMENT] = config.get (self._htmlStylesSection, "comment")

		return styles

	
	def saveStyles (self, styles):
		config = Application.config

		config.set (self._htmlStylesSection, "tag", styles[wx.stc.STC_H_TAG])
		config.set (self._htmlStylesSection, "tag_unknoun", styles[wx.stc.STC_H_TAGUNKNOWN])
		config.set (self._htmlStylesSection, "attribute", styles[wx.stc.STC_H_ATTRIBUTE])
		config.set (self._htmlStylesSection, "attribute_unknown", styles[wx.stc.STC_H_ATTRIBUTEUNKNOWN])
		config.set (self._htmlStylesSection, "number", styles[wx.stc.STC_H_NUMBER])
		config.set (self._htmlStylesSection, "doublestring", styles[wx.stc.STC_H_DOUBLESTRING])
		config.set (self._htmlStylesSection, "singlestring", styles[wx.stc.STC_H_SINGLESTRING])
		config.set (self._htmlStylesSection, "comment", styles[wx.stc.STC_H_COMMENT])
