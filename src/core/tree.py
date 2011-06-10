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


class RootWikiPage (object):
	"""
	Класс для корня вики
	"""

	pageConfig = u"__page.opt"
	contentFile = u"__page.text"
	iconName = u"__icon"

	sectionGeneral = u"General"

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
		if path == "/":
			return self

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


	@staticmethod
	def sortFunction (page1, page2):
		"""
		Функция для сортировки страниц с учетом order
		"""

		orderpage1 = page1.params.orderOption.value
		orderpage2 = page2.params.orderOption.value

		# Если еще не установили порядок страницы (значение по умолчанию: -1)
		if orderpage1 == -1 or orderpage2 == -1:
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


	def sortChildrenAlphabetical(self):
		"""
		Отсортировать дочерние страницы по алфавиту
		"""
		self._children.sort (RootWikiPage.sortAlphabeticalFunction)
		#self._children.sort (RootWikiPage.sortAlphabeticalFunction, reverse=True)

		Application.onStartTreeUpdate (self.root)
		self._saveChildrenParams()
		Application.onEndTreeUpdate (self.root)



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
		oldorder = self._children.index (page)
		if oldorder != neworder:
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


	def isChild (self, page):
		"""
		Проверить, является ли page дочерней (вложенной) страницей для self
		"""
		# Возможно, лучше было бы использовать subpath вместо path, 
		# чтобы не зависеть от способа хранения страниц,
		# но тогда надо учесть, что корень имеет subpath - "/"
		return page.path.startswith (self.path)



class WikiDocument (RootWikiPage):
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

		lastvieved = root.lastViewedPage
		if lastvieved != None:
			root.selectedPage = root[lastvieved]

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
		subpath = "/"

		if isinstance (page, type(self)) or page == None:
			# Экземпляр класса WikiDocument выбирать нельзя
			self._selectedPage = None
		else:
			self._selectedPage = page
			subpath = page.subpath

		if not self.readonly:
			self._params.lastViewedPageOption.value = subpath

		Application.onPageSelect(self._selectedPage)
		self.save()
	

	@property
	def lastViewedPage (self):
		subpath = self._params.lastViewedPageOption.value
		return subpath if len (subpath) != 0 else None


	@property
	def subpath (self):
		return u"/"


	@property
	def title (self):
		return os.path.basename (self.path)


	@staticmethod
	def getTypeString ():
		return u"document"



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
		# может меняться только регистр букв
		if not self.canRename(newtitle):
			raise core.exceptions.DublicateTitle

		newpath = os.path.join (os.path.dirname (oldpath), newtitle)
		os.renames (oldpath, newpath)
		self._title = newtitle

		WikiPage.__renamePaths (self, newpath)

		if self.root.selectedPage == self:
			self.root.params.lastViewedPageOption.value = self.subpath

		Application.onPageRename (self, oldsubpath)
		#Application.onPageUpdate (self)
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

		if self.isChild (newparent):
			# Нельзя быть родителем своего родителя (предка)
			raise core.exceptions.TreeException

		# Проверка на то, что в новом родителе нет записи с таким же заголовком
		if newparent[self.title] != None:
			raise core.exceptions.DublicateTitle

		oldpath = self.path
		oldparent = self.parent

		# Новый путь для страницы
		newpath = os.path.join (newparent.path, self.title)

		# Временное имя папки.
		# Сначала попробуем переименовать папку во временную, 
		# а потом уже ее переместим в нужное место с нужным именем
		tempname = self._getTempName (oldpath)

		try:
			os.renames (oldpath, tempname)
			shutil.move (tempname, newpath)
		except shutil.Error:
			raise core.exceptions.TreeException
		except OSError:
			raise core.exceptions.TreeException

		self._parent = newparent
		oldparent.removeFromChildren (self)
		newparent.addToChildren (self)
		
		WikiPage.__renamePaths (self, newpath)

		if self.root.selectedPage == self:
			self.root.params.lastViewedPageOption.value = self.subpath

		Application.onTreeUpdate (self)

	
	def _getTempName (self, pagepath):
		"""
		Найти уникальное имя для перемещаемой страницы.
		При перемещении сначала пробуем переименовать папку со страницей, а потом уже перемещать
		pagepath - текущий путь до страницы

		Метод возвращает полный путь
		"""
		(path, title) = os.path.split (pagepath)
		template = u"__{title}_{number}"
		number = 0
		newname = template.format (title=title, number=number)

		while (os.path.exists (os.path.join (path, newname) ) ):
			number += 1
			newname = template.format (title=title, number=number)

		return os.path.join (path, newname)


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

		if self._tags != tags:
			self._tags = tags[:]
			self.save()
			Application.onPageUpdate(self)


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
		self._params.orderOption.value = self.order



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

		#if not os.path.exists (self.path):
		#	self.save()

		if text != self.content:
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

		oldpath = self.path
		tempname = self._getTempName (oldpath)

		try:
			os.renames (oldpath, tempname)
			shutil.rmtree (tempname)
		except shutil.Error:
			raise IOError
		except OSError:
			raise IOError

		#try:
		#	shutil.rmtree (self.path)
		#except OSError:
		#	raise IOError

		self._removePageFromTree (self)

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
	

