# coding: utf-8

from typing import List, Optional

from outwiker.core.htmlformatter import HtmlFormatter
import outwiker.core.cssclasses as css


def create_link_to_page(href: str, text: str) -> str:
    html = HtmlFormatter()
    css_classes = [css.CSS_WIKI, css.CSS_LINK_PAGE]
    return html.link(href, text, css_classes)


def create_link_to_attached_file(href: str, text: str) -> str:
    html = HtmlFormatter()
    css_classes = [css.CSS_WIKI, css.CSS_LINK_ATTACH, css.CSS_ATTACH_FILE]
    return html.link(href, text, css_classes)


def create_image(src: str, css_classes: Optional[List[str]] = None) -> str:
    if css_classes:
        css_class = ' '.join(css_classes)
        return '<img class="{css_class}" src="{src}"/>'.format(css_class=css_class, src=src)
    else:
        return '<img src="{src}"/>'.format(src=src)
