#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from event import Event

class Controller(object):
	"""
	Контроллер для обработки событий от дерева и связи его с другими частями
	"""

	_instance = None

	def __init__(self):
		"""
		Constructor.
		"""
		# Обновление страницы
		# Параметры: sender
		self.onPageUpdate = Event()

		# Создание страницы
		# Параметры: sender
		self.onPageCreate = Event()

		# Обновление дерева
		# Параметры: sender - из-за кого обновляется дерево
		self.onTreeUpdate = Event()
		
		# Выбор новой страницы
		# Параметры: новая выбранная страница
		self.onPageSelect = Event()

		# Пользователь хочет скопировать выбранные файлы в страницу
		# Параметры: fnames - выбранные имена файлов (basename без путей)
		self.onAttachmentPaste = Event()

		# Изменение списка закладок
		# Параметр - экземпляр класса Bookmarks
		self.onBookmarksChanged = Event()

		# Удаленеи страницы
		# Параметр - удаленная страница
		self.onPageRemove = Event()

		# Переименование страницы.
		# Параметры: page - переименованная страница, oldSubpath - старый относительный путь до страницы
		self.onPageRename = Event()

		# Начало сложного обновления дерева
		# Параметры: root - корень дерева
		self.onStartTreeUpdate = Event()

		# Конец сложного обновления дерева
		# Параметры: root - корень дерева
		self.onEndTreeUpdate = Event()

		# Вызывается перед тем, как закрыть открытую вики или открыть другую вики
		# Параметры: root - корень дерева
		self.onWikiClose = Event()
		
		# Начало рендеринга HTML
		# Параметры: 
		# page - страница, которую рендерят
		# htmlView - окно, где будет представлен HTML
		self.onHtmlRenderingBegin = Event()
		
		# Завершение рендеринга HTML
		# Параметры: 
		# page - страница, которую рендерят
		# htmlView - окно, где будет представлен HTML
		self.onHtmlRenderingEnd = Event()

		# Изменение настроек редактора
		# Параметры: нет
		self.onEditorConfigChange = Event()

		# Изменение настроек главного окна
		# Параметры: нет
		self.onMainWindowConfigChange = Event()

		# Изменение порядка страниц
		# Параметры: page - страница, положение которой изменили
		self.onPageOrderChange = Event()

		# Событие на принудительное сохранение состояния страницы
		# Например, при потере фокуса приложением.
		# Параметры: нет
		self.onForceSave = Event()

		# Копировать в буфер обмена
		#self.onClipboardCopy = Event()
		
		# Вырезать в буфер обмена
		#self.onClipboardCut = Event()

		# Вставить из буфера обмена
		#self.onClipboardPaste() = Event()

	@staticmethod
	def instance ():
		if Controller._instance == None:
			Controller._instance = Controller()

		return Controller._instance
