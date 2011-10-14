#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import gettext

from .system import getCurrentDir
from outwiker.gui.guiconfig import GeneralGuiConfig


def init_i18n (language):
	langdir = os.path.join (getCurrentDir(), u'locale')

	lang = loadLanguage (language, langdir, u"outwiker")
	lang.install(unicode=1)


def loadLanguage (language, langdir, domain):
	"""
	Загрузить язык из указанной директории
	"""
	gettext.bindtextdomain (domain, langdir)
	gettext.textdomain (domain)

	try:
		lang = gettext.translation(domain, langdir, languages=[language])
	except IOError:
		lang = gettext.translation(domain, langdir, languages=["en"])
		
	return lang


def getLanguageFromConfig (config):
	"""
	Прочитать настройку языка из конфига
	"""
	generalConfig = GeneralGuiConfig (config)
	language = generalConfig.languageOption.value
	return language


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



