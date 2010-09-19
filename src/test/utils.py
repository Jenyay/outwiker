#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Вспомогательные функции для тестов
"""

import os
import shutil

def removeWiki (path):
	"""
	Удалить вики из указанной папки
	"""
	if os.path.exists (path):
		try:
			shutil.rmtree (path)
		except OSError:
			shutil.rmtree (path)
