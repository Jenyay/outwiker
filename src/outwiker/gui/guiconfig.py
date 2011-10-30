#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import locale

import wx

from outwiker.core.config import StringOption, BooleanOption, IntegerOption, ListOption
from outwiker.core.system import getDefaultLanguage


class GeneralGuiConfig (object):
	"""
	Класс для хранения основных настроек
	"""
	def __init__ (self, config):
		self.config = config

		self.languageOption = StringOption (self.config, u"General", u"language", getDefaultLanguage())

		# Спрашивать подтверждение выхода?
		self.DEFAULT_ASK_BEFORE_EXIT = True
		self.askBeforeExitOption = BooleanOption (self.config, u"General", u"AskBeforeExit", self.DEFAULT_ASK_BEFORE_EXIT)

		# Интервал, через которое происходит автосохранение страницы. Если значение <= 0, значит автосохранение отключено
		self.DEFAULT_AUTOSAVE_INTERVAL = 3
		self.autosaveIntervalOption = IntegerOption (self.config, u"General", u"AutosaveInterval", self.DEFAULT_AUTOSAVE_INTERVAL)

		# Количество последних открытых вики
		self.DEFAULT_RECENT_WIKI_COUNT = 5
		self.historyLengthOption = IntegerOption (self.config, u"RecentWiki", u"maxcount", self.DEFAULT_RECENT_WIKI_COUNT)

		# Открывать последнуюю открытую вики при старте?
		self.DEFAULT_RECENT_AUTOOPEN = False
		self.autoopenOption = BooleanOption (self.config, u"RecentWiki", u"AutoOpen", self.DEFAULT_RECENT_AUTOOPEN)


class PluginsConfig (object):
	"""
	Класс для хранения настроек, связанных с плагинами
	"""
	def __init__ (self, config):
		self.config = config

		self.pluginsConfigSection = u"Plugins"
		self.disabledPluginsParam = u"Disabled"

		self.disabledPlugins = ListOption (self.config, 
				self.pluginsConfigSection,
				self.disabledPluginsParam,
				[],
				separator=u";")



class TrayConfig (object):
	"""
	Класс для хранения настроек, связанных с иконками в трее
	"""
	def __init__ (self, config):
		self.config = config

		# Сворачивать в трей?
		self.DEFAULT_MINIMIZE_TO_TRAY = True
		self.minimizeOption = BooleanOption (self.config, u"General", u"MinimizeToTray", self.DEFAULT_MINIMIZE_TO_TRAY)

		# Запускаться свернутым?
		self.DEFAULT_START_ICONIZED = False
		self.startIconizedOption = BooleanOption (self.config, u"General", u"StartIconized", self.DEFAULT_START_ICONIZED)

		# Всегда показывать иконку в трее?
		self.DEFAULT_ALWAYS_SHOW_TRAY_ICON = False
		self.alwaysShowTrayIconOption = BooleanOption (self.config, u"General", u"AlwaysShowTrayIcon", self.DEFAULT_ALWAYS_SHOW_TRAY_ICON)



class EditorConfig (object):
	"""
	Класс для хранения настроек редактора
	"""
	def __init__ (self, config):
		self.config = config

		# Показывать номера строк в редакторе?
		self.DEFAULT_SHOW_LINE_NUMBERS = False
		self.lineNumbersOption = BooleanOption (self.config, u"General", u"ShowLineNumbers", self.DEFAULT_SHOW_LINE_NUMBERS)

		# Размер табуляции
		self.DEFAULT_TAB_WIDTH = 4
		self.tabWidthOption = IntegerOption (self.config, u"General", u"TabWidth", self.DEFAULT_TAB_WIDTH)
		
		# Размер шрифта
		self.DEFAULT_FONT_SIZE = 10
		self.fontSizeOption = IntegerOption (self.config, u"Font", u"size", self.DEFAULT_FONT_SIZE)

		# Начертание шрифта
		self.DEFAULT_FONT_NAME = u""
		self.fontFaceNameOption = StringOption (self.config, u"Font", u"FaceName", self.DEFAULT_FONT_NAME)

		self.DEFAULT_FONT_BOLD = False
		self.fontIsBold = BooleanOption (self.config, "Font", "bold", self.DEFAULT_FONT_BOLD)

		self.DEFAULT_FONT_ITALIC = False
		self.fontIsItalic = BooleanOption (self.config, "Font", "italic", self.DEFAULT_FONT_ITALIC)


class HtmlRenderConfig (object):
	"""
	Класс для хранения настроек HTML-рендера
	"""
	def __init__ (self, config):
		self.config = config

		self.DEFAULT_FONT_SIZE = 10
		self.fontSizeOption = IntegerOption (self.config, u"HTML", u"FontSize", self.DEFAULT_FONT_SIZE)

		self.DEFAULT_FONT_NAME = u"Verdana"
		self.fontFaceNameOption = StringOption (self.config, u"HTML", u"FontFaceName", self.DEFAULT_FONT_NAME)

		self.DEFAULT_FONT_BOLD = False
		self.fontIsBold = BooleanOption (self.config, "HTML", "FontBold", self.DEFAULT_FONT_BOLD)

		self.DEFAULT_FONT_ITALIC = False
		self.fontIsItalic = BooleanOption (self.config, "HTML", "FontItalic", self.DEFAULT_FONT_ITALIC)

		self.DEFAULT_USER_STYLE = u""
		self.userStyleOption = StringOption (self.config, u"HTML", u"UserStyle", self.DEFAULT_USER_STYLE)


class TextPrintConfig (object):
	"""
	Класс для хранения настроек печати текста
	"""
	def __init__ (self, config):
		self.config = config

		# Настройки шрифта
		self.DEFAULT_FONT_NAME = u"Arial"
		self.fontFaceNameOption = StringOption (self.config, u"Print", u"FontFaceName", self.DEFAULT_FONT_NAME)

		self.DEFAULT_FONT_SIZE = 10
		self.fontSizeOption = IntegerOption (self.config, u"Print", u"FontSize", self.DEFAULT_FONT_SIZE)

		self.DEFAULT_FONT_BOLD = False
		self.fontIsBold = BooleanOption (self.config, "Print", "FontBold", self.DEFAULT_FONT_BOLD)

		self.DEFAULT_FONT_ITALIC = False
		self.fontIsItalic = BooleanOption (self.config, "Print", "FontItalic", self.DEFAULT_FONT_ITALIC)


		self.DEFAULT_PAPPER_SIZE = wx.PAPER_A4
		self.paperId = IntegerOption (self.config, u"Print", u"PaperId", self.DEFAULT_PAPPER_SIZE)

		self.DEFAULT_MARGIN_TOP = 20
		self.marginTop = IntegerOption (self.config, u"Print", u"MarginTop", self.DEFAULT_MARGIN_TOP)

		self.DEFAULT_MARGIN_BOTTOM = 20
		self.marginBottom = IntegerOption (self.config, u"Print", u"MarginBottom", self.DEFAULT_MARGIN_BOTTOM)

		self.DEFAULT_MARGIN_LEFT = 20
		self.marginLeft = IntegerOption (self.config, u"Print", u"MarginLeft", self.DEFAULT_MARGIN_LEFT)
		
		self.DEFAULT_MARGIN_RIGHT = 20
		self.marginRight = IntegerOption (self.config, u"Print", u"MarginRight", self.DEFAULT_MARGIN_RIGHT)



class MainWindowConfig (object):
	"""
	Класс для хранения настроек главного окна
	"""
	def __init__ (self, config):
		self.config = config

		self.DEFAULT_TITLE_FORMAT = u"{page} - {file} - OutWiker"
		self.titleFormatOption = StringOption (self.config, u"MainWindow", u"Title", self.DEFAULT_TITLE_FORMAT)

		self.DEFAULT_WIDTH = 800
		self.WidthOption = IntegerOption (self.config, u"MainWindow", u"width", self.DEFAULT_WIDTH)

		self.DEFAULT_HEIGHT = 680
		self.HeightOption = IntegerOption (self.config, u"MainWindow", u"height", self.DEFAULT_HEIGHT)

		self.DEFAULT_XPOS = 0
		self.XPosOption = IntegerOption (self.config, u"MainWindow", u"xpos", self.DEFAULT_XPOS)

		self.DEFAULT_YPOS = 0
		self.YPosOption = IntegerOption (self.config, u"MainWindow", u"ypos", self.DEFAULT_YPOS)

		self.DEFAULT_FULLSCREEN = False
		self.FullscreenOption = BooleanOption (self.config, u"MainWindow", u"fullscreen", self.DEFAULT_FULLSCREEN)



class TreeConfig (object):
	"""
	Класс для хранения настроек панели с деревом
	"""
	def __init__ (self, config):
		self.config = config

		self.DEFAULT_WIDTH = 250
		self.treeWidthOption = IntegerOption (self.config, u"MainWindow", u"TreeWidth", self.DEFAULT_WIDTH)

		self.DEFAULT_HEIGHT = 250
		self.treeHeightOption = IntegerOption (self.config, u"MainWindow", u"TreeHeight", self.DEFAULT_HEIGHT)

		# Параметры панели с деревом
		self.DEFAULT_PANE_OPTIONS = ""
		self.treePaneOption = StringOption (self.config, u"MainWindow", u"TreePane", self.DEFAULT_PANE_OPTIONS)



class AttachConfig (object):
	"""
	Класс для хранения настроек панели с вложенными файлами
	"""
	def __init__ (self, config):
		self.config = config

		self.DEFAULT_WIDTH = 250
		self.attachesWidthOption = IntegerOption (self.config, u"MainWindow", u"AttachesWidth", self.DEFAULT_WIDTH)

		self.DEFAULT_HEIGHT = 150
		self.attachesHeightOption = IntegerOption (self.config, u"MainWindow", u"AttachesHeight", self.DEFAULT_HEIGHT)

		self.DEFAULT_PANE_OPTIONS = u""
		self.attachesPaneOption = StringOption (self.config, u"MainWindow", u"AttachesPane", self.DEFAULT_PANE_OPTIONS)

