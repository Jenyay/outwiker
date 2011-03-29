#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import ConfigParser
import shutil

from application import Application
from config import PageConfig
from bookmarks import Bookmarks
from search import TagsList
import core.exceptions
from attachment import Attachment


class RootWikiPage (object):
	"""
	Класс для корня вики
	"""

	pageConfig = u"__page.opt"
	contentFile = u"__page.text"
	iconName = u"__icon"

	sectionGeneral = u"General"
	paramOrder = u"order"

	def __init__(self, path, readonly=False):
		"""
		Constructor.
		
		path -- путь до страницы относительно корня дерева
		"""
		# Путь до страницы
		self._path = path
		self._parent = None
		self._children = []
		self.readonly = readonly

		self._params = RootWikiPage._readParams(self.path, self.readonly)

	
	@staticmethod
	def _readParams (path, readonly=False):
		return PageConfig (os.path.join (path, RootWikiPage.pageConfig), readonly)


	@property
	def params (self):
		return self._params


	@property
	def path (self):
		return self._path
	

	@property
	def parent (self):
		return self._parent


	@property
	def children (self):
		return self._children[:]


	@property
	def root (self):
		"""
		Найти корень дерева по странице
		"""
		result = self
		while result.parent != None:
			result = result.parent

		return result


	def getParameter (self, section, param):
		"""
		Получить значение параметра param из секции section
		"""
		return self._params.get (section, param)


	def setParameter (self, section, param, value):
		"""
		Установить значение параметра param секции section в value
		"""
		if self.readonly:
			return False

		self._params.set (section, param, value)
		return True


	def save (self):
		if self.readonly:
			return

		if not os.path.exists (self.path):
			os.mkdir (self.path)

		self._params.save()


	def __len__ (self):
		return len (self._children)


	def __getitem__ (self, path):
		"""
		Получить нужную страницу по относительному пути в дереве
		"""
		# Разделим путь по составным частям
		titles = path.split ("/")
		page = self

		for title in titles:
			found = False
			for child in page.children:
				if child.title.lower() == title.lower():
					page = child
					found = True

			if not found:
				page = None
				break

		return page


	def getChildren(self):
		"""
		Загрузить дочерние узлы
		"""
		try:
			entries = os.listdir (self.path)
		except OSError:
			raise IOError

		result = []

		for name in entries:
			fullpath = os.path.join (self.path, name)

			if not name.startswith ("__") and os.path.isdir (fullpath):
				try:
					page = WikiPage.load (fullpath, self, self.readonly)
				except Exception as e:
					continue

				result.append (page)

		result.sort (RootWikiPage.sortFunction)

		return result


	def _sortChildren (self):
		self._children.sort (RootWikiPage.sortFunction)
		self._saveChildrenParams()


	@staticmethod
	def sortFunction (page1, page2):
		"""
		Функция для сортировки страниц с учетом order
		"""
		try:
			orderpage1 = int (page1.getParameter (RootWikiPage.sectionGeneral, RootWikiPage.paramOrder))
			orderpage2 = int (page2.getParameter (RootWikiPage.sectionGeneral, RootWikiPage.paramOrder))
		except Exception:
			# Если хотя бы у одной страницы не указан порядок, то сравнивать страницы только по заголовкам
			orderpage1 = -1
			orderpage2 = -1

		if orderpage1 > orderpage2:
			return 1
		elif orderpage1 < orderpage2:
			return -1

		return RootWikiPage.sortAlphabeticalFunction (page1, page2)


	@staticmethod
	def sortAlphabeticalFunction (page1, page2):
		"""
		Функция для сортировки страниц по алфавиту
		"""
		if page1.title.lower() > page2.title.lower():
			return 1
		elif page1.title.lower() < page2.title.lower():
			return -1

		return 0


	@staticmethod
	def testDublicate (parent, title):
		"""
		Проверить заголовок страницы на то, что в родителе нет страницы с таким заголовком
		"""
		return parent[title] == None


	def _changeChildOrder (self, page, neworder):
		"""
		Изменить порядок дочерних элементов
		Дочернюю страницу page переместить на уровень neworder
		"""
		self._children.index (page)
		self.removeFromChildren (page)
		self._children.insert (neworder, page)
		self._saveChildrenParams()
	

	def _saveChildrenParams (self):
		for child in self._children:
			child.save()
	

	def addToChildren (self, page):
		"""
		Добавить страницу к дочерним страницам
		"""
		self._children.append (page)
		self._children.sort (RootWikiPage.sortFunction)
	

	def removeFromChildren (self, page):
		"""
		Удалить страницу из дочерних страниц
		"""
		self._children.remove (page)
	

	# TODO: Избавиться от этого метода
	def getAttachPath (self, create=False):
		"""
		Возвращает путь до страницы с прикрепленными файлами
		create - создать папку для прикрепленных файлов, если она еще не создана?
		"""
		return Attachment(self).getAttachPath (create)
	

class WikiDocument (RootWikiPage):
	sectionHistory = u"History"
	paramHistory = u"LastViewedPage"

	def __init__ (self, path, readonly = False):
		RootWikiPage.__init__ (self, path, readonly)
		self._selectedPage = None
		self.bookmarks = Bookmarks (self, self._params)


	@staticmethod
	def load(path, readonly = False):
		"""
		Загрузить корневую страницу вики.
		Использовать этот метод вместо конструктора
		"""
		root = WikiDocument(path, readonly)
		root.loadChildren()
		Application.onTreeUpdate(root)
		return root


	def loadChildren (self):
		"""
		Интерфейс для загрузки дочерних страниц
		"""
		self._children = self.getChildren()


	@staticmethod
	def create (path):
		"""
		Создать корень для вики
		"""
		root = WikiDocument (path)
		root.save()
		Application.onTreeUpdate(root)

		return root

	@property
	def selectedPage (self):
		return self._selectedPage

	@selectedPage.setter
	def selectedPage (self, page):
		self._selectedPage = page

		if page != None and not self.readonly:
			self.setParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory,
					page.subpath)

		Application.onPageSelect(self._selectedPage)
		self.save()
	

	@property
	def lastViewedPage (self):
		try:
			subpath = self.getParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory)
			return subpath
		except ConfigParser.NoSectionError:
			pass
		except ConfigParser.NoOptionError:
			pass

	


class WikiPage (RootWikiPage):
	"""
	Страница в дереве.
	"""
	paramTags = u"tags"
	paramType = u"type"

	@staticmethod
	def getTypeString ():
		return u"base"


	def __init__(self, path, title, parent, readonly = False):
		"""
		Constructor.
		
		path -- путь до страницы
		"""
		if not RootWikiPage.testDublicate(parent, title):
			raise core.exceptions.DublicateTitle

		RootWikiPage.__init__ (self, path, readonly)
		self._title = title
		self._parent = parent


	@property
	def order (self):
		"""
		Вернуть индекс страницы в списке дочерних страниц
		"""
		return self.parent.children.index (self)


	@order.setter
	def order (self, neworder):
		"""
		Изменить положение страницы (порядок)
		"""
		if self.readonly:
			raise core.exceptions.ReadonlyException

		realorder = neworder

		if realorder < 0:
			realorder = 0

		if realorder >= len (self.parent.children):
			realorder = len (self.parent.children) - 1

		self.parent._changeChildOrder (self, realorder)
		Application.onPageOrderChange (self)
	

	@property
	def title (self):
		return self._title

	
	@title.setter
	def title (self, newtitle):
		if self.readonly:
			raise core.exceptions.ReadonlyException

		oldtitle = self.title
		oldpath = self.path
		oldsubpath = self.subpath

		if oldtitle == newtitle:
			return

		# Проверка на дубликат страниц, а также на то, что в заголовке страницы
		# может меняться только регинстр букв
		if not self.canRename(newtitle):
			raise core.exceptions.DublicateTitle

		newpath = os.path.join (os.path.dirname (oldpath), newtitle)
		os.renames (oldpath, newpath)
		self._title = newtitle

		WikiPage.__renamePaths (self, newpath)

		if self.root.selectedPage == self:
			self.root.setParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory,
					self.subpath)

		Application.onPageRename (self, oldsubpath)
		Application.onTreeUpdate (self)
	

	def canRename (self, newtitle):
		return (self.title.lower() == newtitle.lower() or
				self.parent[newtitle] == None)
	

	@staticmethod
	def __renamePaths (page, newPath):
		"""
		Скорректировать пути после переименования страницы
		"""
		oldPath = page.path
		page._path = newPath
		page._params = RootWikiPage._readParams(page.path)

		for child in page.children:
			newChildPath = child.path.replace (oldPath, newPath, 1)
			WikiPage.__renamePaths (child, newChildPath)

	
	def moveTo (self, newparent):
		"""
		Переместить запись к другому родителю
		"""
		if self.readonly:
			raise core.exceptions.ReadonlyException

		if self._parent == newparent:
			return

		# Проверка на то, что в новом родителе нет записи с таким же заголовком
		if newparent[self.title] != None:
			raise core.exceptions.DublicateTitle

		oldpath = self.path
		oldparent = self.parent

		# Новый путь для страницы
		newpath = os.path.join (newparent.path, self.title)

		try:
			shutil.move (oldpath, newpath)
		except shutil.Error:
			raise core.exceptions.TreeException

		self._parent = newparent
		oldparent.removeFromChildren (self)
		newparent.addToChildren (self)
		
		WikiPage.__renamePaths (self, newpath)

		if self.root.selectedPage == self:
			self.root.setParameter (WikiDocument.sectionHistory, 
					WikiDocument.paramHistory,
					self.subpath)

		Application.onTreeUpdate (self)


	@property
	def icon (self):
		return self._getIcon()


	@icon.setter
	def icon (self, iconpath):
		if self.readonly:
			raise core.exceptions.ReadonlyException

		name = os.path.basename (iconpath)
		dot = name.rfind (".")
		extension = name[dot:]

		newname = RootWikiPage.iconName + extension
		newpath = os.path.join (self.path, newname)

		if iconpath != newpath:
			shutil.copyfile (iconpath, newpath)

		Application.onPageUpdate (self)
		Application.onTreeUpdate (self)

		return newpath



	@property
	def tags (self):
		return self._tags

	@tags.setter
	def tags (self, tags):
		if self.readonly:
			raise core.exceptions.ReadonlyException

		self._tags = tags[:]
		self.save()
		Application.onPageUpdate(self)


	# TODO: Избавиться
	@property
	def attachment (self):
		"""
		Возвращает список прикрепленных файлов.
		Пути до файлов полные
		"""
		return self._getAttachments()


	# TODO: Избавиться
	def _getAttachments(self):
		"""
		Найти все приаттаченные файлы
		Пути до файлов полные
		"""
		path = self.getAttachPath()

		if not os.path.exists (path):
			return []

		result = [os.path.join (path, fname) for fname in os.listdir (path)]

		return result


	# TODO: Избавиться
	def attach (self, files):
		"""
		Прикрепить файл к странице
		files -- список файлов (или папок), которые надо прикрепить
		"""
		if self.readonly:
			raise core.exceptions.ReadonlyException

		attachPath = self.getAttachPath()
		
		if not os.path.exists (attachPath):
			os.mkdir (attachPath)

		for name in files:
			if os.path.isdir (name):
				basename = os.path.basename (name)
				shutil.copytree (name, os.path.join (attachPath, basename) )
			else:
				shutil.copy (name, attachPath)

		Application.onPageUpdate (self)
	

	# TODO: Избавиться
	def removeAttach (self, files):
		"""
		Удалить прикрепленные файлы
		"""
		if self.readonly:
			raise core.exceptions.ReadonlyException

		attachPath = self.getAttachPath()

		for fname in files:
			path = os.path.join (attachPath, fname)
			try:
				os.remove (path)
			except OSError:
				Application.onPageUpdate (self)
				raise IOError (u"Can't remove %s" % fname)

		Application.onPageUpdate (self)


	def _getIcon (self):
		files = os.listdir (self.path)

		for file in files:
			if (file.startswith (RootWikiPage.iconName) and
					not os.path.isdir (file)):
				return os.path.join (self.path, file)
	

	def initAfterLoading (self):
		"""
		Инициализировать после загрузки (загрузить параметры страницы)
		"""
		# Теги страницы
		self._tags = self._getTags (self._params)

		self._children = self.getChildren ()
	

	@staticmethod
	def load (path, parent, readonly = False):
		"""
		Загрузить страницу.
		Использовать этот метод вместо конструктора, когда надо загрузить страницу
		"""
		from core.factoryselector import FactorySelector

		title = os.path.basename(path)
		params = RootWikiPage._readParams(path, readonly)

		# Получим тип страницы по параметрам
		pageType = FactorySelector.getFactory(params.typeOption.value).getPageType()

		page = pageType (path, title, parent, readonly)
		page.initAfterLoading ()

		return page


	def save (self):
		"""
		Сохранить страницу
		"""
		if self.readonly:
			return

		if not os.path.exists (self.path):
			os.mkdir (self.path)

		# Закомментарить эти три строки, если не хотим, 
		# чтобы папка __attach создавалась при создании страницы
		#attachPath = self.getAttachPath()
		#if not os.path.exists (attachPath):
		#	os.mkdir (attachPath)

		try:
			text = self.content
		except IOError:
			text = u""

		with open (os.path.join (self.path, RootWikiPage.contentFile), "w") as fp:
			fp.write (text.encode ("utf8"))

		self._saveOptions ()
	

	def _saveOptions (self):
		"""
		Сохранить настройки
		"""
		# Тип
		self._params.typeOption.value = self.getTypeString()

		#Теги
		self._saveTags()

		# Порядок страницы
		self._params.set (RootWikiPage.sectionGeneral, RootWikiPage.paramOrder, self.order)



	def _saveTags (self):
		tags = reduce (lambda full, tag: full + ", " + tag, self._tags, "")

		# Удалим начальные ", "
		tags = tags[2: ]
		self._params.set (RootWikiPage.sectionGeneral, WikiPage.paramTags, tags)


	def initAfterCreating (self, tags):
		"""
		Инициализация после создания
		"""
		self._tags = tags[:]
		self.save()
		Application.onPageCreate(self)
	

	def _getTags (self, configParser):
		"""
		Выделить теги из строки конфигурационного файла
		"""
		try:
			tagsString = configParser.get (RootWikiPage.sectionGeneral, WikiPage.paramTags)
		except ConfigParser.NoOptionError:
			return []

		tags = TagsList.parseTagsList (tagsString)

		return tags

	
	@property
	def content(self):
		"""
		Прочитать файл-содержимое страницы
		"""
		text = ""

		try:
			with open (os.path.join (self.path, RootWikiPage.contentFile)) as fp:
				text = fp.read()
		except IOError:
			pass
		
		return unicode (text, "utf8")


	@content.setter
	def content (self, text):
		if self.readonly:
			raise core.exceptions.ReadonlyException

		path = os.path.join (self.path, RootWikiPage.contentFile)

		with open (path, "wb") as fp:
			fp.write (text.encode ("utf8"))

		Application.onPageUpdate(self)
	

	@property
	def textContent (self):
		"""
		Получить контент в текстовом виде.
		Используется для поиска по страницам.
		В большинстве случаев достаточно вернуть просто content
		"""
		return self.content
	

	@property
	def subpath (self):
		result = self.title
		page = self.parent

		while page.parent != None:
			# Пока не дойдем до корня, у которого нет заголовка, и родитель - None
			result = page.title + "/" + result
			page = page.parent

		return result


	def remove (self):
		"""
		Удалить страницу
		"""
		if self.readonly:
			raise core.exceptions.ReadonlyException

		self._removePageFromTree (self)

		try:
			shutil.rmtree (self.path)
		except OSError:
			raise IOError

		# Если выбранная страница была удалена
		if self.root.selectedPage != None and self.root.selectedPage.isRemoved:
			# Новая выбранная страница взамен старой
			newselpage = self.root.selectedPage
			while newselpage.parent != None and newselpage.isRemoved:
				newselpage = newselpage.parent

			# Если попали в корень дерева
			if newselpage.parent == None:
				newselpage = None

			self.root.selectedPage = newselpage
		
		#Application.onTreeUpdate(self.root)
	

	def _removePageFromTree (self, page):
		page.parent.removeFromChildren (page)

		for child in page.children:
			page._removePageFromTree (child)

		Application.onPageRemove (page)


	@property
	def isRemoved (self):
		"""
		Проверить, что страница удалена
		"""
		return self not in self.parent.children
	

