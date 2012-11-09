#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Модуль с функциями сортировки страниц
"""

def sortOrderFunction (page1, page2):
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

    return sortAlphabeticalFunction (page1, page2)


def sortAlphabeticalFunction (page1, page2):
    """
    Функция для сортировки страниц по алфавиту
    """
    if page1.title.lower() > page2.title.lower():
        return 1
    elif page1.title.lower() < page2.title.lower():
        return -1

    return 0
