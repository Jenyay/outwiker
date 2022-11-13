# coding: utf-8

from typing import List, Optional

import outwiker.core.cssclasses as css


def create_link(href: str, text: str, css_classes: Optional[List[str]] = None) -> str:
    if css_classes:
        css_class = ' '.join(css_classes)
        return '<a class="{css_class}" href="{href}">{text}</a>'.format(
                css_class=css_class, href=href, text=text)
    else:
        return '<a href="{href}">{text}</a>'.format(href=href, text=text)


def create_link_to_page(href: str, text: str) -> str:
    css_classes = [css.CSS_WIKI, css.CSS_LINK_PAGE]
    return create_link(href, text, css_classes)


def create_link_to_attached_file(href: str, text: str) -> str:
    css_classes = [css.CSS_WIKI, css.CSS_LINK_ATTACH, css.CSS_ATTACH_FILE]
    return create_link(href, text, css_classes)


def create_anchor(anchor: str) -> str:
    return'<a id="{anchor}"></a>'.format(anchor=anchor) 


def create_image(src: str, css_classes: Optional[List[str]] = None) -> str:
    if css_classes:
        css_class = ' '.join(css_classes)
        return '<img class="{css_class}" src="{src}"/>'.format(css_class=css_class, src=src)
    else:
        return '<img src="{src}"/>'.format(src=src)
