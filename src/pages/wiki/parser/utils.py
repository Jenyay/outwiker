#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from libs.pyparsing import NoMatch

def noConvert (s, l, t):
	return t[0]


def replaceBreakes (text):
	lineBrake = u"[[<<]]"
	doubleBrake = "\\\\\\"

	result = text.replace (doubleBrake, "\n\n")
	result = result.replace (lineBrake, "\n")
	return result


def concatenate (tokenlist):
	"""
	Склеить несколько токенов из списка
	"""
	if len (tokenlist) == 0:
		return NoMatch()

	result = tokenlist[0]
	for token in tokenlist[1:]:
		result |= token

	return result


def convertToHTML (opening, closing, parser):
	"""
	opening - открывающийся тег(и)
	closing - закрывающийся тег(и)
	parser - парсер, у которого берется токен wikiMarkup для преобразования содержимого между тегами
	"""
	def conversionParseAction(s,l,t):
		return opening + parser.wikiMarkup.transformString (t[0]) + closing
	return conversionParseAction


def isImage (fname):
	images_ext = [".png", ".bmp", ".gif", ".tif", ".tiff", ".jpg", ".jpeg"]

	for ext in images_ext:
		if fname.lower().endswith (ext):
			return True

	return False
