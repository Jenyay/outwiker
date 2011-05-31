#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from core.config import StringOption, BooleanOption, IntegerOption

class GeneralGuiConfig (object):
	"""
	Класс для хранения основных настроек
	"""
	def __init__ (self, config):
		self.config = config

		self.languageOption = StringOption (self.config, u"General", u"language", u"en")
		self.askBeforeExitOption = BooleanOption (self.config, u"General", u"AskBeforeExit", True)
		self.historyLengthOption = IntegerOption (self.config, u"RecentWiki", u"maxcount", 5)
		self.autoopenOption = BooleanOption (self.config, u"RecentWiki", u"AutoOpen", False)


class TrayConfig (object):
	"""
	Класс для хранения настроек, связанных с иконками в трее
	"""
	def __init__ (self, config):
		self.config = config

		self.minimizeOption = BooleanOption (self.config, u"General", u"MinimizeToTray", True)
		self.startIconizedOption = BooleanOption (self.config, u"General", u"StartIconized", False)
		self.alwaysShowTrayIconOption = BooleanOption (self.config, u"General", u"AlwaysShowTrayIcon", False)



class EditorConfig (object):
	"""
	Класс для хранения настроек редактора
	"""
	def __init__ (self, config):
		self.config = config

		self.lineNumbersOption = BooleanOption (self.config, u"General", u"ShowLineNumbers", False)
		self.tabWidthOption = IntegerOption (self.config, u"General", u"TabWidth", 4)
		
		self.fontSizeOption = IntegerOption (self.config, u"Font", u"size", 10)
		self.fontFaceNameOption = StringOption (self.config, u"Font", u"FaceName", "")
		self.fontIsBold = BooleanOption (self.config, "Font", "bold", False)
		self.fontIsItalic = BooleanOption (self.config, "Font", "italic", False)


class HtmlRenderConfig (object):
	"""
	Класс для хранения настроек HTML-рендера
	"""
	def __init__ (self, config):
		self.config = config

		self.fontSizeOption = IntegerOption (self.config, u"HTML", u"FontSize", 10)
		self.fontFaceNameOption = StringOption (self.config, u"HTML", u"FontFaceName", "Verdana")
		self.fontIsBold = BooleanOption (self.config, "HTML", "FontBold", False)
		self.fontIsItalic = BooleanOption (self.config, "HTML", "FontItalic", False)



class MainWindowConfig (object):
	"""
	Класс для хранения настроек главного окна
	"""
	def __init__ (self, config):
		self.config = config

		# Главное окно
		self.titleFormatOption = StringOption (self.config, u"MainWindow", u"Title", u"{page} - {file} - OutWiker")
		self.WidthOption = IntegerOption (self.config, u"MainWindow", u"width", 800)
		self.HeightOption = IntegerOption (self.config, u"MainWindow", u"height", 680)
		self.XPosOption = IntegerOption (self.config, u"MainWindow", u"xpos", 0)
		self.YPosOption = IntegerOption (self.config, u"MainWindow", u"ypos", 0)
		self.FullscreenOption = BooleanOption (self.config, u"MainWindow", u"fullscreen", False)



class TreeConfig (object):
	"""
	Класс для хранения настроек панели с деревом
	"""
	def __init__ (self, config):
		self.config = config

		self.treeWidthOption = IntegerOption (self.config, u"MainWindow", u"TreeWidth", 250)
		self.treeHeightOption = IntegerOption (self.config, u"MainWindow", u"TreeHeight", 250)
		self.treePaneOption = StringOption (self.config, u"MainWindow", u"TreePane", "")



class AttachConfig (object):
	"""
	Класс для хранения настроек панели с вложенными файлами
	"""
	def __init__ (self, config):
		self.config = config

		self.attachesWidthOption = IntegerOption (self.config, u"MainWindow", u"AttachesWidth", 250)
		self.attachesHeightOption = IntegerOption (self.config, u"MainWindow", u"AttachesHeight", 150)
		self.attachesPaneOption = StringOption (self.config, u"MainWindow", u"AttachesPane", "")

