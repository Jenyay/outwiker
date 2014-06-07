# -*- coding: UTF-8 -*-

from string import Template

from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.core.application import Application


class HtmlTemplate (object):
    """
    Класс для генерации HTML-страницы на основе шаблона
    """
    def __init__ (self, template):
        """
        template - текст шаблона

        Шаблон должен иметь содержание которого оформлено в стиле,
        описанном в http://docs.python.org/library/string.html#template-strings
        """
        self.config = HtmlRenderConfig (Application.config)

        self.fontsize = self.config.fontSize.value
        self.fontfamily = self.config.fontName.value
        self.userStyle = self.config.userStyle.value

        self.template = Template (template)


    def substitute (self, content, userhead=u""):
        return self.template.safe_substitute (content = content,
                                              fontsize = self.fontsize,
                                              fontfamily = self.fontfamily,
                                              userstyle = self.userStyle,
                                              userhead = userhead)
