# -*- coding: utf-8 -*-

from string import Template
import os.path

from outwiker.core.system import getOS
from outwiker.utilites.textfile import readTextFile


def loadTemplate (fname):
    """
    Загрузить шаблон.
    """
    templatedir = u"templates"

    currentdir = str ((os.path.dirname (__file__)))

    templateFileName = os.path.join (currentdir, templatedir, fname)
    template = readTextFile(templateFileName)

    return Template (template)
