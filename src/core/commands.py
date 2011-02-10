#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Команды для интерфейса
"""

import os.path
import shutil

import wx

import core.exceptions
import core.system
import core.version

from core.tree import WikiDocument
from core.tree import RootWikiPage
from gui.OverwriteDialog import OverwriteDialog
from gui.CreatePageDialog import CreatePageDialog
from core.application import Application


def MessageBox (*args, **kwargs):
	"""
	Замена стандартного MessageBox. Перед показом диалога отключает приложение от события EVT_ACTIVATE_APP.
	"""
	wx.GetApp().unbindActivateApp()
	result = wx.MessageBox (*args, **kwargs)
	wx.GetApp().bindActivateApp()

	return result


def testreadonly (func):
	"""
	Декоратор для отлавливания исключения core.exceptions.ReadonlyException
	"""
	def readOnlyWrap (*args, **kwargs):
		try:
			func (*args, **kwargs)
		except core.exceptions.ReadonlyException:
			MessageBox (_(u"Wiki is opened as read-only"), _(u"Error"), wx.ICON_ERROR | wx.OK)

	return readOnlyWrap


@testreadonly
def attachFilesWithDialog (parent, page):
	"""
	Вызвать диалог для приаттачивания файлов к странице
	parent - родительское окно
	page - страница, куда прикрепляем файлы
	"""
	if page.readonly:
		raise core.exceptions.ReadonlyException

	dlg = wx.FileDialog (parent, style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

	if dlg.ShowModal() == wx.ID_OK:
		files = dlg.GetPaths()
		files.sort()
		attachFiles (parent, page, files)

	dlg.Destroy()


@testreadonly
def attachFiles (parent, page, files):
	"""
	Прикрепить файлы к странице с диалогом о перезаписи при необходимости
	parent - родительское окно
	page - страница, куда прикрепляем файлы
	"""
	if page.readonly:
		raise core.exceptions.ReadonlyException

	oldAttaches = [os.path.basename (fname).lower() for fname in page.attachment]

	overwriteDialog = OverwriteDialog (parent)

	for fname in files:
		if os.path.basename (fname).lower() in oldAttaches:
			text = _(u"File '%s' exists already") % (os.path.basename (fname))
			result = overwriteDialog.ShowDialog (text)

			if result == overwriteDialog.ID_SKIP:
				continue
			elif result == wx.ID_CANCEL:
				break
		
		try:
			page.attach ([fname])
		except IOError:
			text = u'Can\'t attach file "%s"' % (fname)
			MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)
		except shutil.Error:
			text = u'Can\'t attach file "%s"' % (fname)
			MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)

	overwriteDialog.Destroy()



@testreadonly
def editPage (parentWnd, currentPage):
	"""
	Вызвать диалог для редактирования страницы
	parentWnd - родительское окно
	currentPage - страница для редактирования
	"""
	if currentPage.readonly:
		raise core.exceptions.ReadonlyException

	dlg = CreatePageDialog.CreateForEdit (currentPage, parentWnd)
	page = None

	if dlg.ShowModal() == wx.ID_OK:
		Application.onStartTreeUpdate(currentPage.root)

		try:
			factory = dlg.selectedFactory
			tags = dlg.tags

			currentPage.tags = dlg.tags
			currentPage.icon = dlg.icon

			try:
				currentPage.title = dlg.pageTitle
			except OSError as e:
				MessageBox (_(u"Can't rename page\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

			currentPage.root.selectedPage = currentPage
		finally:
			Application.onEndTreeUpdate(currentPage.root)

	dlg.Destroy()


@testreadonly
def removePage (page):
	if page.readonly:
		raise core.exceptions.ReadonlyException

	text = _(u"Remove page '%s' and all subpages?") % (page.title)

	if MessageBox (text, _(u"Remove page?"), wx.YES_NO  | wx.ICON_QUESTION) == wx.YES:
		root = page.root
		Application.onStartTreeUpdate(root)

		try:
			page.remove()
		except IOError:
			MessageBox (_(u"Can't remove page"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		finally:
			Application.onEndTreeUpdate(root)


def createSiblingPage (parentwnd):
	"""
	Создать страницу, находящуюся на том же уровне, что и текущая страница
	parentwnd - окно, которое будет родителем для диалога создания страницы
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	currPage = Application.wikiroot.selectedPage

	if currPage == None or currPage.parent == None:
		parentpage = Application.wikiroot
	else:
		parentpage = currPage.parent

	createPageWithDialog (parentwnd, parentpage)


def createChildPage (parentwnd):
	"""
	Создать страницу, которая будет дочерней к текущей странице
	parentwnd - окно, которое будет родителем для диалога создания страницы
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	currPage = Application.wikiroot.selectedPage

	if currPage == None:
		currPage = Application.wikiroot

	createPageWithDialog (parentwnd, currPage)
	

@testreadonly
def createPageWithDialog (parentwnd, parentpage):
	"""
	Показать диалог настроек и создать страницу
	"""
	if parentpage.readonly:
		raise core.exceptions.ReadonlyException
	
	dlg = CreatePageDialog.CreateForCreate (parentpage, parentwnd)
	page = None

	if dlg.ShowModal() == wx.ID_OK:
		factory = dlg.selectedFactory
		title = dlg.pageTitle
		tags = dlg.tags

		Application.onStartTreeUpdate(parentpage.root)

		try:
			page = factory.create (parentpage, title, tags)
			
			assert page != None

			page.icon = dlg.icon
			page.root.selectedPage = page

		except OSError, IOError:
			MessageBox (_(u"Can't create page"), "Error", wx.ICON_ERROR | wx.OK)
		finally:
			Application.onEndTreeUpdate(parentpage.root)

	dlg.Destroy()


	return page


def openWikiWithDialog (parent, readonly=False):
	"""
	Показать диалог открытия вики и вернуть открытую wiki
	parent -- родительское окно
	"""
	wikiroot = None

	dialog = wx.FileDialog (parent, 
			wildcard = "__page.opt|__page.opt", 
			style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

	if dialog.ShowModal() == wx.ID_OK:
		fullpath = dialog.GetPath()
		path = os.path.dirname(fullpath)
		wikiroot = openWiki (path, readonly)

	dialog.Destroy()

	return wikiroot


def openWiki (path, readonly=False):
	wikiroot = None

	#Application.wikiroot = None
	Application.onStartTreeUpdate(None)

	try:
		# Загрузить вики
		wikiroot = WikiDocument.load (path, readonly)

		# Открыть последнюю открытую страницу
		if wikiroot.lastViewedPage != None:
			wikiroot.selectedPage = wikiroot[wikiroot.lastViewedPage]
		else:
			wikiroot.selectedPage = None

		Application.wikiroot = wikiroot
		Application.onWikiOpen (Application.wikiroot)
	except IOError:
		core.commands.MessageBox (_(u"Can't load wiki '%s'") % path, 
				_(u"Error"), 
				wx.ICON_ERROR | wx.OK)
	finally:
		Application.onEndTreeUpdate(wikiroot)

	return Application.wikiroot


def copyTextToClipboard (text):
	if not wx.TheClipboard.Open():
		MessageBox (_(u"Can't open clipboard"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	data = wx.TextDataObject (text)
	wx.TheClipboard.SetData(data)
	wx.TheClipboard.Flush()
	wx.TheClipboard.Close()


def copyPathToClipboard (page):
	"""
	Копировать путь до страницы в буфер обмена
	"""
	assert page != None
	copyTextToClipboard (page.path)


def copyAttachPathToClipboard (page):
	"""
	Копировать путь до папки с прикрепленными файлами в буфер обмена
	"""
	assert page != None
	path = os.path.join (page.path, RootWikiPage.attachDir)
	copyTextToClipboard (path)


def copyLinkToClipboard (page):
	"""
	Копировать ссылку на страницу в буфер обмена
	"""
	assert page != None
	copyTextToClipboard ("/" + page.subpath)


def copyTitleToClipboard (page):
	"""
	Копировать заголовок страницы в буфер обмена
	"""
	assert page != None
	copyTextToClipboard (page.title)


@testreadonly
def movePage (page, newParent):
	"""
	Сделать страницу page ребенком newParent
	"""
	assert page != None
	assert newParent != None

	try:
		page.moveTo (newParent)
	except core.exceptions.DublicateTitle:
		# Невозможно переместить из-за дублирования имен
		MessageBox (_(u"Can't move page when page with that title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)
	except core.exceptions.TreeException:
		# Невозможно переместить по другой причине
		MessageBox (_(u"Can't move page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


def setStatusText (text, index = 0):
	"""
	Установить текст статусбара.
	text - текст
	index - номер ячейки статусбара
	"""
	wx.GetApp().GetTopWindow().statusbar.SetStatusText (text, index)


def getCurrentVersion ():
	fname = "version.txt"
	path = os.path.join (core.system.getCurrentDir(), fname)

	try:
		with open (path) as fp:
			lines = fp.readlines()
	except IOError, e:
		MessageBox (_(u"Can't open file %s") % fname, _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	version_str = "%s.%s %s" % (lines[0].strip(), lines[1].strip(), lines[2].strip())

	try:
		version = core.version.Version.parse (version_str)
	except ValueError:
		MessageBox (_(u"Can't parse version"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		version = core.version.Version(0, 0)

	return version


@testreadonly
def moveCurrentPageUp ():
	"""
	Переместить текущую страницу на одну позицию вверх
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		Application.wikiroot.selectedPage.order -= 1


@testreadonly
def moveCurrentPageDown ():
	"""
	Переместить текущую страницу на одну позицию вниз
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		Application.wikiroot.selectedPage.order += 1


@testreadonly
def sortChildrenAlphabeticalGUI ():
	"""
	Команда для сортировки дочерних страниц текущей страницы по алфавиту
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		sortChildrenAlphabetical (Application.wikiroot.selectedPage)


@testreadonly
def sortSiblingsAlphabeticalGUI ():
	"""
	Команда для сортировки по алфавиту того же уровня, на котором мы сейчас находимся
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		sortChildrenAlphabetical (Application.wikiroot.selectedPage.parent)


def sortChildrenAlphabetical(parentPage):
	"""
	Отсортировать дочерние страницы по алфавиту
	"""
	children = parentPage.children
	children.sort (RootWikiPage.sortAlphabeticalFunction)

	Application.onStartTreeUpdate (parentPage.root)

	try:
		for n in range (len (children) ):
			children[n].order = n
	finally:
		Application.onEndTreeUpdate (parentPage.root)


@testreadonly
def renamePage (page, newtitle):
	try:
		page.title = newtitle
		page.root.selectedPage = page

	except core.exceptions.DublicateTitle:
		core.commands.MessageBox (_(u"Can't move page when page with that title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)

	except OSError as e:
		core.commands.MessageBox (_(u"Can't rename page\n%s") % unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)
