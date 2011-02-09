#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

import wx
import wx.aui

from core.tree import WikiDocument, RootWikiPage
from WikiTree import WikiTree
from gui.CurrentPagePanel import CurrentPagePanel
import core.commands
from core.recent import RecentWiki
import pages.search.searchpage
import core.system
from gui.preferences.PrefDialog import PrefDialog
from gui.about import AboutDialog
from core.application import Application
from gui.trayicon import OutwikerTrayIcon
from gui.AttachPanel import AttachPanel
import core.config


class GuiController (object):
	"""
	Класс содержит обработчики меню и панели инструментов с главного окна
	"""
	def __init__ (self, mainWnd):
		"""
		mainWnd - галвное окно
		"""
		self.mainWnd = mainWnd
