# -*- coding: UTF-8 -*-
"""
Версия 1.1
"""

import wx


class Shortcuter (object):
    """Класс для расстановки шорткатов в меню для wxPython"""
    def __init__(self, menubar):
        self._menubar = menubar


    def assignShortcuts (self):
        """
        Расставить клавишные сокращения (шорткаты) для доступа к меню (с использованием комбинаций, Alt+...)
        Метод проходит по всем меню и расставляет подчеркивания там, где их еще нет.
        """
        # Проверить сокращения для заголовков меню первого уровня
        self._assignMenuShortcuts (self._menubar)
        self._menubar.UpdateMenus()


    def checkDuplicateShortcuts (self):
        """
        Проверить шорткаты на повторы.
        Возвращает множество заголовков с дублирующимися шорткатами
        """
        duplicates = set()
        self._checkDuplicatesShortcuts (self._menubar, duplicates)

        result = list (duplicates)
        result.sort (key=lambda item: self._extractShortcut (item))

        return result


    def checkDuplacateHotKeys (self):
        """
        Проверить горячие клавиши на повторы во всем меню.
        Возвращает множество заголовков с дублирующимися горячими клавишами
        """
        duplicates = set()
        self._checkDuplicatesHotKeys (self._menubar, duplicates)

        result = list (duplicates)
        result.sort (key=lambda item: self._extractHotKey (item))

        return result


    def _checkDuplicatesHotKeys (self, menu, duplicates, hotkeysDict={}):
        """
        menu - меню, в котором проверяются горячие клавиши
        duplicates - множество пунктов меню, в которых горячие клавиши совпадают
        hotkeysDict - словарь полученных горячих клавиш. Ключ - горячая клавиша, значение - пункт меню
        """
        menuitems = self._getMenuItems (menu)

        for menuitem, position in zip (menuitems, range(len (menuitems))):
            title = self._getText (menuitem, position)
            hotkey = self._extractHotKey (title)

            if hotkey in hotkeysDict:
                duplicates.add (hotkeysDict[hotkey])
                duplicates.add (title)

            if len (hotkey) != 0:
                hotkeysDict[hotkey] = title

            submenu = self._getSubMenu (menuitem)
            if submenu is not None:
                self._checkDuplicatesHotKeys (submenu, duplicates, hotkeysDict)


    def _checkDuplicatesShortcuts (self, menu, duplicates):
        def addDuplicates (oldtitle, newtitle):
            duplicates.add (oldtitle)
            duplicates.add (newtitle)

        self._getExistingShortcuts (menu, addDuplicates)

        menuitems = self._getMenuItems (menu)

        for menuitem in menuitems:
            submenu = self._getSubMenu (menuitem)
            if submenu is not None:
                self._checkDuplicatesShortcuts (submenu, duplicates)


    def _getExistingShortcuts (self, menu, duplicateFunc):
        """
        Возвращает список уже присвоенных шорткатов.
        Возвращает словарь шорткатов
        menu - меню, из которого нужно извлечь шорткаты
        duplicateFunc - функция, которая вызывается в случае обнаружения повторяющихся шорткатов. Функция принимает две строки с пунктами меню, где совпадают шорткаты.
        """
        # Ключ - буква, клавиатурного сокращения (подчеркнутая буква, буква перед которой стоит &)
        # Значение - название пункта меню.
        shortcuts = {}

        menuitems = self._getMenuItems (menu)

        for menuitem, position in zip (menuitems, range(len (menuitems))):
            title = self._getText (menuitem, position)
            shortcut = self._extractShortcut (title)

            if shortcut in shortcuts:
                duplicateFunc (shortcuts[shortcut], title)

            if len (shortcut) != 0:
                shortcuts[shortcut] = title

        return shortcuts


    def _assignMenuShortcuts (self, menu):
        """
        Проверить и применить клавишные сокращения для одного меню
        """
        def noneDuplicateFunc (shortcut, title):
            """
            Функция, используемая в случае, если при обнаружении повторения шортката делать ничего не надо
            """
            pass

        # Ключ - буква, клавиатурного сокращения (подчеркнутая буква, буква перед которой стоит &)
        # Значение - название пункта меню.
        shortcuts = self._getExistingShortcuts (menu, noneDuplicateFunc)

        menuitems = self._getMenuItems (menu)

        for menuitem, position in zip (menuitems, range(len (menuitems))):
            title = self._getText (menuitem, position)
            shortcut = self._extractShortcut (title)

            if len (shortcut) == 0:
                newtitle, newshortcut = self._findNewShortcut (title, shortcuts)
                if len (newshortcut) != 0:
                    shortcuts[newshortcut] = newtitle
                    self._setText (menuitem, newtitle, position)

            submenu = self._getSubMenu (menuitem)
            if submenu is not None:
                self._assignMenuShortcuts (submenu)


    @staticmethod
    def _getSubMenu (menuitem):
        if isinstance (menuitem, wx.MenuItem):
            return menuitem.GetSubMenu()
        elif isinstance (menuitem, wx.Menu):
            return menuitem


    @staticmethod
    def _getMenuItems (menu):
        """
        Получить список подменю в зависимости от класса menu
        """
        if isinstance (menu, wx.Menu):
            return menu.GetMenuItems()
        elif isinstance (menu, wx.MenuBar):
            return [currentmenu for currentmenu, title in menu.GetMenus()]


    @staticmethod
    def _getText (menuitem, position):
        """
        Получить заголовок меню (или элемента меню) в зависимости от типа menuitem
        """
        if isinstance (menuitem, wx.MenuItem):
            return menuitem.GetItemLabel()
        elif isinstance (menuitem, wx.Menu):
            menubar = menuitem.GetMenuBar()
            return menubar.GetMenuLabel (position)


    @staticmethod
    def _setText (menuitem, title, position):
        """
        Получить заголовок меню (или элемента меню) в зависимости от типа menuitem
        """
        if isinstance (menuitem, wx.MenuItem):
            menuitem.SetItemLabel (title)
            checkable = menuitem.IsCheckable()
            checked = menuitem.IsChecked() if checkable else False
            enabled = menuitem.IsEnabled()

            # Без удаления пункта не хотят появляться подчеркивания
            menu = menuitem.GetMenu()

            menu.RemoveItem (menuitem)
            menu.InsertItem (position, menuitem)

            menuitem.Enable (enabled)

            if checkable:
                # После удаления пункта меню пропадает его "чекабельность"
                # Только таким образом ее удается восстановить (по крайней мере под Unity)
                menuitem.Check(False)
                menuitem.Check (checked)

        elif isinstance (menuitem, wx.Menu):
            menubar = menuitem.GetMenuBar()
            menubar.SetMenuLabel (position, title)


    @staticmethod
    def _findNewShortcut (title, shortcuts):
        """
        Метод подбирает наиболее подходящее место для подчеркивания (если это возможно) и возвращает кортеж из нового заголовка меню и нового клавиатурного сокращения
        title - исходный заголовок меню
        shortcuts - словарь уже занятых шорткатов

        Если невозможно подобр шорткат, то возвращается кортеж из исходного заголовка и пустой строки
        """
        newtitle = title
        newshortcut = u""

        for index in range (len (title)):
            if (title[index].lower() not in shortcuts and
                    len (title[index].strip()) != 0):
                newshortcut = title[index].lower()
                newtitle = title[:index] + "&" + title[index:]
                break

        return newtitle, newshortcut



    @staticmethod
    def _extractShortcut (title):
        """
        Возвращает букву, перед которой стоит знак &. Если такой буквы нет, возвращает пустую строку
        Учитывается тот факт, что строка && означает, что & надо просто показать
        "&&&&Бла-бла-бла" не делает подчеркнутым первый &
        "&&&Бла-бла-бла" делает подчеркнутой букву "Б"

        В реальности вместо амперсандов мы получим знаки подчеркивания "_"
        """
        # Удалим все не значащие &&, чтобы они не мешались
        cleartitle = title.replace (u"&&", "")
        index = cleartitle.find (u"&")
        if index == -1 or index == len (cleartitle) - 1:
            return u""

        return cleartitle[index + 1].lower()


    @staticmethod
    def _extractHotKey (title):
        """
        Возвращает горячую клавишу для меню (то, что идет после символа табуляции)
        """
        substrings = title.split ("\t", 1)
        return substrings[1] if len (substrings) == 2 else u""
