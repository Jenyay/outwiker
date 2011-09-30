#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import os.path
import ConfigParser

import wx

from outwiker.core.application import Application
import outwiker.core.exceptions
import outwiker.core.commands
import outwiker.core.system
import outwiker.gui.pagedialog
from outwiker.core.config import BooleanOption


class WikiTree(wx.Panel):
	def __init__(self, *args, **kwds):
		self.ID_ADD_CHILD = wx.NewId()
		self.ID_ADD_SIBLING = wx.NewId()
		self.ID_RENAME = wx.NewId()
		self.ID_REMOVE = wx.NewId()
		self.ID_PROPERTIES_BUTTON = wx.NewId()
		self.ID_PROPERTIES_POPUP = wx.NewId()
		self.ID_MOVE_UP = wx.NewId()
		self.ID_MOVE_DOWN = wx.NewId()
		self.ID_ADD_SIBLING_PAGE = wx.NewId()
		self.ID_ADD_CHILD_PAGE = wx.NewId()
		self.ID_REMOVE_PAGE = wx.NewId()
		
		self.ID_COPY_PATH = wx.NewId()
		self.ID_COPY_ATTACH_PATH = wx.NewId()
		self.ID_COPY_TITLE = wx.NewId()
		self.ID_COPY_LINK = wx.NewId()

		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.toolbar = self.__getToolbar(self, -1)
		self.treeCtrl = wx.TreeCtrl(self, -1, style=wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_LINES_AT_ROOT|wx.TR_EDIT_LABELS|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER)

		self.__set_properties()
		self.__do_layout()

		self.defaultIcon = os.path.join (outwiker.core.system.getImagesDir(), "page.png")
		self.iconHeight = 16

		self.defaultBitmap = wx.Bitmap (self.defaultIcon)
		assert self.defaultBitmap.IsOk()
		
		self.defaultBitmap.SetHeight (self.iconHeight)

		self.dragItem = None
	
		# Картинки для дерева
		self.imagelist = wx.ImageList(16, self.iconHeight)
		self.treeCtrl.AssignImageList (self.imagelist)

		# Кеш для страниц, чтобы было проще искать элемент дерева по странице
		# Словарь. Ключ - страница, значение - элемент дерева wx.TreeItemId
		self._pageCache = {}

		self.__createPopupMenu()

		# Элемент, над которым показываем меню
		self.popupItem = None

		# Секция настроек куда сохраняем развернутость страницы
		self.pageOptionsSection = u"Tree"

		# Имя опции для сохранения развернутости страницы
		self.pageOptionExpand = "Expand"

		self.__BindApplicationEvents()
		self.__BindGuiEvents()
		self.__BindPopupMenuEvents()


	def __BindApplicationEvents(self):
		"""
		Подписка на события контроллера
		"""
		Application.onWikiOpen += self.__onWikiOpen
		Application.onTreeUpdate += self.__onTreeUpdate
		Application.onPageCreate += self.__onPageCreate
		Application.onPageOrderChange += self.__onPageOrderChange
		Application.onPageSelect += self.__onPageSelect
		Application.onPageRemove += self.__onPageRemove

		Application.onStartTreeUpdate += self.__onStartTreeUpdate
		Application.onEndTreeUpdate += self.__onEndTreeUpdate
		
		# События, связанные с рендерингом страниц
		#Application.onHtmlRenderingBegin += self.__onHtmlRenderingBegin
		#Application.onHtmlRenderingEnd += self.__onHtmlRenderingEnd


	def __UnBindApplicationEvents(self):
		"""
		Отписка от событий контроллера
		"""
		Application.onWikiOpen -= self.__onWikiOpen
		Application.onTreeUpdate -= self.__onTreeUpdate
		Application.onPageCreate -= self.__onPageCreate
		Application.onPageOrderChange -= self.__onPageOrderChange
		Application.onPageSelect -= self.__onPageSelect
		Application.onPageRemove -= self.__onPageRemove

		Application.onStartTreeUpdate -= self.__onStartTreeUpdate
		Application.onEndTreeUpdate -= self.__onEndTreeUpdate
		
		# События, связанные с рендерингом страниц
		#Application.onHtmlRenderingBegin -= self.__onHtmlRenderingBegin
		#Application.onHtmlRenderingEnd -= self.__onHtmlRenderingEnd


	def __onWikiOpen (self, root):
		self.__treeUpdate (root)
	

	def __BindGuiEvents (self):
		"""
		Подписка на события интерфейса
		"""
		# События, связанные с деревом
		self.Bind (wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)

		# Перетаскивание элементов
		self.treeCtrl.Bind (wx.EVT_TREE_BEGIN_DRAG, self.__onBeginDrag)
		self.treeCtrl.Bind (wx.EVT_TREE_END_DRAG, self.__onEndDrag)
		
		# Переименование элемента
		self.treeCtrl.Bind (wx.EVT_TREE_END_LABEL_EDIT, self.__onEndLabelEdit)

		# Показ всплывающего меню
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_MENU, self.__onItemMenu)
		
		# Сворачивание/разворачивание элементов
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_COLLAPSED, self.__onTreeStateChanged)
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_EXPANDED, self.__onTreeStateChanged)

		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_ACTIVATED, self.__onTreeItemActivated)

		self.Bind(wx.EVT_MENU, self.__onMoveUp, id=self.ID_MOVE_UP)
		self.Bind(wx.EVT_MENU, self.__onMoveDown, id=self.ID_MOVE_DOWN)
		self.Bind(wx.EVT_MENU, self.__onAddSiblingPage, id=self.ID_ADD_SIBLING_PAGE)
		self.Bind(wx.EVT_MENU, self.__onAddChildPage, id=self.ID_ADD_CHILD_PAGE)
		self.Bind(wx.EVT_MENU, self.__onRemovePage, id=self.ID_REMOVE_PAGE)
		
		self.Bind(wx.EVT_MENU, self.__onPropertiesButton, id=self.ID_PROPERTIES_BUTTON)

		self.Bind (wx.EVT_CLOSE, self.__onClose)


	def __onClose (self, event):
		self.__UnBindApplicationEvents()


	def __onPropertiesButton (self, event):
		if Application.selectedPage != None:
			outwiker.gui.pagedialog.editPage (self, Application.selectedPage)


	def __onPageCreate (self, newpage):
		"""
		Обработка создания страницы
		"""
		if newpage.parent in self._pageCache:
			parentItem = self._pageCache[newpage.parent]
			self.__insertChild (newpage, parentItem)

			assert newpage in self._pageCache
			item = self._pageCache[newpage]
			assert item.IsOk()

			self.treeCtrl.Expand (item)


	def __onAddSiblingPage (self, event):
		outwiker.gui.pagedialog.createSiblingPage (self)


	def __onAddChildPage (self, event):
		outwiker.gui.pagedialog.createChildPage (self)


	def __onRemovePage (self, event):
		if Application.wikiroot != None and Application.wikiroot.selectedPage != None:
			outwiker.core.commands.removePage (Application.wikiroot.selectedPage)


	def __onMoveUp (self, event):
		outwiker.core.commands.moveCurrentPageUp()


	def __onMoveDown (self, event):
		outwiker.core.commands.moveCurrentPageDown()


	def __onPageRemove (self, page):
		self.__removePageItem (page)
	

	def __onTreeItemActivated (self, event):
		item = event.GetItem()
		if not item.IsOk():
			return

		page = self.treeCtrl.GetItemData (item).GetData()
		outwiker.gui.pagedialog.editPage (self, page)
		

	def __BindPopupMenuEvents (self):
		"""
		События, связанные с контекстным меню
		"""
		self.Bind(wx.EVT_MENU, self.__onAddChild, id=self.ID_ADD_CHILD)
		self.Bind(wx.EVT_MENU, self.__onAddSibling, id=self.ID_ADD_SIBLING)
		self.Bind(wx.EVT_MENU, self.__onRename, id=self.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.__onRemove, id=self.ID_REMOVE)
		
		self.Bind(wx.EVT_MENU, self.__onCopyTitle, id=self.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.__onCopyPath, id=self.ID_COPY_PATH)
		self.Bind(wx.EVT_MENU, self.__onCopyAttachPath, id=self.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.__onCopyLink, id=self.ID_COPY_LINK)

		self.Bind(wx.EVT_MENU, self.__onPropertiesPopup, id=self.ID_PROPERTIES_POPUP)
	

	#def __onHtmlRenderingBegin (self, page, htmlView):
		#self.treeCtrl.Disable()
		#self.treeCtrl.Update()
		#pass

	
	#def __onHtmlRenderingEnd (self, page, htmlView):
		#self.treeCtrl.Enable()
		#pass


	def __onTreeStateChanged (self, event):
		item = event.GetItem()
		assert item.IsOk()
		self.__saveItemState (item)


	def __saveItemState (self, itemid):
		assert itemid.IsOk()

		page = self.treeCtrl.GetItemData (itemid).GetData()
		expanded = self.treeCtrl.IsExpanded (itemid)
		expandedOption = BooleanOption (page.params, self.pageOptionsSection, self.pageOptionExpand, False)

		try:
			expandedOption.value = expanded
		except IOError as e:
			outwiker.core.commands.MessageBox (_(u"Can't save page options\n%s") % (unicode (e)),
					_(u"Error"), wx.ICON_ERROR | wx.OK)


	def __loadExpandState (self, page):
		if page.parent != None:
			try:
				expanded = page.params.getbool (self.pageOptionsSection, self.pageOptionExpand)
			except ConfigParser.NoSectionError:
				return
			except ConfigParser.NoOptionError:
				return

			if expanded:
				self.treeCtrl.Expand (self._pageCache[page])


	def __onRemove (self, event):
		"""
		Удалить страницу
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		outwiker.core.commands.removePage (page)


	def __onCopyLink (self, event):
		"""
		Копировать ссылку на страницу в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		outwiker.core.commands.copyLinkToClipboard (page)

	
	def __onCopyTitle (self, event):
		"""
		Копировать заголовок страницы в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		outwiker.core.commands.copyTitleToClipboard (page)

	
	def __onCopyPath (self, event):
		"""
		Копировать путь до страницы в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		outwiker.core.commands.copyPathToClipboard (page)


	def __onCopyAttachPath (self, event):
		"""
		Копировать путь до прикрепленных файлов в буфер обмена
		"""
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		outwiker.core.commands.copyAttachPathToClipboard (page)


	def __createPopupMenu (self):
		self.popupMenu = wx.Menu ()
		self.popupMenu.Append (self.ID_ADD_CHILD, _(u"Add Child Page…"))
		self.popupMenu.Append (self.ID_ADD_SIBLING, _(u"Add Sibling Page…"))
		self.popupMenu.Append (self.ID_RENAME, _(u"Rename"))
		self.popupMenu.Append (self.ID_REMOVE, _(u"Remove…"))
		self.popupMenu.AppendSeparator()
		
		self.popupMenu.Append (self.ID_COPY_TITLE, _(u"Copy Page Title"))
		self.popupMenu.Append (self.ID_COPY_PATH, _(u"Copy Page Path"))
		self.popupMenu.Append (self.ID_COPY_ATTACH_PATH, _(u"Copy Attaches Path"))
		self.popupMenu.Append (self.ID_COPY_LINK, _(u"Copy Page Link"))
		self.popupMenu.AppendSeparator()

		self.popupMenu.Append (self.ID_PROPERTIES_POPUP, _(u"Properties…"))
	

	def __onRename (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		self.treeCtrl.EditLabel (self.popupItem)
	

	def __onAddChild (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		outwiker.gui.pagedialog.createPageWithDialog (self, page)

	
	def __onAddSibling (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None
		assert page.parent != None

		outwiker.gui.pagedialog.createPageWithDialog (self, page.parent)

	
	def __onPropertiesPopup (self, event):
		assert self.popupItem != None
		assert self.popupItem.IsOk()

		page = self.treeCtrl.GetItemData (self.popupItem).GetData()
		assert page != None

		if page.parent != None:
			outwiker.gui.pagedialog.editPage (self, page)
	

	def __onItemMenu (self, event):
		self.popupItem = event.GetItem()
		if not self.popupItem.IsOk ():
			return

		self.PopupMenu (self.popupMenu)
	

	def beginRename (self):
		selectedItem = self.treeCtrl.GetSelection()
		if not selectedItem.IsOk():
			return

		self.treeCtrl.EditLabel (selectedItem)


	def __onEndLabelEdit (self, event):
		if event.IsEditCancelled():
			return

		# Новый заголовок
		label = event.GetLabel().strip()

		item = event.GetItem()
		page = self.treeCtrl.GetItemData (item).GetData()
		
		# Не доверяем переименовывать элементы системе
		event.Veto()

		outwiker.core.commands.renamePage (page, label)


	def __onStartTreeUpdate (self, root):
		self.__unbindUpdateEvents()
	

	def __unbindUpdateEvents (self):
		Application.onTreeUpdate -= self.__onTreeUpdate
		Application.onPageCreate -= self.__onPageCreate
		Application.onPageSelect -= self.__onPageSelect
		Application.onPageOrderChange -= self.__onPageOrderChange
		self.Unbind (wx.EVT_TREE_SEL_CHANGED, handler = self.__onSelChanged)

	
	def __onEndTreeUpdate (self, root):
		self.__bindUpdateEvents()
		self.__treeUpdate (Application.wikiroot)


	def __bindUpdateEvents (self):
		Application.onTreeUpdate += self.__onTreeUpdate
		Application.onPageCreate += self.__onPageCreate
		Application.onPageSelect += self.__onPageSelect
		Application.onPageOrderChange += self.__onPageOrderChange
		self.Bind (wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)

	
	def __onBeginDrag (self, event):
		event.Allow()
		self.dragItem = event.GetItem()
		self.treeCtrl.SetFocus()


	def __onEndDrag (self, event):
		if self.dragItem != None:
			# Элемент, на который перетащили другой элемент (self.dragItem)
			endDragItem = event.GetItem()

			# Перетаскиваемая станица
			draggedPage = self.treeCtrl.GetItemData (self.dragItem).GetData()

			# Будущий родитель для страницы
			if endDragItem.IsOk():
				newParent = self.treeCtrl.GetItemData (endDragItem).GetData()
				outwiker.core.commands.movePage (draggedPage, newParent)
				self.treeCtrl.Expand (self._pageCache[newParent])

		self.dragItem = None


	def __onTreeUpdate (self, sender):
		self.__treeUpdate (sender.root)


	def __onPageSelect (self, page):
		"""
		Изменение выбранной страницы
		"""
		currpage = self.selectedPage
		if currpage != page:
			self.selectedPage = page


	def __onSelChanged (self, event):
		page = self.selectedPage
		if page.root.selectedPage != page:
			page.root.selectedPage = page
	

	def __onPageOrderChange (self, sender):
		"""
		Изменение порядка страниц
		"""
		self.__updatePage (sender)
	

	@property
	def selectedPage (self):
		item = self.treeCtrl.GetSelection ()
		if item.IsOk():
			page = self.treeCtrl.GetItemData (item).GetData()
			return page


	@selectedPage.setter
	def selectedPage (self, newSelPage):
		if newSelPage == None:
			return

		item = self._pageCache[newSelPage]
		self.treeCtrl.SelectItem (item)

	
	def __set_properties(self):
		self.SetSize((256, 260))

	def __do_layout(self):
		mainSizer = wx.FlexGridSizer(1, 1, 0, 0)
		mainSizer.Add(self.toolbar, 1, wx.EXPAND, 0)
		mainSizer.Add(self.treeCtrl, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.AddGrowableRow(1)
		mainSizer.AddGrowableCol(0)
	

	def __treeUpdate (self, rootPage):
		"""
		Обновить дерево
		"""
		#self.Unbind (wx.EVT_TREE_SEL_CHANGED, handler = self.__onSelChanged)

		# Так как мы сами будем сворачивать/разворачивать узлы дерева, 
		# на эти события реагировать не надо пока строится дерево
		self.treeCtrl.Unbind (wx.EVT_TREE_ITEM_COLLAPSED, handler = self.__onTreeStateChanged)
		self.treeCtrl.Unbind (wx.EVT_TREE_ITEM_EXPANDED, handler = self.__onTreeStateChanged)
		
		self.treeCtrl.DeleteAllItems()
		self.imagelist.RemoveAll()
		self.defaultImageId = self.imagelist.Add (self.defaultBitmap)
		self._pageCache = {}

		if rootPage != None:
			rootname = os.path.basename (rootPage.path)
			rootItem = self.treeCtrl.AddRoot (rootname, 
					data = wx.TreeItemData (rootPage),
					image = self.defaultImageId)

			self.__mountItem (rootItem, rootPage)

			self.__appendChildren (rootPage, rootItem)
			self.selectedPage = rootPage.selectedPage
			self.treeCtrl.Expand (rootItem)

		#self.Bind (wx.EVT_TREE_SEL_CHANGED, self.__onSelChanged)
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_COLLAPSED, self.__onTreeStateChanged)
		self.treeCtrl.Bind (wx.EVT_TREE_ITEM_EXPANDED, self.__onTreeStateChanged)
	

	def __appendChildren (self, parentPage, parentItem):
		"""
		Добавить детей в дерево
		parentPage - родительская страница, куда добавляем дочерние страницы
		parentItem - родительский элемент дерева, куда добавляем дочерние элементы
		"""
		self._pageCache[parentPage] = parentItem

		for child in parentPage.children:
			item = self.__insertChild (child, parentItem)
			self.__mountItem (item, child)

		self.__loadExpandState (parentPage)


	def __mountItem (self, treeitem, page):
		"""
		Оформить элемент дерева в зависимости от настроек страницы (например, пометить только для чтения)
		"""
		if page.readonly:
			#font = self.treeCtrl.GetItemFont (treeitem)
			font = wx.SystemSettings.GetFont (wx.SYS_DEFAULT_GUI_FONT)
			font.SetStyle (wx.FONTSTYLE_ITALIC)
			self.treeCtrl.SetItemFont (treeitem, font)

	

	def __insertChild (self, child, parentItem):
		"""
		Вставить одну дочерниюю страницу (child) в ветвь, 
		где родителем является элемент parentItem
		"""
		item = self.treeCtrl.InsertItemBefore (parentItem, 
				child.order, 
				child.title, 
				data = wx.TreeItemData(child) )

		icon = child.icon

		if icon != None:
			image = wx.Bitmap (icon)
			image.SetHeight (self.iconHeight)
			imageId = self.imagelist.Add (image)
		else:
			imageId = self.defaultImageId
			
		self.treeCtrl.SetItemImage (item, imageId)

		self.__appendChildren (child, item)

		return item
	

	def __removePageItem (self, page):
		"""
		Удалить элемент, соответствующий странице
		"""
		item = self._pageCache[page]
		del self._pageCache[page]
		self.treeCtrl.Delete (item)


	def __updatePage (self, page):
		"""
		Обновить страницу (удалить из списка и добавить снова)
		"""
		#print page.title
		#print page.root.selectedPage.title

		# Отпишемся от обновлений страниц, чтобы не изменять выбранную страницу
		self.__unbindUpdateEvents()
		self.treeCtrl.Freeze()

		self.__removePageItem (page)

		#print page.title
		#print page.root.selectedPage.title

		item = self.__insertChild (page, self._pageCache[page.parent])

		#print page.title
		#print page.root.selectedPage.title

		if page.root.selectedPage == page:
			# Если обновляем выбранную страницу
			self.treeCtrl.SelectItem (item)

		self.__scrollToCurrentPage()
		self.treeCtrl.Thaw()
		self.__bindUpdateEvents()
	

	def __scrollToCurrentPage (self):
		"""
		Если текущая страницавылезла за пределы видимости, то прокрутить к ней
		"""
		selectedPage = Application.selectedPage
		if selectedPage == None:
			return

		item = self._pageCache[selectedPage]
		if not self.treeCtrl.IsVisible (item):
			self.treeCtrl.ScrollTo (item)
	

	def __getToolbar (self, parent, id):
		imagesDir = outwiker.core.system.getImagesDir()

		toolbar = wx.ToolBar (parent, id, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE)

		toolbar.AddLabelTool(self.ID_MOVE_DOWN, 
				_(u"Move Page Down"), 
				wx.Bitmap(os.path.join (imagesDir, "move_down.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Move Page Down"), 
				"")

		toolbar.AddLabelTool(self.ID_MOVE_UP, 
				_(u"Move Page Up"), 
				wx.Bitmap(os.path.join (imagesDir, "move_up.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Move Page Up"), 
				"")
		toolbar.AddSeparator()


		toolbar.AddLabelTool(self.ID_ADD_SIBLING_PAGE,
				_(u"Add Sibling Page…"), 
				wx.Bitmap(os.path.join (imagesDir, "node-insert-next.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Add Sibling Page…"), 
				"")

		toolbar.AddLabelTool(self.ID_ADD_CHILD_PAGE,
				_(u"Add Child Page…"), 
				wx.Bitmap(os.path.join (imagesDir, "node-insert-child.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Add Child Page…"), 
				"")

		toolbar.AddLabelTool(self.ID_REMOVE_PAGE,
				_(u"Remove Page…"), 
				wx.Bitmap(os.path.join (imagesDir, "node-delete.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Remove Page…"), 
				"")

		toolbar.AddSeparator()

		toolbar.AddLabelTool(self.ID_PROPERTIES_BUTTON,
				_(u"Page Properties…"), 
				wx.Bitmap(os.path.join (imagesDir, "edit.png"),
					wx.BITMAP_TYPE_ANY),
				wx.NullBitmap, 
				wx.ITEM_NORMAL,
				_(u"Page Properties…"), 
				"")


		toolbar.Realize()
		return toolbar
	

# end of class WikiTree

