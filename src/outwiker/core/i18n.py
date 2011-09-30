#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import gettext

from .system import getCurrentDir


def init_i18n (language):
	langdir = os.path.join (getCurrentDir(), u'locale')

	try:
		lang = gettext.translation(u'outwiker', langdir, languages=[language])
		lang.install(unicode=1)
	except IOError:
		lang = gettext.translation(u'outwiker', langdir, languages=["en"])
		lang.install(unicode=1)
		raise


def isLangDir (root, folder):
	"""
	Возвращает True, если path - путь до папки с локализацией
	"""
	path = os.path.join (root, folder)

	if not os.path.isdir (path):
		return False

	messdir = os.path.join (path, u"LC_MESSAGES")
	if not os.path.exists(messdir) or not os.path.isdir (messdir):
		return False

	langfile = os.path.join (messdir, u"outwiker.mo")
	if not os.path.exists (langfile):
		return False

	return True


def getLanguages ():
	"""
	Получить список всех языков, находящихся в папке locale
	"""
	langdir = os.path.join (getCurrentDir(), u'locale')

	languages = []
	for folder in os.listdir (langdir):
		if isLangDir (langdir, folder):
			languages.append (folder)

	return languages



