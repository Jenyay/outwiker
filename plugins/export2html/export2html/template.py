# -*- coding: UTF-8 -*-

from string import Template
import os.path

from outwiker.core.system import getOS


def loadTemplate (fname):
    """
    Загрузить шаблон.
    """
    templatedir = u"templates"

    currentdir = unicode ((os.path.dirname (__file__)), getOS().filesEncoding)

    templateFileName = os.path.join (currentdir, templatedir, fname)

    with open (templateFileName) as fp:
        template = unicode (fp.read(), "utf8")

    return Template (template)
