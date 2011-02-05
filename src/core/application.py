#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gettext

from core.config import GeneralConfig, getConfigPath
import core.i18n
from core.event import Event


class Application (object):
	def __init__ (self, configFilename):
		pass

	
	@staticmethod
	def init (configFilename):
		Application.config = GeneralConfig (configFilename)
		Application.__initLocale()
		Application.__createEvents()
		Application.wikiroot = None
	

	@staticmethod
	def __createEvents ():
		"""
		Создать статические члены для событий
		"""
		# Обновление страницы
		# Параметры: sender
		Application.onPageUpdate = Event()

		# Создание страницы
		# Параметры: sender
		Application.onPageCreate = Event()

		# Обновление дерева
		# Параметры: sender - из-за кого обновляется дерево
		Application.onTreeUpdate = Event()
		
		# Выбор новой страницы
		# Параметры: новая выбранная страница
		Application.onPageSelect = Event()

		# Пользователь хочет скопировать выбранные файлы в страницу
		# Параметры: fnames - выбранные имена файлов (basename без путей)
		Application.onAttachmentPaste = Event()

		# Изменение списка закладок
		# Параметр - экземпляр класса Bookmarks
		Application.onBookmarksChanged = Event()

		# Удаленеи страницы
		# Параметр - удаленная страница
		Application.onPageRemove = Event()

		# Переименование страницы.
		# Параметры: page - переименованная страница, oldSubpath - старый относительный путь до страницы
		Application.onPageRename = Event()

		# Начало сложного обновления дерева
		# Параметры: root - корень дерева
		Application.onStartTreeUpdate = Event()

		# Конец сложного обновления дерева
		# Параметры: root - корень дерева
		Application.onEndTreeUpdate = Event()

		# Вызывается перед тем, как закрыть открытую вики или открыть другую вики
		# Параметры: root - корень дерева
		Application.onWikiClose = Event()
		
		# Начало рендеринга HTML
		# Параметры: 
		# page - страница, которую рендерят
		# htmlView - окно, где будет представлен HTML
		Application.onHtmlRenderingBegin = Event()
		
		# Завершение рендеринга HTML
		# Параметры: 
		# page - страница, которую рендерят
		# htmlView - окно, где будет представлен HTML
		Application.onHtmlRenderingEnd = Event()

		# Изменение настроек редактора
		# Параметры: нет
		Application.onEditorConfigChange = Event()

		# Изменение настроек главного окна
		# Параметры: нет
		Application.onMainWindowConfigChange = Event()

		# Изменение порядка страниц
		# Параметры: page - страница, положение которой изменили
		Application.onPageOrderChange = Event()

		# Событие на принудительное сохранение состояния страницы
		# Например, при потере фокуса приложением.
		# Параметры: нет
		Application.onForceSave = Event()


	@staticmethod
	def __initLocale ():
		language = Application.config.languageOption.value

		try:
			core.i18n.init_i18n (language)
		except IOError, e:
			print u"Can't load language: %s" % language
