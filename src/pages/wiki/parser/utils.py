#!/usr/bin/env python
# -*- coding: UTF-8 -*-

def noConvert (s, l, t):
	return t[0]


def replaceBreakes (text):
	lineBrake = u"[[<<]]"
	doubleBrake = "\\\\\\"

	result = text.replace (doubleBrake, "\n\n")
	result = result.replace (lineBrake, "\n")
	return result
