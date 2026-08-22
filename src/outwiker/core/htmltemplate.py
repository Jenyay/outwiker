# -*- coding: utf-8 -*-

import re
from string import Template

import rcssmin

from outwiker.gui.guiconfig import HtmlRenderConfig
import outwiker.core.cssclasses as css


class MyTemplate(Template):
    """
    Template class. The only reason for this class is to disable
    $$ to $ replacement.
    Regular expression implementation is partially taken from
    http://stackoverflow.com/a/12769116
    """

    pattern = r"""
      %(delim)s(?:
      (?P<escaped>^$) |          # Disable $$ replacement
      (?P<named>%(id)s) |        # delimiter and a Python identifier
      {(?P<braced>%(id)s)} |     # delimiter and a braced identifier
      (?P<invalid>^$)            # never matches (the regex is not multilined)
    )
    """ % dict(delim=re.escape(Template.delimiter), id=Template.idpattern)


class HtmlTemplate:
    """Class for generating HTML page based on a template."""

    def __init__(self, application, template):
        """
        template - template text

        Template content must be in the style described in
        http://docs.python.org/library/string.html#template-strings,
        except that $$ in the template is not replaced with $
        """
        self.config = HtmlRenderConfig(application.config)

        self.fontsize = self.config.fontSize.value
        self.fontfamily = self.config.fontName.value
        self.userStyle = self.config.userStyle.value

        self.template = MyTemplate(template)

    def substitute(self, content, **kwargs):
        if "userhead" not in kwargs:
            kwargs["userhead"] = ""
        if "title" not in kwargs:
            kwargs["title"] = ""

        custom_styles_str = "\n".join(
            kwargs.get("custom_styles", []) + [self.userStyle]
        )
        custom_styles_str = HtmlTemplate.minimize_css(custom_styles_str)

        default_styles = HtmlTemplate.minimize_css(css.getDefaultStyles())

        return self.template.safe_substitute(
            content=content,
            fontsize=self.fontsize,
            fontfamily=self.fontfamily,
            userstyle=custom_styles_str,
            defaultstyle=default_styles,
            **kwargs,
        )

    @staticmethod
    def minimize_css(css_text: str) -> str:
        return rcssmin.cssmin(css_text)
