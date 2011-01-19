#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import core.system


def getConfigPath (dirname, fname):
	"""
	Вернуть полный путь до файла настроек.
	Поиск пути осуществляется следующим образом:
	1. Если в папке с программой есть файл настроек, то вернуть путь до него
	2. Иначе настройки будут храниться в домашней поддиректории. При этом создать директорию .outwiker в домашней директории.
	"""
	someDir = os.path.join (core.system.getCurrentDir(), fname)
	if os.path.exists (someDir):
		path = someDir
	else:
		homeDir = os.path.join (unicode (os.path.expanduser("~"), core.system.getOS().filesEncoding), dirname)
		if not os.path.exists (homeDir):
			os.mkdir (homeDir)

		path = os.path.join (homeDir, fname)

	return path


class Config (object):
	"""
	Оболочка над ConfigParser
	"""
	def __init__ (self, fname, readonly=False):
		"""
		fname -- имя файла конфига
		"""
		self.readonly = readonly
		self.fname = fname
		self.__config = ConfigParser.ConfigParser()

		self.__config.read (self.fname)
	

	def set (self, section, param, value):
		if self.readonly:
			return False

		section_encoded = section.encode ("utf8")
		if not self.__config.has_section (section_encoded):
			self.__config.add_section (section_encoded)

		self.__config.set (section_encoded, param.encode ("utf8"), unicode (value).encode ("utf8"))

		return self.save()


	def save (self):
		if self.readonly:
			return False

		with open (self.fname, "wb") as fp:
			self.__config.write (fp)

		return True
	
	
	def get (self, section, param):
		val = self.__config.get (section.encode ("utf8"), param.encode ("utf8"))
		return unicode (val, "utf8", "replace")

	
	def getint (self, section, param):
		return int (self.__config.get (section.encode ("utf8"), param.encode ("utf8")))

	def getbool (self, section, param):
		val = self.__config.get (section.encode ("utf8"), param.encode ("utf8"))

		return True if val.strip().lower() == "true" else False


	def remove_section (self, section):
		section_encoded = section.encode ("utf8")
		result1 = self.__config.remove_section (section_encoded)
		result2 = self.save()

		return result1 and result2


	def remove_option (self, section, option):
		section_encoded = section.encode ("utf8")
		option_encoded = option.encode ("utf8")

		result1 = self.__config.remove_option (section_encoded, option_encoded)
		result2 = self.save()

		return result1 and result2


	def has_section (self, section):
		section_encoded = section.encode ("utf8")
		return self.__config.has_section (section_encoded)


class StringOption (object):
	def __init__ (self, config, section, param, defaultValue):
		"""
		config - экземпляр класса core.Config
		section - секция для параметра конфига
		param - имя параметра конфига
		defaultValue - значение по умолчанию
		"""
		self.config = config
		self.section = section
		self.param = param
		self.defaultValue = defaultValue

		# Указатель на последнее возникшее исключение
		# Т.к. как правило исключения игнорируются, то это поле используется для отладкиы
		self.error = None

		self.loadParam (config)


	def loadParam (self, config):
		try:
			self.val = self._loadValue()
		except Exception as e:
			self.error = e
			self.val = self.defaultValue


	def _loadValue (self):
		"""
		Получить значение. В производных классах этот метод переопределяется
		"""
		return self.config.get (self.section, self.param)


	def _saveValue (self):
		self.config.set (self.section, self.param, self.val)
	

	@property
	def value (self):
		return self.val


	@value.setter
	def value (self, val):
		self.val = val
		self._saveValue()


class BooleanOption (StringOption):
	"""
	Булевская настройка.
	Элемент управления - wx.CheckBox
	"""
	def __init__ (self, config, section, param, defaultValue):
		StringOption.__init__ (self, config, section, param, defaultValue)


	def _loadValue (self):
		"""
		Получить значение. В производных классах этот метод переопределяется
		"""
		return self.config.getbool (self.section, self.param)


class IntegerOption (StringOption):
	"""
	Настройка для целых чисел.
	Элемент управления - wx.SpinCtrl
	"""
	def __init__ (self, config, section, param, defaultValue):
		StringOption.__init__ (self, config, section, param, defaultValue)


	def _loadValue (self):
		"""
		Получить значение. В производных классах этот метод переопределяется
		"""
		return self.config.getint (self.section, self.param)


class FontOption (object):
	def __init__ (self, config, 
			faceNameOption, 
			sizeOption,
			isBoldOption,
			isItalicOption):
		"""
		faceNameOption - экземепляр класса StringOption, где хранится значение начертания шрифта
		sizeOption - экземпляр класса IntegerOption, где хранится размер шрифта
		isBoldOption, isItalicOption - экземпляры класса BooleanOption
		"""
		self.faceName = faceNameOption
		self.size = sizeOption
		self.bold = isBoldOption
		self.italic = isItalicOption



class GeneralConfig (Config):
	"""
	Класс для хранения основных настроек
	"""
	def __init__ (self, fname, readonly=False):
		Config.__init__ (self, fname, readonly)
		self.languageOption = StringOption (self, u"General", u"language", u"en")

		# Список последних открытых файлов
		self.historyLengthOption = IntegerOption (self, u"RecentWiki", u"maxcount", 5)
		self.autoopenOption = BooleanOption (self, u"RecentWiki", u"AutoOpen", False)

		self.minimizeOption = BooleanOption (self, u"General", u"MinimizeToTray", True)
		self.startIconizedOption = BooleanOption (self, u"General", u"StartIconized", False)
		self.askBeforeExitOption = BooleanOption (self, u"General", u"AskBeforeExit", True)

		# Редактор
		self.lineNumbersOption = BooleanOption (self, u"General", u"ShowLineNumbers", False)
		
		fontSizeOption = IntegerOption (self, u"Font", u"size", 10)
		fontFaceNameOption = StringOption (self, u"Font", u"FaceName", "")
		fontIsBold = BooleanOption (self, "Font", "bold", False)
		fontIsItalic = BooleanOption (self, "Font", "italic", False)

		self.fontEditorOption = FontOption (self, fontFaceNameOption, fontSizeOption, fontIsBold, fontIsItalic)

		# Главное окно
		self.titleFormatOption = StringOption (self, u"MainWindow", u"Title", u"{page} - {file} - OutWiker")
		self.WidthOption = IntegerOption (self, u"MainWindow", u"width", 800)
		self.HeightOption = IntegerOption (self, u"MainWindow", u"height", 680)
		self.XPosOption = IntegerOption (self, u"MainWindow", u"xpos", 0)
		self.YPosOption = IntegerOption (self, u"MainWindow", u"ypos", 0)
		self.FullscreenOption = BooleanOption (self, u"MainWindow", u"fullscreen", False)

		# Панель с деревом
		self.treeWidthOption = core.config.IntegerOption (self, u"MainWindow", u"TreeWidth", 250)
		self.treeHeightOption = core.config.IntegerOption (self, u"MainWindow", u"TreeHeight", 250)
		self.treePaneOption = core.config.StringOption (self, u"MainWindow", u"TreePane", "")

		# Панель с прикрепленными файлами
		self.attachesWidthOption = core.config.IntegerOption (self, u"MainWindow", u"AttachesWidth", 250)
		self.attachesHeightOption = core.config.IntegerOption (self, u"MainWindow", u"AttachesHeight", 150)
		self.attachesPaneOption = core.config.StringOption (self, u"MainWindow", u"AttachesPane", "")
