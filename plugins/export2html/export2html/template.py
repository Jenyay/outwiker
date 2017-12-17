# -*- coding: UTF-8 -*-

from string import Template
import os.path

from outwiker.core.system import getOS


def loadTemplate (fname):
    """
    Загрузить шаблон.
    """
    templatedir = u"templates"

    currentdir = str ((os.path.dirname (__file__)))

    templateFileName = os.path.join (currentdir, templatedir, fname)

    with open (templateFileName) as fp:
        template = fp.read()

    return Template (template)
