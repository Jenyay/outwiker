#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import sys

import wx
import wx.aui

from outwiker.core.tree import WikiDocument, RootWikiPage
import outwiker.core.config
import outwiker.core.commands
import outwiker.core.system
from outwiker.core.application import Application

from .WikiTree import WikiTree
import outwiker.pages.search.searchpage
from .guiconfig import MainWindowConfig, TreeConfig, AttachConfig, GeneralGuiConfig

from .mainid import MainId
from .CurrentPagePanel import CurrentPagePanel
from .mainmenu import MainMenu
from .maintoolbar import MainToolBar
from .pagedialog import createSiblingPage, createChildPage, editPage
from .trayicon import OutwikerTrayIcon
from .AttachPanel import AttachPanel
from .preferences.PrefDialog import PrefDialog
from .mainwndcontroller import MainWndController


class MainWindow(wx.Frame):
	def __init__(self, *args, **kwds):
		kwds["style"] = wx.DEFAULT_FRAME_STYLE
		wx.Frame.__init__(self, *args, **kwds)

		self.mainWindowConfig = MainWindowConfig (Application.config)
		self.treeConfig = TreeConfig (Application.config)
		self.attachConfig = AttachConfig (Application.config)
		self.generalConfig = GeneralGuiConfig (Application.config)

		# Флаг, обозначающий, что в цикле обработки стандартных сообщений 
		# (например, копирования в буфер обмена) сообщение вернулось обратно
		self.__stdEventLoop = False

		self.__setIcon()
		self.SetTitle (u"OutWiker")

		self.__createMenu()
		self.__createToolBar()
		self.__createStatusBar()

		self.controller = MainWndController (self)
		self.controller.loadMainWindowParams()

		self.__createAuiPanes (self)

		self.__bindGuiEvents()

		self._dropTarget = DropFilesTarget (self.attachPanel)
		self.controller.enableGui()
		self.__createAcceleratorTable()
		self.controller.updateRecentMenu()
		self.setFullscreen(self.mainWindowConfig.FullscreenOption.value)
		self.Show()
		self.taskBarIcon = OutwikerTrayIcon(self)


	def __createAcceleratorTable (self):
		"""
		Создать горячие клавиши, которые не попали в меню
		"""
		aTable = wx.AcceleratorTable([
			(wx.ACCEL_CTRL,  wx.WXK_INSERT, wx.ID_COPY),
			(wx.ACCEL_SHIFT,  wx.WXK_INSERT, wx.ID_PASTE),
			(wx.ACCEL_SHIFT,  wx.WXK_DELETE, wx.ID_CUT)])
		self.SetAcceleratorTable(aTable)


	def __createStatusBar (self):
		self.statusbar = wx.StatusBar(self, -1)
		self.statusbar.SetFieldsCount(1)
		self.SetStatusBar (self.statusbar)


	def __createMenu (self):
		self.mainMenu = MainMenu()
		self.SetMenuBar(self.mainMenu)


	def __createToolBar (self):
		self.mainToolbar = MainToolBar (self, -1, style=wx.TB_HORIZONTAL|wx.TB_FLAT|wx.TB_DOCKABLE)
		self.SetToolBar(self.mainToolbar)


	def __bindGuiEvents (self):
		"""
		Подписаться на события меню, кнопок и т.п.
		"""
		self.Bind(wx.EVT_MENU, self.__onNew, id=MainId.ID_NEW)
		self.Bind(wx.EVT_MENU, self.__onOpen, id=MainId.ID_OPEN)
		self.Bind(wx.EVT_MENU, self.__onOpenReadOnly, id=MainId.ID_OPEN_READONLY)
		self.Bind(wx.EVT_MENU, self.__onSave, id=MainId.ID_SAVE)
		self.Bind(wx.EVT_MENU, self.__onPrint, id=wx.ID_PRINT)
		self.Bind(wx.EVT_MENU, self.__onExit, id=MainId.ID_EXIT)
		self.Bind(wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_UNDO)
		self.Bind(wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_REDO)
		self.Bind(wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_CUT)
		self.Bind(wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_COPY)
		self.Bind(wx.EVT_MENU, self.__onStdEvent, id=MainId.ID_PASTE)
		self.Bind(wx.EVT_MENU, self.__onPreferences, id=MainId.ID_PREFERENCES)
		self.Bind(wx.EVT_MENU, self.__onAddSiblingPage, id=MainId.ID_ADDPAGE)
		self.Bind(wx.EVT_MENU, self.__onAddChildPage, id=MainId.ID_ADDCHILD)
		self.Bind(wx.EVT_MENU, self.__onMovePageUp, id=MainId.ID_MOVE_PAGE_UP)
		self.Bind(wx.EVT_MENU, self.__onMovePageDown, id=MainId.ID_MOVE_PAGE_DOWN)
		self.Bind(wx.EVT_MENU, self.__onSortChildrenAlphabetical, id=MainId.ID_SORT_CHILDREN_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.__onSortSiblingAlphabetical, id=MainId.ID_SORT_SIBLINGS_ALPHABETICAL)
		self.Bind(wx.EVT_MENU, self.__onRename, id=MainId.ID_RENAME)
		self.Bind(wx.EVT_MENU, self.__onRemovePage, id=MainId.ID_REMOVE_PAGE)
		self.Bind(wx.EVT_MENU, self.__onEditPage, id=MainId.ID_EDIT)
		self.Bind(wx.EVT_MENU, self.__onGlobalSearch, id=MainId.ID_GLOBAL_SEARCH)
		self.Bind(wx.EVT_MENU, self.__onAttach, id=MainId.ID_ATTACH)
		self.Bind(wx.EVT_MENU, self.__onCopyTitle, id=MainId.ID_COPY_TITLE)
		self.Bind(wx.EVT_MENU, self.__onCopyPath, id=MainId.ID_COPYPATH)
		self.Bind(wx.EVT_MENU, self.__onCopyAttaches, id=MainId.ID_COPY_ATTACH_PATH)
		self.Bind(wx.EVT_MENU, self.__onCopyLink, id=MainId.ID_COPY_LINK)
		self.Bind(wx.EVT_MENU, self.__onReload, id=MainId.ID_RELOAD)
		self.Bind(wx.EVT_MENU, self.__onViewTree, self.mainMenu.viewNotes)
		self.Bind(wx.EVT_MENU, self.__onViewAttaches, self.mainMenu.viewAttaches)
		self.Bind(wx.EVT_MENU, self.__onFullscreen, self.mainMenu.viewFullscreen)
		self.Bind(wx.EVT_MENU, self.__onHelp, id=MainId.ID_HELP)
		self.Bind(wx.EVT_MENU, self.__onAbout, id=MainId.ID_ABOUT)
		self.Bind(wx.EVT_TOOL, self.__onNew, id=MainId.ID_NEW)
		self.Bind(wx.EVT_TOOL, self.__onOpen, id=MainId.ID_OPEN)
		self.Bind(wx.EVT_TOOL, self.__onReload, id=MainId.ID_RELOAD)
		self.Bind(wx.EVT_TOOL, self.__onAttach, id=MainId.ID_ATTACH)
		self.Bind(wx.EVT_TOOL, self.__onGlobalSearch, id=MainId.ID_GLOBAL_SEARCH)
		self.Bind (wx.EVT_CLOSE, self.__onClose)

	
	def __createAuiPanes(self, parent):
		self.auiManager = wx.aui.AuiManager(parent)

		self.tree = WikiTree(parent, -1)
		self.pagePanel = CurrentPagePanel(parent, -1)
		self.attachPanel = AttachPanel (parent, -1)

		self.__initPagePane (self.auiManager)
		self.__initAttachesPane (self.auiManager)
		self.__initTreePane (self.auiManager)
		self.__loadPanesSize ()

		self.auiManager.SetDockSizeConstraint (0.8, 0.8)
		self.auiManager.Update()

		self.auiManager.Bind (wx.aui.EVT_AUI_PANE_CLOSE, self.__onPaneClose)

	
	def __onPaneClose (self, event):
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
			pane = wx.aui.AuiPaneInfo().Name(("treePane")).Caption(_(u"Notes")).Gripper(False).CaptionVisible(True).Layer(2).Position(0).CloseButton(True).MaximizeButton(False).Left().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		pane.CloseButton()
		pane.Caption(_(u"Notes"))

		pane.BestSize ((self.treeConfig.treeWidthOption.value, 
			self.treeConfig.treeHeightOption.value))
		
		auiManager.AddPane(self.tree, pane)
	

	def __initAttachesPane (self, auiManager):
		"""
		Загрузить настройки окошка с прикрепленными файлами
		"""
		pane = self.__loadPaneInfo (self.attachConfig.attachesPaneOption)

		if pane == None:
			pane = wx.aui.AuiPaneInfo().Name("attachesPane").Caption(_(u"Attaches")).Gripper(False).CaptionVisible(True).Layer(1).Position(0).CloseButton(True).MaximizeButton(False).Bottom().Dock()

		# Из-за глюка http://trac.wxwidgets.org/ticket/12422 придется пока отказаться от плавающих панелек
		pane.Dock()
		pane.CloseButton()
		pane.Caption(_(u"Attaches"))

		auiManager.AddPane(self.attachPanel, pane, _(u"Attaches") )
	

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

	
	def __saveParams (self):
		"""
		Сохранить параметры в конфиг
		"""
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
			outwiker.core.commands.MessageBox (_(u"Can't save config\n%s") % (unicode (e)),
					_(u"Error"), wx.ICON_ERROR | wx.OK)
	

	def __setIcon (self):
		icon = wx.EmptyIcon()
		icon.CopyFromBitmap(wx.Bitmap(os.path.join (outwiker.core.system.getImagesDir(), "outwiker.ico"), 
			wx.BITMAP_TYPE_ANY))

		self.SetIcon(icon)


	def __onClose (self, event):
		askBeforeExit = self.generalConfig.askBeforeExitOption.value

		if (not askBeforeExit or 
				outwiker.core.commands.MessageBox (_(u"Really exit?"), _(u"Exit"), wx.YES_NO  | wx.ICON_QUESTION ) == wx.YES):
			self.__saveParams()

			self.auiManager.UnInit()

			self.tree.Close()
			self.tree = None

			self.pagePanel.Close()
			self.pagePanel = None

			self.attachPanel.Close()
			self.attachPanel = None

			self.statusbar.Close()
			
			self.taskBarIcon.Destroy()
			self.controller.destroy()

			self.Destroy()
		else:
			event.Veto()
	

	def __onNew(self, event): 
		outwiker.core.commands.createNewWiki(self)


	def __onOpen(self, event):
		outwiker.core.commands.openWikiWithDialog (self)
	

	def __onSave(self, event):
		Application.onForceSave()


	def __onReload(self, event):
		outwiker.core.commands.reloadWiki (self)
	

	def destroyPagePanel (self, save):
		"""
		Уничтожить панель с текущей страницей.
		save - надо ли предварительно сохранить страницу?
		"""
		if save:
			self.pagePanel.destroyPageView()
		else:
			self.pagePanel.destroyWithoutSave()


	def __onAddSiblingPage(self, event):
		"""
		Создание страницы на уровне текущей страницы
		"""
		createSiblingPage (self)

	
	def __onAddChildPage(self, event):
		"""
		Создание дочерней страницы
		"""
		createChildPage (self)


	def __onAttach(self, event):
		if Application.selectedPage != None:
			outwiker.core.commands.attachFilesWithDialog (self, Application.wikiroot.selectedPage)

	def __onAbout(self, event):
		outwiker.core.commands.showAboutDialog (self)


	def __onExit(self, event):
		self.Close()


	def __onCopyPath(self, event):
		if Application.selectedPage != None:
			outwiker.core.commands.copyPathToClipboard (Application.wikiroot.selectedPage)


	def __onCopyAttaches(self, event):
		if Application.selectedPage != None:
			outwiker.core.commands.copyAttachPathToClipboard (Application.wikiroot.selectedPage)

	
	def __onCopyLink(self, event):
		if Application.selectedPage != None:
			outwiker.core.commands.copyLinkToClipboard (Application.wikiroot.selectedPage)

	
	def __onCopyTitle(self, event):
		if Application.selectedPage != None:
			outwiker.core.commands.copyTitleToClipboard (Application.wikiroot.selectedPage)
	

	def __onEditPage(self, event):
		if Application.selectedPage != None:
			editPage (self, Application.selectedPage)


	def __onRemovePage(self, event):
		if Application.selectedPage != None:
			outwiker.core.commands.removePage (Application.wikiroot.selectedPage)


	@outwiker.core.commands.testreadonly
	def __onGlobalSearch(self, event):
		if Application.wikiroot != None:
			try:
				outwiker.pages.search.searchpage.GlobalSearch.create (Application.wikiroot)
			except IOError:
				outwiker.core.commands.MessageBox (_(u"Can't create page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


	def __onStdEvent(self, event):
		if not self.__stdEventLoop:
			self.__stdEventLoop = True
			target = wx.Window.FindFocus()

			if target != None:
				target.ProcessEvent (event)
		self.__stdEventLoop = False


	def __onRename(self, event):
		self.tree.beginRename()


	def __onHelp(self, event):
		outwiker.core.commands.openHelp()


	def __onOpenReadOnly(self, event):
		outwiker.core.commands.openWikiWithDialog (self, readonly=True)


	def __onPreferences(self, event):
		with PrefDialog (self) as dlg:
			dlg.ShowModal()
	

	def __onViewTree(self, event):
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


	def __onViewAttaches(self, event):
		self.showHideAttaches()


	def __onFullscreen(self, event):
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
		self.controller.loadMainWindowParams()
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


	def __onMovePageUp(self, event):
		outwiker.core.commands.moveCurrentPageUp()


	def __onMovePageDown(self, event):
		outwiker.core.commands.moveCurrentPageDown()
		

	def __onSortChildrenAlphabetical(self, event):
		outwiker.core.commands.sortChildrenAlphabeticalGUI()


	def __onSortSiblingAlphabetical(self, event):
		outwiker.core.commands.sortSiblingsAlphabeticalGUI()


	def __onPrint(self, event):
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
			outwiker.core.commands.attachFiles (self._mainWindow, 
						Application.wikiroot.selectedPage, 
						files)
			return True
