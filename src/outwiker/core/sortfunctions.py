# -*- coding: utf-8 -*-
"""
Module with page sorting functions
"""


def sortOrderFunction(page1, page2):
    """
    Function for sorting pages with order consideration
    """
    orderpage1 = page1.params.orderOption.value
    orderpage2 = page2.params.orderOption.value

    # If the page order has not been set yet (default value: -1)
    if orderpage1 == -1 or orderpage2 == -1:
        return sortAlphabeticalFunction(page1, page2)
    elif orderpage1 > orderpage2:
        return 1
    elif orderpage1 < orderpage2:
        return -1

    return 0


def sortAlphabeticalFunction(page1, page2):
    """
    Function for sorting pages alphabetically
    """
    if page1.display_title.lower() > page2.display_title.lower():
        return 1
    elif page1.display_title.lower() < page2.display_title.lower():
        return -1

    return 0
