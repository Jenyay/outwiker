# -*- coding: utf-8 -*-
"""
Небольшие функции, которые могут быть использованы в разных классах
"""
import os.path


def getImagePath(imageName):
    """
    Получить полный путь до картинки
    """
    imagedir = os.path.join(os.path.dirname(__file__), "images")
    fname = os.path.join(imagedir, imageName)
    return fname
