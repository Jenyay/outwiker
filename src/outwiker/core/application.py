#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gettext

from .i18n import init_i18n
from .config import Config, getConfigPath
from .event import Event
from .recent import RecentWiki
from .pluginsloader import PluginsLoader
from gui.guiconfig import GeneralGuiConfig


class ApplicationParams (object):
	def __init__ (self):
		# Открытая в данный момент wiki
		self.__wikiroot = None

		# Главное окно приложения
		self.__mainWindow = None
		self.config = None
		self.recentWiki = None
		self.plugins = PluginsLoader (self)
		self.__createEvents()

	
	def init (self, configFilename):
		"""
		Инициализировать конфиг и локаль
		"""
		self.config = Config (configFilename)
		self.recentWiki = RecentWiki (self.config)
		self.__initLocale()


	@property
	def wikiroot (self):
		return self.__wikiroot


	@wikiroot.setter
	def wikiroot (self, value):
		self.onWikiClose (self.__wikiroot)

		if self.__wikiroot != None:
			self.__unbindWikiEvents (self.__wikiroot)

		self.__wikiroot = value

		if self.__wikiroot != None:
			self.__bindWikiEvents (self.__wikiroot)

		self.onWikiOpen (self.__wikiroot)


	@property
	def mainWindow (self):
		return self.__mainWindow


	@mainWindow.setter
	def mainWindow (self, value):
		self.__mainWindow = value


	def __bindWikiEvents (self, wiki):
		wiki.onPageSelect += self.onPageSelect
		wiki.onPageUpdate += self.onPageUpdate
		wiki.onTreeUpdate += self.onTreeUpdate
		wiki.onStartTreeUpdate += self.onStartTreeUpdate
		wiki.onEndTreeUpdate += self.onEndTreeUpdate
		wiki.onPageOrderChange += self.onPageOrderChange
		wiki.onPageRename += self.onPageRename
		wiki.onPageCreate += self.onPageCreate
		wiki.onPageRemove += self.onPageRemove
		wiki.bookmarks.onBookmarksChanged += self.onBookmarksChanged


	def __unbindWikiEvents (self, wiki):
		wiki.onPageSelect -= self.onPageSelect
		wiki.onPageUpdate -= self.onPageUpdate
		wiki.onTreeUpdate -= self.onTreeUpdate
		wiki.onStartTreeUpdate -= self.onStartTreeUpdate
		wiki.onEndTreeUpdate -= self.onEndTreeUpdate
		wiki.onPageOrderChange -= self.onPageOrderChange
		wiki.onPageRename -= self.onPageRename
		wiki.onPageCreate -= self.onPageCreate
		wiki.onPageRemove -= self.onPageRemove
		wiki.bookmarks.onBookmarksChanged -= self.onBookmarksChanged


	@property
	def selectedPage (self):
		"""
		Вернуть текущую страницу или None, если страница не выбрана или вики не открыта
		"""
		if self.__wikiroot == None:
			return None

		return self.__wikiroot.selectedPage


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

		# Событие вызывается после создания википарсера (Parser), но до его использования
		# Параметры: экземпляр Parser
		self.onWikiParserPrepare = Event ()


	def __initLocale (self):
		generalConfig = GeneralGuiConfig (self.config)
		language = generalConfig.languageOption.value

		try:
			init_i18n (language)
		except IOError, e:
			print u"Can't load language: %s" % language


Application = ApplicationParams()
