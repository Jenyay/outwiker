#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os


def getHtmlRender (parent):
	"""
	Возвращает используемый HTML-рендер
	"""
	if os.name == "nt":
		from htmlrenderwx import HtmlRenderWX
		return HtmlRenderWX (parent)
	else:
		import htmlrenderwebkit
		return htmlrenderwebkit.HtmlRenderWebKit (parent)
