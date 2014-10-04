# -*- coding: UTF-8 -*-

from string import Template
import os.path


def loadTemplate (fname):
    """
    Загрузить шаблон.
    """
    templatedir = u"templates"

    templateFileName = os.path.join (os.path.dirname (__file__),
                                     templatedir,
                                     fname)

    with open (templateFileName) as fp:
        template = unicode (fp.read(), "utf8")

    return Template (template)
