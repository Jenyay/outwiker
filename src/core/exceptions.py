#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class OutWikerException (BaseException):
	def __init__ (self):
		BaseException.__init__(self)


class TreeException (OutWikerException):
	def __init__ (self):
		OutWikerException.__init__(self)


class DublicateTitle (TreeException):
	def __init__ (self):
		TreeException.__init__(self)
