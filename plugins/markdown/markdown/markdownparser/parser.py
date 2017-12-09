# -*- coding: UTF-8 -*-

from markdown_plugin_libs.markdown import markdown
from markdown_plugin_libs.markdown.extensions.fenced_code import FencedCodeExtension
from markdown_plugin_libs.markdown.extensions.codehilite import CodeHiliteExtension
from markdown_plugin_libs.markdown.extensions.tables import TableExtension
from pygments.formatters import HtmlFormatter

CUSTOM_STYLES = u"""
div.{name} {{border-style: solid; border-color: gray; border-width: 1px; padding: 0.5em;}}
table {{
    border-collapse: collapse;
}}

td, th {{
    padding: 0.2em 0.5em;
    border: 1px solid gray;
   }}

div.{name} > pre {{
    white-space: pre-wrap;       /* css-3 */
    white-space: -moz-pre-wrap;  /* Mozilla, since 1999 */
    white-space: -pre-wrap;      /* Opera 4-6 */
    white-space: -o-pre-wrap;    /* Opera 7 */
    word-wrap: break-word;       /* Internet Explorer 5.5+ */
}}
"""


class Parser (object):
    def __init__(self):
        self._cssclass = u'codehilite'

    def getCSS(self):
        formatter = HtmlFormatter(style=u'default', cssclass=self._cssclass)
        css = formatter.get_style_defs()
        css += CUSTOM_STYLES.format(name=self._cssclass)
        return css

    def convert(self, text):
        html = markdown(
            text,
            output_format='html5',
            extensions=[CodeHiliteExtension(),
                        FencedCodeExtension(),
                        TableExtension()]
        )
        return html
