# -*- coding: utf-8 -*-

from string import Template
import os.path

from outwiker.api.core.text import readTextFile


def loadTemplate(fname: str) -> Template:
    """
    Load template from file
    """
    templatedir = "templates"

    currentdir = str((os.path.dirname(__file__)))

    templateFileName = os.path.join(currentdir, templatedir, fname)
    template = readTextFile(templateFileName)

    return Template(template)
