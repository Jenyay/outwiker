# -*- coding: UTF-8 -*-

import re
from string import Template

from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.core.application import Application


class MyTemplate (Template):
    """
    Класс работы с шаблонами. Единственное, для чего сделан такой класс
    - избавитсья от замены $$ на $
    Реализация регулярного выражения частично взята
    из http://stackoverflow.com/a/12769116
    """
    pattern = ur"""
      %(delim)s(?:
      (?P<escaped>^$) |          # Отключим замену $$
      (?P<named>%(id)s) |        # delimiter and a Python identifier
      {(?P<braced>%(id)s)} |     # delimiter and a braced identifier
      (?P<invalid>^$)            # never matches (the regex is not multilined)
    )
    """ % dict(delim=re.escape(Template.delimiter), id=Template.idpattern)


class HtmlTemplate(object):
    """
    Класс для генерации HTML-страницы на основе шаблона
    """
    def __init__(self, template):
        """
        template - текст шаблона

        Шаблон должен иметь содержание которого оформлено в стиле,
        описанном в http://docs.python.org/library/string.html#template-strings
        за исключением того, что в шаблоне $$ не заменяется на $
        """
        self.config = HtmlRenderConfig(Application.config)

        self.fontsize = self.config.fontSize.value
        self.fontfamily = self.config.fontName.value
        self.userStyle = self.config.userStyle.value

        self.template = MyTemplate(template)

    def substitute(self, content, userhead=u""):
        return self.template.safe_substitute(content=content,
                                             fontsize=self.fontsize,
                                             fontfamily=self.fontfamily,
                                             userstyle=self.userStyle,
                                             userhead=userhead)
