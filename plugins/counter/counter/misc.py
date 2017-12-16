# -*- coding: UTF-8 -*-
"""
Небольшие функции, которые могут быть использованы в разных классах
"""
import os.path


def getImagePath(image_name):
    """
    Получить полный путь до картинки
    """
    imagedir = str(os.path.join(os.path.dirname(__file__), "images"))
    fname = os.path.join(imagedir, image_name)
    return fname
