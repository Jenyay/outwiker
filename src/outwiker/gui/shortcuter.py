#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Версия 1.0
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


    def checkDublicates (self):
        """
        Проверить шорткаты на повторы. Возвращает список заголовков с дублирующимися шорткатами
        """
        dublicates = []

        self._checkDublicates (self._menubar, dublicates)
        return dublicates


    def _checkDublicates (self, menu, dublicatesList):
        self._getExistingShortcuts (menu, lambda shortcut, title: dublicatesList.append (title))

        menuitems = self._getMenuItems (menu)

        for menuitem, position in zip (menuitems, range (len (menuitems))):
            submenu = self._getSubMenu (menuitem)
            if submenu != None:
                self._checkDublicates (submenu, dublicatesList)


    def _getExistingShortcuts (self, menu, dublicateFunc):
        """
        Возвращает список уже присвоенных шорткатов.
        Возвращает словарь шорткатов
        menu - меню, из которого нужно извлечь шорткаты
        dublicateFunc - функция, которая вызывается в случае обнаружения повторяющихся шорткатов. Функция принимает два аргумента: строку с буквой-шорткатом и заголовок пункта меню, к которому этот шорткат относится.
        """
        # Ключ - буква, клавиатурного сокращения (подчеркнутая буква, буква перед которой стоит &)
        # Значение - название пункта меню.
        shortcuts = {}

        menuitems = self._getMenuItems (menu)

        for menuitem, position in zip (menuitems, range (len (menuitems))):
            title = self._getText (menuitem, position)
            shortcut = self._extractShortcut (title)

            if shortcut in shortcuts:
                dublicateFunc (shortcuts[shortcut], title)

            if len (shortcut) != 0:
                shortcuts[shortcut] = title

        return shortcuts


    def _assignMenuShortcuts (self, menu):
        """
        Проверить и применить клавишные сокращения для одного меню
        """
        def noneDublicateFunc (shortcut, title):
            """
            Функция, используемая в случае, если при обнаружении повторения шортката делать ничего не надо
            """
            pass

        # Ключ - буква, клавиатурного сокращения (подчеркнутая буква, буква перед которой стоит &)
        # Значение - название пункта меню.
        shortcuts = self._getExistingShortcuts (menu, noneDublicateFunc)

        menuitems = self._getMenuItems (menu)

        for menuitem, position in zip (menuitems, range (len (menuitems))):
            title = self._getText (menuitem, position)
            shortcut = self._extractShortcut (title)
            # print title

            if len (shortcut) == 0:
                newtitle, newshortcut = self._findNewShortcut (title, shortcuts)
                if len (newshortcut) != 0:
                    shortcuts[newshortcut] = newtitle
                    self._setText (menuitem, newtitle, position)

            submenu = self._getSubMenu (menuitem)
            if submenu != None:
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
            return [menu for menu, title in menu.GetMenus()]


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

            # Без удаления пункта не хотят появляться подчеркивания
            menu = menuitem.GetMenu()
            menu.RemoveItem (menuitem)
            menu.InsertItem (position, menuitem)
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
