# -*- coding: utf-8 -*-

import re
from string import Template

from outwiker.core.application import Application
from outwiker.gui.guiconfig import HtmlRenderConfig
import outwiker.core.cssclasses as css


class MyTemplate (Template):
    """
    Класс работы с шаблонами. Единственное, для чего сделан такой класс
    - избавиться от замены $$ на $
    Реализация регулярного выражения частично взята
    из http://stackoverflow.com/a/12769116
    """

    pattern = r"""
      %(delim)s(?:
      (?P<escaped>^$) |          # Отключим замену $$
      (?P<named>%(id)s) |        # delimiter and a Python identifier
      {(?P<braced>%(id)s)} |     # delimiter and a braced identifier
      (?P<invalid>^$)            # never matches (the regex is not multilined)
    )
    """ % dict(delim=re.escape(Template.delimiter), id=Template.idpattern)


class HtmlTemplate(object):
    """Класс для генерации HTML-страницы на основе шаблона."""

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

    def substitute(self, content, **kwargs):
        """
        In outwiker.core 1.5 'userhead' parameter will be replaced to **kwargs
        TODO: Remove the legacy code
        """
        if 'userhead' not in kwargs:
            kwargs['userhead'] = ''
        if 'title' not in kwargs:
            kwargs['title'] = ''

        return self.template.safe_substitute(content=content,
                                             fontsize=self.fontsize,
                                             fontfamily=self.fontfamily,
                                             userstyle=self.userStyle,
                                             defaultstyle=css.getDefaultStyles(),
                                             **kwargs)
