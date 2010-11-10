#!/usr/bin/env python
# -*- coding: utf8 -*-

import ConfigParser
import os
import core.system


class MyConfigParser (ConfigParser.ConfigParser):
	def __init__ (self, defaults=None, dict_type=dict):
		ConfigParser.ConfigParser.__init__ (self, defaults, dict_type)
	

	def _read(self, fp, fpname):
		"""Parse a sectioned setup file.

		The sections in setup file contains a title line at the top,
		indicated by a name in square brackets (`[]'), plus key/value
		options lines, indicated by `name: value' format lines.
		Continuations are represented by an embedded newline then
		leading whitespace.  Blank lines, lines beginning with a '#',
		and just about everything else are ignored.
		"""
		cursect = None							# None, or a dictionary
		optname = None
		lineno = 0
		e = None								  # None, or an exception
		while True:
			line = fp.readline()
			if not line:
				break
			lineno = lineno + 1
			# comment or blank line?
			if line.strip() == '' or line[0] in '#;':
				continue
			if line.split(None, 1)[0].lower() == 'rem' and line[0] in "rR":
				# no leading whitespace
				continue
			# continuation line?
			if line[0].isspace() and cursect is not None and optname:
				value = line.strip()
				if value:
					cursect[optname] = "%s\n%s" % (cursect[optname], value)
			# a section header or option header?
			else:
				# is it a section header?
				mo = self.SECTCRE.match(line)
				if mo:
					sectname = mo.group('header')
					if sectname in self._sections:
						cursect = self._sections[sectname]
					elif sectname == ConfigParser.DEFAULTSECT:			# Тут добавил "ConfigParser."
						cursect = self._defaults
					else:
						cursect = self._dict()
						cursect['__name__'] = sectname
						self._sections[sectname] = cursect
					# So sections can't start with a continuation line
					optname = None
				# no section header in the file?
				elif cursect is None:
					raise MissingSectionHeaderError(fpname, lineno, line)
				# an option line?
				else:
					mo = self.OPTCRE.match(line)
					if mo:
						optname, vi, optval = mo.group('option', 'vi', 'value')
						if vi in ('=', ':') and ';' in optval:
							# ';' is a comment delimiter only if it follows
							# a spacing character
							pos = optval.find(';')
							if pos != -1 and optval[pos-1].isspace():
								optval = optval[:pos]

						# !!! Из-за этой строки проблемы с тегами, кончиющимися на "Р"
						#optval = optval.strip()
						# allow empty values
						if optval == '""':
							optval = ''
						optname = self.optionxform(optname.rstrip())
						cursect[optname] = optval
					else:
						# a non-fatal parsing error occurred.  set up the
						# exception but keep going. the exception will be
						# raised at the end of the file and will contain a
						# list of all bogus lines
						if not e:
							e = ParsingError(fpname)
						e.append(lineno, repr(line))
		# if any parsing errors occurred, raise an exception
		if e:
			raise e


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
		self.__config = MyConfigParser()

		#fp = open (self.fname)
		#tmp = fp.readlines()
		#print tmp

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
		#print repr (val)
		return unicode (val, "utf8", "replace")
		#return unicode (val, "utf8")

	
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


	def has_section (self, section):
		section_encoded = section.encode ("utf8")
		return self.__config.has_section (section_encoded)


class StringOption (object):
	def __init__ (self, config, section, param, defaultValue):
		"""
		section - секция для параметра конфига
		param - имя параметра конфига
		config - экземпляр класса core.Config
		defaultValue - значение по умолчанию
		"""
		self.section = section
		self.param = param
		self.defaultValue = defaultValue
		self.config = config

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
		self.SashPositionOption = IntegerOption (self, u"MainWindow", u"sash", 200)
