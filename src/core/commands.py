#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Команды для интерфейса
"""

import os.path
import shutil

import wx

from gui.CreatePageDialog import CreatePageDialog
from core.tree import WikiDocument
import core.exceptions
from core.controller import Controller
from core.tree import RootWikiPage
from gui.OverwriteDialog import OverwriteDialog

def attachFilesWithDialog (parent, page):
	"""
	Вызвать диалог для приаттачивания файлов к странице
	parent -- родительское окно
	page -- страница, куда прикрепляем файлы
	"""
	dlg = wx.FileDialog (parent, style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

	if dlg.ShowModal() == wx.ID_OK:
		files = dlg.GetPaths()
		files.sort()
		attachFiles (parent, page, files)

	dlg.Destroy()


def attachFiles (parent, page, files):
	"""
	Прикрепить файлы к странице с диалогом о перезаписи при необходимости
	"""
	oldAttaches = [os.path.basename (fname).lower() for fname in page.attachment]

	overwriteDialog = OverwriteDialog (parent)

	for fname in files:
		if os.path.basename (fname).lower() in oldAttaches:
			text = u'File "%s" exists already' % (os.path.basename (fname))
			result = overwriteDialog.ShowDialog (text)

			if result == overwriteDialog.ID_SKIP:
				continue
			elif result == wx.ID_CANCEL:
				break
		
		try:
			page.attach ([fname])
		except IOError:
			text = u'Can\'t attach file "%s"' % (fname)
			wx.MessageBox (text, u"Error", wx.ICON_ERROR | wx.OK)
		except shutil.Error:
			text = u'Can\'t attach file "%s"' % (fname)
			wx.MessageBox (text, u"Error", wx.ICON_ERROR | wx.OK)

	overwriteDialog.Destroy()



def editPage (parentWnd, currentPage):
	"""
	Вызвать диалог для редактирования страницы
	parentWnd -- родительское окно
	currentPage -- страница для редактирования
	"""
	if currentPage.readonly:
		wx.MessageBox (u"Wiki is opened as read-only", u"Error", wx.ICON_ERROR | wx.OK)
		return

	dlg = CreatePageDialog.CreateForEdit (currentPage, parentWnd)
	page = None

	if dlg.ShowModal() == wx.ID_OK:
		Controller.instance().onStartTreeUpdate(currentPage.root)

		try:
			factory = dlg.selectedFactory
			tags = dlg.tags

			currentPage.tags = dlg.tags
			currentPage.icon = dlg.icon

			try:
				currentPage.title = dlg.pageTitle
			except OSError as e:
				wx.MessageBox (u"Can't rename page\n" + unicode (e), u"Error", wx.ICON_ERROR | wx.OK)

			currentPage.root.selectedPage = currentPage
		finally:
			Controller.instance().onEndTreeUpdate(currentPage.root)

	dlg.Destroy()


def removePage (page):
	text = u"Remove page '%s' and all subpages?" % (page.title)

	if wx.MessageBox (text, u"Remove page?", wx.YES_NO  | wx.ICON_QUESTION) == wx.YES:
		root = page.root
		Controller.instance().onStartTreeUpdate(root)

		try:
			page.remove()
		except IOError:
			wx.MessageBox (u"Can't remove page", u"Error", wx.ICON_ERROR | wx.OK)
		except core.exceptions.ReadonlyException:
			wx.MessageBox (u"Wiki is opened as read-only", u"Error", wx.ICON_ERROR | wx.OK)
		finally:
			Controller.instance().onEndTreeUpdate(root)


def createPageWithDialog (parentwnd, parentpage):
	"""
	Показать диалог настроек и создать страницу
	"""
	dlg = CreatePageDialog.CreateForCreate (parentpage, parentwnd)
	page = None

	if dlg.ShowModal() == wx.ID_OK:
		factory = dlg.selectedFactory
		title = dlg.pageTitle
		tags = dlg.tags

		Controller.instance().onStartTreeUpdate(parentpage.root)

		try:
			page = factory.create (parentpage, title, tags)
			
			assert page != None

			page.icon = dlg.icon
			page.root.selectedPage = page

		except OSError, IOError:
			wx.MessageBox (u"Can't create page", "Error", wx.ICON_ERROR | wx.OK)
		finally:
			Controller.instance().onEndTreeUpdate(parentpage.root)

	dlg.Destroy()


	return page


def openWikiWithDialog (parent, oldWikiRoot):
	"""
	Показать диалог открытия вики и вернуть открытую wiki
	parent -- родительское окно
	"""
	wikiroot = None

	dialog = wx.FileDialog (parent, 
			wildcard = "__page.opt|__page.opt", 
			style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

	if dialog.ShowModal() == wx.ID_OK:
		if oldWikiRoot != None:
			Controller.instance().onWikiClose (oldWikiRoot)
	
		Controller.instance().onStartTreeUpdate(oldWikiRoot)

		try:
			fullpath = dialog.GetPath()
			path = os.path.dirname(fullpath)
			wikiroot = openWiki (path)
		finally:
			Controller.instance().onEndTreeUpdate(wikiroot)

	dialog.Destroy()

	return wikiroot


def openWiki (path, readonly=False):
	wikiroot = WikiDocument.load (path, readonly)

	if wikiroot.lastViewedPage != None:
		wikiroot.selectedPage = wikiroot[wikiroot.lastViewedPage]
	else:
		wikiroot.selectedPage = None

	return wikiroot


def copyTextToClipboard (text):
	if not wx.TheClipboard.Open():
		wx.MessageBox (u"Can't open clipboard", u"Error", wx.ICON_ERROR | wx.OK)
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
		wx.MessageBox (u"Can't move page when page with that title already exists", u"Error", wx.ICON_ERROR | wx.OK)
	except core.exceptions.TreeException:
		# Невозможно переместить по другой причине
		wx.MessageBox (u"Can't move page", u"Error", wx.ICON_ERROR | wx.OK)
	except core.exceptions.ReadonlyException:
		wx.MessageBox (u"Wiki is opened as read-only", u"Error", wx.ICON_ERROR | wx.OK)


def setStatusText (text, index = 0):
	"""
	Установить текст статусбара.
	text - текст
	index - номер ячейки статусбара
	"""
	wx.GetApp().GetTopWindow().statusbar.SetStatusText (text, index)
