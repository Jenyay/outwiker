#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Тесты, связанные с конфигом
"""

import unittest
import os
import ConfigParser
import shutil

from core.config import Config, getConfigPath
import core.system
import core.config


class ConfigTest (unittest.TestCase):
	def setUp (self):
		self.path = u"test/testconfig.ini"

		if os.path.exists (self.path):
			os.remove (self.path)


	def testGetSet (self):
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		self.assertEqual (config.get (u"Секция 1", u"Параметр 1"), u"Значение 1")
		self.assertEqual (config.getint (u"Секция 1", u"Параметр 2"), 111)

	
	def testWrite (self):
		"""
		Тесты на то, что измененные значения сразу сохраняются в файл
		"""
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		config2 = Config (self.path)
		self.assertEqual (config2.get (u"Секция 1", u"Параметр 1"), u"Значение 1")
		self.assertEqual (config2.getint (u"Секция 1", u"Параметр 2"), 111)

	
	def testRemoveSection (self):
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		result = config.remove_section (u"Секция 1")

		config2 = Config (self.path)
		self.assertRaises (ConfigParser.NoSectionError, config2.get, u"Секция 1", u"Параметр 1")
	

	def testHasSection (self):
		config = Config (self.path)
		config.set (u"Секция 1", u"Параметр 1", u"Значение 1")
		config.set (u"Секция 1", u"Параметр 2", 111)

		self.assertEqual (config.has_section (u"Секция 1"), True)
		
		result = config.remove_section (u"Секция 1")
		self.assertEqual (config.has_section (u"Секция 1"), False)
	

	def testPortableConfig (self):
		"""
		Проверка правильности определения расположения конфига при хранении его в папке с программой
		"""
		dirname = u".outwiker_test"
		fname = u"outwiker_test.ini"

		programDir = core.system.getCurrentDir()
		localPath = os.path.join (programDir, fname)

		# Создадим файл рядом с запускаемым файлом
		fp = open (localPath, "w")
		fp.close()
		
		fullpath = getConfigPath(dirname, fname)

		self.assertEqual (localPath, fullpath)

		# Удалим созданный файл
		os.remove (localPath)
	

	def testNotPortableConfig1 (self):
		"""
		Проверка правильности определения расположения конфига при хранении его в папке профиля
		"""
		dirname = u".outwiker_test"
		fname = u"outwiker_test.ini"

		programDir = core.system.getCurrentDir()
		localPath = os.path.join (programDir, fname)

		# На всякий случай проверим, что файла в локальной папке нет, иначе удалим его
		if os.path.exists (localPath):
			os.remove (localPath)

		homeDir = os.path.join (os.path.expanduser("~"), dirname)
		homePath = os.path.join (homeDir, fname)

		# Удалим папку в профиле
		if os.path.exists (homeDir):
			shutil.rmtree (homeDir)

		fullpath = getConfigPath(dirname, fname)

		self.assertEqual (homePath, fullpath)
		self.assertTrue (os.path.exists (homeDir))

		# Удалим папку в профиле
		if os.path.exists (homeDir):
			shutil.rmtree (homeDir)


class ConfigOptionsTest (unittest.TestCase):
	def setUp (self):
		self.path = u"../test/testconfig.ini"

		# Создадим небольшой файл настроек
		with open (self.path, "wb") as fp:
			fp.write (u"[Test]\n")
			fp.write (u"intval=100\n")
			fp.write (u"boolval=True\n")
			fp.write (u"strval=тест\n".encode ("utf-8"))

		self.config = core.config.Config (self.path)
	

	def tearDown (self):
		os.remove (self.path)
		pass
	

	# Строковые опции
	def testStringOpt1 (self):
		opt = core.config.StringOption (self.config, u"Test", u"strval", "defaultval")
		self.assertEqual (opt.value, u"тест")


	def testStringOpt2 (self):
		opt = core.config.StringOption (self.config, u"Test", u"strval2", "defaultval")
		self.assertEqual (opt.value, u"defaultval")


	def testStringOpt3 (self):
		opt = core.config.StringOption (self.config, u"Test", u"strval3", "defaultval")
		opt.value = u"проверка"

		newconfig = core.config.Config (self.path)
		newopt = core.config.StringOption (newconfig, u"Test", u"strval3", "defaultval")

		self.assertEqual (newopt.value, u"проверка")
	

	# Целочисленные опции
	def testIntOpt1 (self):
		opt = core.config.IntegerOption (self.config, u"Test", u"intval", 777)
		self.assertEqual (opt.value, 100)


	def testIntOpt2 (self):
		opt = core.config.IntegerOption (self.config, u"Test", u"intval2", 777)
		self.assertEqual (opt.value, 777)


	def testIntOpt3 (self):
		opt = core.config.IntegerOption (self.config, u"Test", u"intval3", 777)
		opt.value = 666

		newconfig = core.config.Config (self.path)
		newopt = core.config.IntegerOption (newconfig, u"Test", u"intval3", 888)

		self.assertEqual (newopt.value, 666)
	

	# Булевы опции
	def testBoolOpt1 (self):
		opt = core.config.BooleanOption (self.config, u"Test", u"Boolval", False)
		self.assertEqual (opt.value, True)


	def testBoolOpt2 (self):
		opt = core.config.BooleanOption (self.config, u"Test", u"Boolval2", False)
		self.assertEqual (opt.value, False)


	def testBoolOpt3 (self):
		opt = core.config.BooleanOption (self.config, u"Test", u"Boolval3", False)
		opt.value = True

		newconfig = core.config.Config (self.path)
		newopt = core.config.BooleanOption (newconfig, u"Test", u"Boolval3", False)

		self.assertEqual (newopt.value, True)
