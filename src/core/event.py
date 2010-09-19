#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Event:
	"""
	Класс событий
	"""
	def __init__ (self):
		self.handlers = set()

	def _handle (self, handler):
		self.handlers.add(handler)
		return self

	def _unhandle (self, handler):
		try:
			self.handlers.remove(handler)
		except:
			raise ValueError("Handler is not handling this event, so cannot unhandle it.")
		return self

	def _run (self, *args, **kargs):
		for handler in self.handlers:
			handler(*args, **kargs)

	def getHandlerCount (self):
		return 

	__iadd__ = _handle
	__isub__ = _unhandle
	__call__ = _run

	def __len__ (self):
		return len (self.handlers)

