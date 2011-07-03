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
from core.application import Application
from gui.trayicon import OutwikerTrayIcon
from gui.AttachPanel import AttachPanel
import core.config
import gui.pagedialog
from guiconfig import MainWindowConfig, TreeConfig, AttachConfig, GeneralGuiConfig
from .mainid import MainId
from mainmenu import MainMenu


class MainWindow(wx.Frame):
	def __init__(self, *args, **kwds):
		self.disabledTools = [MainId.ID_SAVE, MainId.ID_RELOAD, 
				MainId.ID_ADDPAGE, MainId.ID_ADDCHILD, MainId.ID_ATTACH, 
				MainId.ID_COPYPATH, MainId.ID_COPY_ATTACH_PATH, MainId.ID_COPY_LINK,
				MainId.ID_COPY_TITLE, MainId.ID_BOOKMARKS, MainId.ID_ADDBOOKMARK,
				MainId.ID_EDIT, MainId.ID_REMOVE_PAGE, MainId.ID_GLOBAL_SEARCH,
				wx.ID_UNDO, wx.ID_REDO, wx.ID_CUT, wx.ID_COPY, wx.ID_PASTE,
				MainId.ID_SORT_SIBLINGS_ALPHABETICAL, MainId.ID_SORT_CHILDREN_ALPHABETICAL,
				MainId.ID_MOVE_PAGE_UP, MainId.ID_MOVE_PAGE_DOWN, MainId.ID_RENAME]


		self.mainWindowConfig = MainWindowConfig (Application.config)
		self.treeConfig = TreeConfig (Application.config)
		self.attachConfig = AttachConfig (Application.config)
		self.generalConfig = GeneralGuiConfig (Application.config)

		# Флаг, обозначающий, что в цикле обработки стандартных сообщений 
		# вроде копирования в буфер обмена сообщение вернулось обратно
		self.stdEventLoop = False

		# Идентификаторы для пунктов меню последних открытых вики
		# Ключ - id, значение - путь до вики
		self._recentId = {}

		# Идентификаторы для пунктов меню для открытия закладок
		# Ключ - id, значение - путь до страницы вики
		self._bookmarksId = {}

		Application.onTreeUpdate += self.onTreeUpdate
		Application.onPageSelect += self.onPageSelect
		Application.onBookmarksChanged += self.onBookmarksChanged
		Application.onMainWindowConfigChange += self.onMainWindowConfigChange
		
		# Путь к директории с программой/скриптом
		self.imagesDir = core.system.getImagesDir()

		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)
		
		# Menu Bar
		self.mainMenu = MainMenu()
		self.SetMenuBar(self.mainMenu)
		# Menu Bar end
		
		# Tool Bar
		self.mainToolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE)
		self.SetToolBar(self.mainToolbar)
		self.mainToolbar.AddLabelTool(MainId.ID_NEW, _(u"New…"), wx.Bitmap(os.path.join (self.imagesDir, "new.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Create new wiki…"), "")
		self.mainToolbar.AddLabelTool(MainId.ID_OPEN, _(u"Open…"), wx.Bitmap(os.path.join (self.imagesDir, "open.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Open wiki…"), "")
		self.mainToolbar.AddLabelTool(MainId.ID_SAVE, _("Save"), wx.Bitmap(os.path.join (self.imagesDir, "save.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Save wiki"), "")
		self.mainToolbar.AddLabelTool(MainId.ID_RELOAD, _("Reload"), wx.Bitmap(os.path.join (self.imagesDir, "reload.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _("Reload wiki"), "")
		self.mainToolbar.AddSeparator()
		self.mainToolbar.AddLabelTool(MainId.ID_ATTACH, _(u"Attach files…"), wx.Bitmap(os.path.join (self.imagesDir, "attach.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Attach files…"), "")
		self.mainToolbar.AddLabelTool(MainId.ID_GLOBAL_SEARCH, _(u"Global search…"), wx.Bitmap(os.path.join (self.imagesDir, "global_search.png"), wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, _(u"Global search…"), "")
		self.mainToolbar.AddSeparator()
		# Tool Bar end
		self.mainPanel = wx.Panel(self, -1)
		self.statusbar = wx.StatusBar(self, -1)

		self.__set_properties()
		self.__do_layout()

		self.Bind(wx.EVT_MENU, self.onNew, id=MainId.ID_NEW)
		self.Bind(wx.EVT_MENU, self.onOpen, id=MainId.ID_OPEN)
		self.Bind(wx.EVT_MENU, self.onOpenReadOnly, id=MainId.ID_OPEN_READONLY)
		self.Bind(wx.EVT_MENU, self.onSave, id=MainId.ID_SAVE)
		self.Bind(wx.EVT_MENU, self.onPrint, id=wx.ID_PRINT)
		self.Bind(wx.EVT_MENU, self.onExit, id=MainId.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_REDO)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_CUT)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_COPY)
		self.Bind(wx.EVT_MENU, self.onStdEvent, id=wx.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.onPreferences, id=MainId.ID_PREFERENCES)
		self.Bind(wx.EVT_MENU, self.onAddSiblingPage, id=MainId.ID_ADDPAGE)
		self.Bind(wx.EVT_MENU, self.onAddChildPage, id=MainId.ID_ADDCHILD)
		self.Bind(wx.EVT_MENU, self.onMovePageUp, id=MainId.ID_MOVE_PAGE_UP)
		self.Bind(wx.EVT_MENU, self.onMovePageDown, id=MainId.ID_MOVE_PAGE_DOWN)
		self.Bind(wx.EVT_MENU, self.onSortChildrenAlphabetical, id=MainId.ID_SORT_CHILDREN_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.onSortSiblingAlphabetical, id=MainId.ID_SORT_SIBLINGS_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.onRename, id=MainId.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.onRemovePage, id=MainId.ID_REMOVE_PAGE)
		self.Bind(wx.EVT_MENU, self.onEditPage, id=MainId.ID_EDIT)
		self.Bind(wx.EVT_MENU, self.onGlobalSearch, id=MainId.ID_GLOBAL_SEARCH)
		self.Bind(wx.EVT_MENU, self.onAttach, id=MainId.ID_ATTACH)
		self.Bind(wx.EVT_MENU, self.onCopyTitle, id=MainId.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.onCopyPath, id=MainId.ID_COPYPATH)
		self.Bind(wx.EVT_MENU, self.onCopyAttaches, id=MainId.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.onCopyLink, id=MainId.ID_COPY_LINK)
		self.Bind(wx.EVT_MENU, self.onReload, id=MainId.ID_RELOAD)
		self.Bind(wx.EVT_MENU, self.onBookmark, id=MainId.ID_ADDBOOKMARK)
		self.Bind(wx.EVT_MENU, self.onViewTree, self.mainMenu.viewNotes)
		self.Bind(wx.EVT_MENU, self.onViewAttaches, self.mainMenu.viewAttaches)
		self.Bind(wx.EVT_MENU, self.onFullscreen, self.mainMenu.viewFullscreen)
		self.Bind(wx.EVT_MENU, self.onHelp, id=MainId.ID_HELP)
		self.Bind(wx.EVT_MENU, self.onAbout, id=MainId.ID_ABOUT)
		self.Bind(wx.EVT_TOOL, self.onNew, id=MainId.ID_NEW)
		self.Bind(wx.EVT_TOOL, self.onOpen, id=MainId.ID_OPEN)
		self.Bind(wx.EVT_TOOL, self.onReload, id=MainId.ID_RELOAD)
		self.Bind(wx.EVT_TOOL, self.onAttach, id=MainId.ID_ATTACH)
		self.Bind(wx.EVT_TOOL, self.onGlobalSearch, id=MainId.ID_GLOBAL_SEARCH)

		Application.onWikiOpen += self.onWikiOpen

		self.auiManager = wx.aui.AuiManager(self.mainPanel)

		self.tree = WikiTree(self.mainPanel, -1)
		self.pagePanel = CurrentPagePanel(self.mainPanel, -1)
		self.attachPanel = AttachPanel (self.mainPanel, -1)

		self.__loadMainWindowParams()
		self.__initAuiManager ()
		self.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.onPaneClose)

		self.Bind (wx.EVT_CLOSE, self.onClose)
		self.mainPanel.Bind (wx.EVT_CLOSE, self.onMainPanelClose)

		self._dropTarget = DropFilesTarget (self)

		self.__enableGui()

		self.statusbar.SetFieldsCount(1)

		aTable = wx.AcceleratorTable([
			(wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
			(wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
			(wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
		self.SetAcceleratorTable(aTable)

		self._updateRecentMenu()
		self.setFullscreen(self.mainWindowConfig.FullscreenOption.value)

		self.Show()

		if len (sys.argv) > 1:
			self._openFromCommandLine()
		else:
			# Открыть последний открытый файл (если установлена соответствующая опция)
			self.__openRecentWiki ()

		self.taskBarIcon = OutwikerTrayIcon(self)
		self.__updateTitle()

	
	def onWikiOpen (self, wikiroot):
		"""
		Обновить окно после того как загрузили вики
		"""
		if wikiroot != None and not wikiroot.readonly:
			try:
				self.recentWiki.add (wikiroot.path)
				self._updateRecentMenu()
			except IOError as e:
				core.commands.MessageBox (
						_(u"Can't add wiki to recent list.\nCan't save config.\n%s") % (unicode (e)),
						_(u"Error"), wx.ICON_ERROR | wx.OK)

		self.__enableGui()
		self._loadBookmarks()
		self.__updateTitle()


	def onMainPanelClose (self, event):
		self.tree.Close()
		self.tree = None

		self.pagePanel.Close()
		self.pagePanel = None

		self.attachPanel.Close()
		self.attachPanel = None
		
		self.mainPanel.Destroy()


	def __initAuiManager(self):
		self.__initPagePane (self.auiManager)
		self.__initAttachesPane (self.auiManager)
		self.__initTreePane (self.auiManager)
		self.__loadPanesSize ()

		self.auiManager.SetDockSizeConstraint (0.8, 0.8)
		self.auiManager.Update()

	
	def onPaneClose (self, event):
		if event.GetPane().name == self.auiManager.GetPane (self.tree).name:
			self.mainMenu.viewNotes.Check (False)
		elif event.GetPane().name == self.auiManager.GetPane (self.attachPanel).name:
			self.mainMenu.viewAttaches.Check (False)


	def __initTreePane (self, auiManager):
		"""
		Загрузить настройки окошка с деревом
		"""
		pane = self.__loadPaneInfo (self.treeConfig.treePaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name(("treePane")).Caption(_("Notes")).Gripper(False).CaptionVisible(True).Layer(2).Position(0).CloseButton(True).MaximizeButton(False).Left().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		pane.CloseButton()

		pane.BestSize ((self.treeConfig.treeWidthOption.value, 
			self.treeConfig.treeHeightOption.value))
		
		auiManager.AddPane(self.tree, pane)
	

	def __initAttachesPane (self, auiManager):
		"""
		Загрузить настройки окошка с прикрепленными файлами
		"""
		pane = self.__loadPaneInfo (self.attachConfig.attachesPaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name("attachesPane").Caption(_("Attaches")).Gripper(False).CaptionVisible(True).Layer(1).Position(0).CloseButton(True).MaximizeButton(False).Bottom().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		pane.CloseButton()

		auiManager.AddPane(self.attachPanel, pane, _('Attaches') )
	

	def __initPagePane (self, auiManager):
		"""
		Загрузить настройки окошка с видом текущей страницы
		"""
		pane = wx.aui.AuiPaneInfo().Name("pagePane").Gripper(False).CaptionVisible(False).Layer(0).Position(0).CloseButton(False).MaximizeButton(False).Center().Dock()

		auiManager.AddPane(self.pagePanel, pane)
	

	def __loadPaneInfo (self, param):
		"""
		Загрузить из конфига и вернуть информацию о dockable-панели (AuiPaneInfo)
		"""
		string_info = param.value

		if len (string_info) == 0:
			return

		pane = wx.aui.AuiPaneInfo()
		try:
			self.auiManager.LoadPaneInfo (string_info, pane)
		except Exception, e:
			return

		return pane


	def __savePaneInfo (self, param, paneInfo):
		"""
		Сохранить в конфиг информацию о dockable-панели (AuiPaneInfo)
		"""
		string_info = self.auiManager.SavePaneInfo (paneInfo)
		param.value = string_info


	def __savePanesParams (self):
		"""
		Сохранить параметры панелей
		"""
		self.__savePaneInfo (self.treeConfig.treePaneOption, self.auiManager.GetPane (self.tree))
		self.__savePaneInfo (self.attachConfig.attachesPaneOption, self.auiManager.GetPane (self.attachPanel))
		self.__savePanesSize()
	

	def __savePanesSize (self):
		"""
		Сохранить размеры панелей
		"""
		self.treeConfig.treeWidthOption.value = self.tree.GetSizeTuple()[0]
		self.treeConfig.treeHeightOption.value = self.tree.GetSizeTuple()[1]
			
		self.attachConfig.attachesWidthOption.value = self.attachPanel.GetSizeTuple()[0]
		self.attachConfig.attachesHeightOption.value = self.attachPanel.GetSizeTuple()[1]
		
		#print "save:"
		#print self.attachConfig.attachesWidthOption.value
		#print self.attachConfig.attachesHeightOption.value


	def onPageSelect (self, newpage):
		self.__updateTitle()
	

	def __updateTitle (self):
		template = self.mainWindowConfig.titleFormatOption.value

		if Application.wikiroot == None:
			self.SetTitle (u"OutWiker")
			return

		pageTitle = u"" if Application.wikiroot.selectedPage == None else Application.wikiroot.selectedPage.title
		filename = os.path.basename (Application.wikiroot.path)

		result = template.replace ("{file}", filename).replace ("{page}", pageTitle)
		self.SetTitle (result)
	

	def __enableGui (self):
		"""
		Проверить открыта ли вики и включить или выключить кнопки на панели
		"""
		enabled = Application.wikiroot != None
		self.__enableTools (enabled)
		self.__enableMenu (enabled)
		self.pagePanel.Enable(enabled)
		self.tree.Enable(enabled)
		self.attachPanel.Enable(enabled)


	
	def __enableTools (self, enabled):
		for toolId in self.disabledTools:
			if self.mainToolbar.FindById (toolId) != None:
				self.mainToolbar.EnableTool (toolId, enabled)

	
	def __enableMenu (self, enabled):
		for toolId in self.disabledTools:
			if self.mainMenu.FindItemById (toolId) != None:
				self.mainMenu.Enable (toolId, enabled)


	def __openRecentWiki (self):
		"""
		Открыть последнюю вики, если установлена соответствующая опция
		"""
		openRecent = self.generalConfig.autoopenOption.value

		if openRecent and len (self.recentWiki) > 0:
			core.commands.openWiki (self.recentWiki[0])


	def _openFromCommandLine (self):
		"""
		Открыть вики, путь до которой передан в командной строке
		"""
		fname = unicode (sys.argv[1], core.system.getOS().filesEncoding)
		if not os.path.isdir (fname):
			fname = os.path.split (fname)[0]

		core.commands.openWiki (fname)

	
	def _updateRecentMenu (self):
		"""
		Обновление меню со списком последних открытых вики
		"""
		self._removeMenuItemsById (self.mainMenu.fileMenu, self._recentId.keys())
		self._recentId = {}

		# TODO: Рефакторинг
		# Сделать класс RecentWiki изменяемым
		self.recentWiki = RecentWiki (Application.config)

		self._recentId = {}

		for n in range (len (self.recentWiki)):
			id = wx.NewId()
			path = self.recentWiki[n]
			self._recentId[id] = path

			title = path if n + 1 > 9 else u"&{n}. {path}".format (n=n + 1, path=path)

			self.mainMenu.fileMenu.Append (id, title, "", wx.ITEM_NORMAL)
			
			self.Bind(wx.EVT_MENU, self.onRecent, id=id)
	

	def _loadBookmarks (self):
		self._removeMenuItemsById (self.mainMenu.bookmarksMenu, self._bookmarksId.keys())
		self._bookmarksId = {}

		if Application.wikiroot != None:
			for n in range (len (Application.wikiroot.bookmarks)):
				id = wx.NewId()
				page = Application.wikiroot.bookmarks[n]
				if page == None:
					continue

				subpath = page.subpath
				self._bookmarksId[id] = subpath

				# Найдем родителя
				parent = page.parent

				if parent.parent != None:
					label = "%s [%s]" % (page.title, parent.subpath)
				else:
					label = page.title

				self.mainMenu.bookmarksMenu.Append (id, label, "", wx.ITEM_NORMAL)
				self.Bind(wx.EVT_MENU, self.onSelectBookmark, id=id)


	def _removeMenuItemsById (self, menu, keys):
		"""
		Удалить все элементы меню по идентификаторам
		"""
		for key in keys:
			menu.Delete (key)
			self.Unbind (wx.EVT_MENU, id = key)


	def onRecent (self, event):
		"""
		Выбор пункта меню с недавно открытыми файлами
		"""
		core.commands.openWiki (self._recentId[event.Id])


	def onSelectBookmark (self, event):
		subpath = self._bookmarksId[event.Id]
		page = Application.wikiroot[subpath]

		if page != None:
			Application.wikiroot.selectedPage = Application.wikiroot[subpath]
	

	def __loadMainWindowParams(self):
		"""
		Загрузить параметры из конфига
		"""
		#config = Application.config
		self.Freeze()

		width = self.mainWindowConfig.WidthOption.value
		height = self.mainWindowConfig.HeightOption.value

		xpos = self.mainWindowConfig.XPosOption.value
		ypos = self.mainWindowConfig.YPosOption.value
		
		self.SetDimensions (xpos, ypos, width, height, sizeFlags=wx.SIZE_FORCE)

		self.Layout()
		self.Thaw()
	

	def __saveParams (self):
		"""
		Сохранить параметры в конфиг
		"""
		#config = Application.config

		try:
			if not self.IsIconized():
				if not self.IsFullScreen():
					(width, height) = self.GetSizeTuple()
					self.mainWindowConfig.WidthOption.value = width
					self.mainWindowConfig.HeightOption.value = height

					(xpos, ypos) = self.GetPositionTuple()
					self.mainWindowConfig.XPosOption.value = xpos
					self.mainWindowConfig.YPosOption.value = ypos

				self.mainWindowConfig.FullscreenOption.value = self.IsFullScreen()

				self.__savePanesParams()
		except Exception, e:
			core.commands.MessageBox (_(u"Can't save config\n%s") % (unicode (e)),
					_(u"Error"), wx.ICON_ERROR | wx.OK)
	

	def __set_properties(self):
		self.SetTitle(_("OutWiker"))
		_icon = wx.EmptyIcon()
		_icon.CopyFromBitmap(wx.Bitmap(os.path.join (self.imagesDir, "icon.ico"), wx.BITMAP_TYPE_ANY))
		self.SetIcon(_icon)
		self.SetSize((400, 402))
		self.mainToolbar.Realize()


	def __do_layout(self):
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		mainSizer.Add(self.mainPanel, 1, wx.EXPAND, 0)
		mainSizer.Add(self.statusbar, 1, wx.EXPAND, 0)
		self.SetSizer(mainSizer)
		mainSizer.AddGrowableRow(0)
		mainSizer.AddGrowableCol(0)
		self.Layout()


	def onClose (self, event):
		askBeforeExit = self.generalConfig.askBeforeExitOption.value

		if (not askBeforeExit or 
				core.commands.MessageBox (_(u"Really exit?"), _(u"Exit"), wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES):
			self.__saveParams()

			self.auiManager.UnInit()
			self.mainPanel.Close()

			self.taskBarIcon.Destroy()
			self.Destroy()
		else:
			event.Veto()
	

	def onMainWindowConfigChange (self):
		self.__updateTitle()


	def onTreeUpdate (self, sender):
		"""
		Событие при обновлении дерева
		"""
		self._loadBookmarks()
		self.__updateTitle()


	def onNew(self, event): 
		core.commands.createNewWiki(self)


	def onOpen(self, event):
		core.commands.openWikiWithDialog (self)
	

	def onSave(self, event):
		Application.onForceSave()


	def onReload(self, event):
		core.commands.reloadWiki (self)
	

	def destroyPagePanel (self, save):
		"""
		Уничтожить панель с текущей страницей.
		save - надо ли предварительно сохранить страницу?
		"""
		if save:
			self.pagePanel.destroyPageView()
		else:
			self.pagePanel.destroyWithoutSave()


	def onAddSiblingPage(self, event):
		"""
		Создание страницы на уровне текущей страницы
		"""
		gui.pagedialog.createSiblingPage (self)

	
	def onAddChildPage(self, event):
		"""
		Создание дочерней страницы
		"""
		gui.pagedialog.createChildPage (self)


	def onAttach(self, event):
		if Application.selectedPage != None:
			core.commands.attachFilesWithDialog (self, Application.wikiroot.selectedPage)

	def onAbout(self, event):
		core.commands.showAboutDialog (self)


	def onExit(self, event):
		self.Close()


	def onCopyPath(self, event):
		if Application.selectedPage != None:
			core.commands.copyPathToClipboard (Application.wikiroot.selectedPage)


	def onCopyAttaches(self, event):
		if Application.selectedPage != None:
			core.commands.copyAttachPathToClipboard (Application.wikiroot.selectedPage)

	
	def onCopyLink(self, event):
		if Application.selectedPage != None:
			core.commands.copyLinkToClipboard (Application.wikiroot.selectedPage)

	
	def onCopyTitle(self, event):
		if Application.selectedPage != None:
			core.commands.copyTitleToClipboard (Application.wikiroot.selectedPage)
	

	def onBookmarksChanged (self, event):
		self._loadBookmarks()


	def onBookmark(self, event):
		if Application.selectedPage != None:
			selectedPage = Application.wikiroot.selectedPage

			if not Application.wikiroot.bookmarks.pageMarked (selectedPage):
				Application.wikiroot.bookmarks.add (Application.wikiroot.selectedPage)
			else:
				Application.wikiroot.bookmarks.remove (Application.wikiroot.selectedPage)


	def onEditPage(self, event):
		if Application.selectedPage != None:
			gui.pagedialog.editPage (self, Application.selectedPage)


	def onRemovePage(self, event):
		if Application.selectedPage != None:
			core.commands.removePage (Application.wikiroot.selectedPage)


	@core.commands.testreadonly
	def onGlobalSearch(self, event):
		if Application.wikiroot != None:
			try:
				pages.search.searchpage.GlobalSearch.create (Application.wikiroot)
			except IOError:
				core.commands.MessageBox (_(u"Can't create page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


	def onStdEvent(self, event):
		if not self.stdEventLoop:
			self.stdEventLoop = True
			target = wx.Window.FindFocus()

			if target != None:
				target.ProcessEvent (event)
		self.stdEventLoop = False


	def onRename(self, event):
		self.tree.beginRename()


	def onHelp(self, event):
		core.commands.openHelp()


	def onOpenReadOnly(self, event):
		core.commands.openWikiWithDialog (self, readonly=True)


	def onPreferences(self, event):
		dlg = PrefDialog (self)
		dlg.ShowModal()
		dlg.Destroy()
	

	def onViewTree(self, event):
		self.showHideTree()
	

	def __showHidePane (self, control):
		"""
		Показать / скрыть pane с некоторым контролом
		"""
		pane = self.auiManager.GetPane (control)

		self.__savePanesSize()

		if pane.IsShown():
			pane.Hide()
		else:
			pane.Show()

		self.__loadPanesSize ()
		self.__updateViewMenu()
	

	def showHideTree (self):
		"""
		Показать/спарятать дерево с заметками
		"""
		self.__showHidePane (self.tree)

	
	def showHideAttaches (self):
		"""
		Показать/спарятать дерево с заметками
		"""
		self.__showHidePane (self.attachPanel)


	def onViewAttaches(self, event):
		self.showHideAttaches()


	def onFullscreen(self, event):
		self.setFullscreen(not self.IsFullScreen())


	def setFullscreen (self, fullscreen):
		"""
		Установить параметры в зависимости от режима fullscreen
		"""
		if fullscreen:
			self.__toFullscreen()
		else:
			self.__fromFullscreen()


	def __toFullscreen(self):
		self.__savePanesSize()
		self.ShowFullScreen(True, wx.FULLSCREEN_NOTOOLBAR | wx.FULLSCREEN_NOBORDER | wx.FULLSCREEN_NOCAPTION)
		self.auiManager.GetPane (self.attachPanel).Hide()
		self.auiManager.GetPane (self.tree).Hide()
		self.auiManager.Update()
		self.__updateViewMenu()


	def __fromFullscreen (self):
		self.__loadMainWindowParams()
		self.ShowFullScreen(False)
		self.auiManager.GetPane (self.attachPanel).Show()
		self.auiManager.GetPane (self.tree).Show()
		self.__loadPanesSize ()
		self.__updateViewMenu()

	
	def __loadPanesSize (self):
		self.auiManager.GetPane (self.attachPanel).BestSize ((self.attachConfig.attachesWidthOption.value, 
			self.attachConfig.attachesHeightOption.value))

		self.auiManager.GetPane (self.tree).BestSize ((self.treeConfig.treeWidthOption.value, 
			self.treeConfig.treeHeightOption.value))

		self.auiManager.Update()
	

	def __updateViewMenu (self):
		self.mainMenu.viewNotes.Check (self.auiManager.GetPane (self.tree).IsShown())
		self.mainMenu.viewAttaches.Check (self.auiManager.GetPane (self.attachPanel).IsShown())
		self.mainMenu.viewFullscreen.Check (self.IsFullScreen())


	def onMovePageUp(self, event):
		core.commands.moveCurrentPageUp()


	def onMovePageDown(self, event):
		core.commands.moveCurrentPageDown()
		

	def onSortChildrenAlphabetical(self, event):
		core.commands.sortChildrenAlphabeticalGUI()


	def onSortSiblingAlphabetical(self, event):
		core.commands.sortSiblingsAlphabeticalGUI()


	def onPrint(self, event):
		self.pagePanel.Print()

# end of class MainWindow


class DropFilesTarget (wx.FileDropTarget):
	def __init__ (self, mainWindow):
		wx.FileDropTarget.__init__ (self)
		self._mainWindow = mainWindow
		self._mainWindow.SetDropTarget (self)
	
	
	def OnDropFiles (self, x, y, files):
		if (Application.wikiroot != None and
				Application.wikiroot.selectedPage != None):
			core.commands.attachFiles (self._mainWindow, 
						Application.wikiroot.selectedPage, 
						files)
			return True
