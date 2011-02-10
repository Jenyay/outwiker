#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gettext

from core.config import GeneralConfig, getConfigPath
import core.i18n
from core.event import Event


class ApplicationParams (object):
	def __init__ (self):
		# Открытая в данный момент wiki
		self._wikiroot = None
		self.config = None
		self.__createEvents()

	
	def init (self, configFilename):
		"""
		Инициализировать конфиг и локаль
		"""
		self.config = GeneralConfig (configFilename)
		self.__initLocale()


	@property
	def wikiroot (self):
		return self._wikiroot


	@wikiroot.setter
	def wikiroot (self, value):
		self.onWikiClose (self._wikiroot)
		self._wikiroot = value
		self.onWikiOpen (self._wikiroot)


	def __createEvents (self):
		"""
		Создать статические члены для событий
		"""
		# Открытие вики
		# Параметр: root - корень новой вики (возможно, None)
		self.onWikiOpen = Event()

		# Закрытие вики
		# Параметр: root - корень закрываемой вики (возможно, None)
		self.onWikiClose = Event()

		# Обновление страницы
		# Параметры: sender
		self.onPageUpdate = Event()

		# Создание страницы
		# Параметры: sender
		self.onPageCreate = Event()

		# Обновление дерева
		# Параметры: sender - из-за кого обновляется дерево
		self.onTreeUpdate = Event()
		
		# Выбор новой страницы
		# Параметры: новая выбранная страница
		self.onPageSelect = Event()

		# Пользователь хочет скопировать выбранные файлы в страницу
		# Параметры: fnames - выбранные имена файлов (basename без путей)
		self.onAttachmentPaste = Event()

		# Изменение списка закладок
		# Параметр - экземпляр класса Bookmarks
		self.onBookmarksChanged = Event()

		# Удаленеи страницы
		# Параметр - удаленная страница
		self.onPageRemove = Event()

		# Переименование страницы.
		# Параметры: page - переименованная страница, oldSubpath - старый относительный путь до страницы
		self.onPageRename = Event()

		# Начало сложного обновления дерева
		# Параметры: root - корень дерева
		self.onStartTreeUpdate = Event()

		# Конец сложного обновления дерева
		# Параметры: root - корень дерева
		self.onEndTreeUpdate = Event()

		# Начало рендеринга HTML
		# Параметры: 
		# page - страница, которую рендерят
		# htmlView - окно, где будет представлен HTML
		self.onHtmlRenderingBegin = Event()
		
		# Завершение рендеринга HTML
		# Параметры: 
		# page - страница, которую рендерят
		# htmlView - окно, где будет представлен HTML
		self.onHtmlRenderingEnd = Event()

		# Изменение настроек редактора
		# Параметры: нет
		self.onEditorConfigChange = Event()

		# Изменение настроек главного окна
		# Параметры: нет
		self.onMainWindowConfigChange = Event()

		# Изменение порядка страниц
		# Параметры: page - страница, положение которой изменили
		self.onPageOrderChange = Event()

		# Событие на принудительное сохранение состояния страницы
		# Например, при потере фокуса приложением.
		# Параметры: нет
		self.onForceSave = Event()


	def __initLocale (self):
		language = self.config.languageOption.value

		try:
			core.i18n.init_i18n (language)
		except IOError, e:
			print u"Can't load language: %s" % language


Application = ApplicationParams()
