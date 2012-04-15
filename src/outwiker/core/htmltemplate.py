#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from string import Template
import os.path

from outwiker.gui.guiconfig import HtmlRenderConfig
from .application import Application


class HtmlTemplate (object):
    """
    Класс для генерации HTML-страницы на основе шаблона
    """
    def __init__ (self, path):
        """
        path - путь до директории с шаблоном. 

        Основной шаблон должен иметь имя template.html, 
        содержание которого оформлено в стиле, описанном в http://docs.python.org/library/string.html#template-strings
        """
        self.config = HtmlRenderConfig (Application.config)

        self.fontsize = self.config.fontSize.value
        self.fontfamily = self.config.fontName.value
        self.userStyle = self.config.userStyle.value

        tpl_fname = u"__default.html"
        tpl_path = os.path.join (path, tpl_fname)

        with open (tpl_path) as fp:
            self.template = Template (unicode (fp.read().strip(), "utf8") )


    def substitute (self, content, userhead=u""):
        return self.template.substitute (content=content, 
                fontsize=self.fontsize,
                fontfamily = self.fontfamily,
                userstyle = self.userStyle,
                userhead=userhead)
