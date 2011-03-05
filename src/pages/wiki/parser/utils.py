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
